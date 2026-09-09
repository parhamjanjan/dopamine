from datetime import datetime, time, timedelta

from django.utils import timezone

from .models import (
    RoomMembership,
    StudySession,
    StudyTimeLog,
)


def get_period_range(period):
    now = timezone.now()
    local_now = timezone.localtime(now)

    today = local_now.date()

    if period == 'today':
        start_date = today
        end_date = today

    elif period == 'yesterday':
        yesterday = today - timedelta(days=1)

        start_date = yesterday
        end_date = yesterday

    elif period == 'week':
        # شروع هفته: شنبه
        #
        # weekday():
        # Monday = 0
        # Tuesday = 1
        # Wednesday = 2
        # Thursday = 3
        # Friday = 4
        # Saturday = 5
        # Sunday = 6

        days_since_saturday = (
            local_now.weekday() - 5
        ) % 7

        start_date = (
            today -
            timedelta(
                days=days_since_saturday
            )
        )

        end_date = today

    elif period == 'all':
        return None, None

    else:
        return None, None

    current_timezone = (
        timezone.get_current_timezone()
    )

    start = timezone.make_aware(
        datetime.combine(
            start_date,
            time.min
        ),
        current_timezone
    )

    end = timezone.make_aware(
        datetime.combine(
            end_date + timedelta(days=1),
            time.min
        ),
        current_timezone
    )

    return start, end


def get_room_ranking(
    room_id,
    period='today'
):
    memberships = (
        RoomMembership.objects
        .filter(
            room_id=room_id,
            is_active=True,
            room__is_active=True,
        )
        .select_related('user')
    )

    start, end = get_period_range(period)

    ranking = []

    now = timezone.now()

    for membership in memberships:

        logs = (
            StudyTimeLog.objects
            .filter(
                session__membership=membership,
                state=StudyTimeLog.StudyState.FOCUSED,
            )
        )

        if start is not None:
            logs = logs.filter(
                started_at__lt=end,
                ended_at__gt=start,
            )

        total_seconds = 0

        for log in logs:

            log_start = log.started_at

            log_end = (
                log.ended_at
                if log.ended_at
                else now
            )

            if start is not None:
                effective_start = max(
                    log_start,
                    start
                )

                effective_end = min(
                    log_end,
                    end
                )
            else:
                effective_start = log_start
                effective_end = log_end

            if effective_end <= effective_start:
                continue

            total_seconds += int(
                (
                    effective_end -
                    effective_start
                ).total_seconds()
            )

        active_session = (
            StudySession.objects
            .filter(
                membership=membership,
                is_active=True,
                status=StudySession.Status.ACTIVE,
            )
            .first()
        )

        is_studying = bool(
            active_session
            and active_session.current_state
            == StudySession.StudyState.FOCUSED
        )

        ranking.append({
            'user_id': membership.user.id,
            'username': membership.user.username,
            'study_seconds': total_seconds,
            'study_minutes': total_seconds // 60,
            'is_studying': is_studying,
        })

    ranking.sort(
        key=lambda item: item['study_seconds'],
        reverse=True
    )

    for index, item in enumerate(
        ranking,
        start=1
    ):
        item['rank'] = index

    return ranking