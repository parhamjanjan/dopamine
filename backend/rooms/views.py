from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    StudyRoom,
    RoomMembership,
    StudySession,
    StudyTimeLog,
)

from .serializers import (
    StudyRoomSerializer,
    RoomMembershipSerializer,
    StudySessionSerializer,
)

from .services import (
    get_room_ranking,
)


def broadcast_room_ranking(room_id):
    """
    به تمام کاربران متصل به سالن اطلاع می‌دهد
    که Ranking باید دوباره محاسبه شود.
    """

    channel_layer = get_channel_layer()

    async_to_sync(
        channel_layer.group_send
    )(
        f'study_room_{room_id}',
        {
            'type': 'ranking_refresh',
        }
    )


def update_study_time_log(
    session,
    new_state,
    now
):
    """
    وضعیت قبلی جلسه را می‌بندد و در صورت تغییر وضعیت،
    وضعیت جدید را شروع می‌کند.

    فقط زمانی که وضعیت قبلی FOCUSED باشد،
    زمان مطالعه به valid_study_seconds اضافه می‌شود.
    """

    previous_state = (
        session.current_state
    )

    previous_heartbeat = (
        session.last_heartbeat_at
    )

    if previous_heartbeat is None:
        previous_heartbeat = now

    elapsed = (
        now - previous_heartbeat
    ).total_seconds()

    # جلوگیری از ثبت زمان غیرمنطقی
    MAX_HEARTBEAT_INTERVAL = 30

    elapsed = min(
        max(elapsed, 0),
        MAX_HEARTBEAT_INTERVAL
    )

    elapsed_seconds = int(
        elapsed
    )

    # پیدا کردن Log باز قبلی
    previous_log = (
        StudyTimeLog.objects
        .filter(
            session=session,
            ended_at__isnull=True,
        )
        .order_by('-started_at')
        .first()
    )

    if previous_log:

        previous_log.ended_at = now

        previous_log.duration_seconds += (
            elapsed_seconds
        )

        previous_log.save(
            update_fields=[
                'ended_at',
                'duration_seconds',
            ]
        )

    elif elapsed_seconds > 0:

        StudyTimeLog.objects.create(
            session=session,
            state=previous_state,
            started_at=previous_heartbeat,
            ended_at=now,
            duration_seconds=elapsed_seconds,
        )

    # اگر وضعیت تغییر کرده،
    # Log جدید را باز می‌کنیم.
    if new_state != previous_state:

        StudyTimeLog.objects.create(
            session=session,
            state=new_state,
            started_at=now,
            ended_at=None,
            duration_seconds=0,
        )

    # فقط Focused زمان مطالعه محسوب می‌شود.
    if (
        previous_state
        == StudySession.StudyState.FOCUSED
    ):
        return elapsed_seconds

    return 0


class StudyRoomListCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        rooms = (
            StudyRoom.objects
            .filter(
                is_active=True
            )
            .select_related('owner')
        )

        serializer = StudyRoomSerializer(
            rooms,
            many=True,
            context={
                'request': request
            }
        )

        return Response(
            serializer.data
        )

    @transaction.atomic
    def post(self, request):

        serializer = StudyRoomSerializer(
            data=request.data,
            context={
                'request': request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        room = serializer.save(
            owner=request.user
        )

        RoomMembership.objects.create(
            room=room,
            user=request.user,
            is_active=True,
        )

        response_serializer = (
            StudyRoomSerializer(
                room,
                context={
                    'request': request
                }
            )
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class StudyRoomDetailView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        room_id
    ):

        room = get_object_or_404(
            StudyRoom,
            id=room_id,
            is_active=True,
        )

        serializer = StudyRoomSerializer(
            room,
            context={
                'request': request
            }
        )

        membership = (
            RoomMembership.objects
            .filter(
                room=room,
                user=request.user,
                is_active=True,
            )
            .first()
        )

        active_session = None

        if membership:

            active_session = (
                StudySession.objects
                .filter(
                    membership=membership,
                    status=StudySession.Status.ACTIVE,
                    is_active=True,
                )
                .first()
            )

        return Response({

            **serializer.data,

            'active_session': (
                StudySessionSerializer(
                    active_session
                ).data

                if active_session

                else None
            ),
        })


class JoinStudyRoomView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def post(
        self,
        request,
        room_id
    ):

        room = (
            StudyRoom.objects
            .select_for_update()
            .filter(
                id=room_id,
                is_active=True,
            )
            .first()
        )

        if not room:

            return Response(
                {
                    'detail':
                        'سالن موردنظر پیدا نشد.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -------------------------------------------------
        # بررسی عضویت فعلی در همین سالن
        # -------------------------------------------------

        existing_membership = (
            RoomMembership.objects
            .filter(
                room=room,
                user=request.user,
            )
            .first()
        )

        if (
            existing_membership
            and existing_membership.is_active
        ):

            return Response(
                {
                    'detail':
                        'شما قبلاً عضو این سالن هستید.',

                    'membership':
                        RoomMembershipSerializer(
                            existing_membership
                        ).data,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------------------------
        # هر کاربر فقط یک سالن فعال
        # -------------------------------------------------

        another_membership = (
            RoomMembership.objects
            .filter(
                user=request.user,
                is_active=True,
                room__is_active=True,
            )
            .exclude(
                room=room
            )
            .select_related('room')
            .first()
        )

        if another_membership:

            return Response(
                {
                    'detail':
                        'شما در حال حاضر عضو '
                        'یک سالن دیگر هستید.',

                    'room_id':
                        another_membership.room.id,

                    'room_name':
                        another_membership.room.name,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------------------------
        # سالن خصوصی
        # -------------------------------------------------

        if room.is_private:

            join_code = request.data.get(
                'join_code',
                ''
            )

            if join_code != room.join_code:

                return Response(
                    {
                        'detail':
                            'کد ورود سالن نادرست است.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # -------------------------------------------------
        # ظرفیت
        # -------------------------------------------------

        member_count = (
            RoomMembership.objects
            .filter(
                room=room,
                is_active=True,
            )
            .count()
        )

        if member_count >= room.max_members:

            return Response(
                {
                    'detail':
                        'ظرفیت این سالن تکمیل شده است.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------------------------
        # فعال کردن عضویت قبلی
        # -------------------------------------------------

        if existing_membership:

            existing_membership.is_active = True

            existing_membership.joined_at = (
                timezone.now()
            )

            existing_membership.save(
                update_fields=[
                    'is_active',
                    'joined_at',
                ]
            )

            membership = (
                existing_membership
            )

        else:

            membership = (
                RoomMembership.objects.create(
                    room=room,
                    user=request.user,
                    is_active=True,
                )
            )

        # -------------------------------------------------
        # اطلاع‌رسانی Ranking
        # -------------------------------------------------

        broadcast_room_ranking(
            room.id
        )

        return Response(
            RoomMembershipSerializer(
                membership
            ).data,
            status=status.HTTP_201_CREATED
        )


class LeaveStudyRoomView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def post(
        self,
        request,
        room_id
    ):

        membership = get_object_or_404(
            RoomMembership,
            room_id=room_id,
            user=request.user,
            is_active=True
        )

        active_session = (
            StudySession.objects
            .filter(
                membership=membership,
                is_active=True
            )
            .first()
        )

        if active_session:

            now = timezone.now()

            # ثبت آخرین بازه مطالعه
            update_study_time_log(
                active_session,
                active_session.current_state,
                now
            )

            active_log = (
                StudyTimeLog.objects
                .filter(
                    session=active_session,
                    ended_at__isnull=True,
                )
                .order_by('-started_at')
                .first()
            )

            if active_log:

                active_log.ended_at = now

                active_log.save(
                    update_fields=[
                        'ended_at'
                    ]
                )

            active_session.ended_at = now

            active_session.status = (
                StudySession.Status.INTERRUPTED
            )

            active_session.is_active = False

            active_session.save(
                update_fields=[
                    'ended_at',
                    'status',
                    'is_active',
                ]
            )

        membership.is_active = False

        membership.save(
            update_fields=[
                'is_active'
            ]
        )

        # Ranking بعد از خروج کاربر
        broadcast_room_ranking(
            room_id
        )

        return Response(
            {
                'detail':
                    'با موفقیت از سالن خارج شدید.'
            }
        )


class StartStudyView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def post(
        self,
        request,
        room_id
    ):

        membership = get_object_or_404(
            RoomMembership,
            room_id=room_id,
            user=request.user,
            is_active=True
        )

        existing_session = (
            StudySession.objects
            .filter(
                membership=membership,
                is_active=True
            )
            .first()
        )

        if existing_session:

            return Response(
                {
                    'detail':
                        'یک جلسه مطالعه فعال دارید.',

                    'session':
                        StudySessionSerializer(
                            existing_session
                        ).data
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        now = timezone.now()

        session = (
            StudySession.objects.create(
                membership=membership,

                started_at=now,

                last_heartbeat_at=now,

                current_state=
                    StudySession.StudyState.AWAY,

                status=
                    StudySession.Status.ACTIVE,

                is_active=True,
            )
        )

        # در شروع جلسه وضعیت هنوز AWAY است
        # تا اولین heartbeat وضعیت واقعی را تعیین کند.

        broadcast_room_ranking(
            room_id
        )

        return Response(
            StudySessionSerializer(
                session
            ).data,
            status=status.HTTP_201_CREATED
        )


class StopStudyView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def post(
        self,
        request,
        room_id
    ):

        membership = get_object_or_404(
            RoomMembership,
            room_id=room_id,
            user=request.user,
            is_active=True
        )

        session = get_object_or_404(
            StudySession,
            membership=membership,
            is_active=True,
            status=StudySession.Status.ACTIVE
        )

        now = timezone.now()

        # ثبت آخرین بازه وضعیت
        added_seconds = update_study_time_log(
            session,
            session.current_state,
            now
        )

        if (
            session.current_state
            == StudySession.StudyState.FOCUSED
        ):
            session.valid_study_seconds += (
                added_seconds
            )

        # بستن Log باز
        active_log = (
            StudyTimeLog.objects
            .filter(
                session=session,
                ended_at__isnull=True,
            )
            .order_by('-started_at')
            .first()
        )

        if active_log:

            active_log.ended_at = now

            active_log.save(
                update_fields=[
                    'ended_at'
                ]
            )

        session.ended_at = now

        session.status = (
            StudySession.Status.COMPLETED
        )

        session.is_active = False

        session.save(
            update_fields=[
                'ended_at',
                'status',
                'is_active',
                'valid_study_seconds',
            ]
        )

        # -------------------------------------------------
        # Ranking بعد از Stop
        # -------------------------------------------------

        broadcast_room_ranking(
            room_id
        )

        return Response(
            StudySessionSerializer(
                session
            ).data
        )


class StudyHeartbeatView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def post(
        self,
        request,
        room_id
    ):

        membership = get_object_or_404(
            RoomMembership,
            room_id=room_id,
            user=request.user,
            is_active=True
        )

        session = get_object_or_404(
            StudySession.objects.select_for_update(),
            membership=membership,
            is_active=True,
            status=StudySession.Status.ACTIVE
        )

        state = request.data.get(
            'state'
        )

        confidence = request.data.get(
            'confidence',
            0
        )

        valid_states = {
            StudySession.StudyState.FOCUSED,

            StudySession.StudyState.DISTRACTED,

            StudySession.StudyState.AWAY,
        }

        if state not in valid_states:

            return Response(
                {
                    'detail':
                        'وضعیت مطالعه نامعتبر است.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):

            confidence = 0

        confidence = max(
            0.0,
            min(
                1.0,
                confidence
            )
        )

        now = timezone.now()

        # -------------------------------------------------
        # ثبت بازه وضعیت قبلی
        # -------------------------------------------------

        added_seconds = (
            update_study_time_log(
                session,
                state,
                now
            )
        )

        # فقط Focused زمان مطالعه محسوب می‌شود.
        session.valid_study_seconds += (
            added_seconds
        )

        # -------------------------------------------------
        # وضعیت جدید
        # -------------------------------------------------

        session.current_state = state

        session.last_heartbeat_at = now

        session.save(
            update_fields=[
                'current_state',
                'last_heartbeat_at',
                'valid_study_seconds',
            ]
        )

        # -------------------------------------------------
        # Ranking زنده
        # -------------------------------------------------

        broadcast_room_ranking(
            room_id
        )

        return Response(
            {
                'session_id':
                    session.id,

                'state':
                    session.current_state,

                'confidence':
                    confidence,

                'added_seconds':
                    added_seconds,

                'valid_study_seconds':
                    session.valid_study_seconds,

                'study_minutes':
                    round(
                        session.valid_study_seconds
                        / 60,
                        2
                    ),

                'timestamp':
                    now.isoformat(),
            },
            status=status.HTTP_200_OK
        )