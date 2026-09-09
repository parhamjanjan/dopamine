from rest_framework import serializers

from .models import (
    StudyRoom,
    RoomMembership,
    StudySession,
)


class StudyRoomSerializer(serializers.ModelSerializer):

    owner_username = serializers.CharField(
        source='owner.username',
        read_only=True
    )

    member_count = serializers.SerializerMethodField()

    current_user_membership = serializers.SerializerMethodField()

    is_member = serializers.SerializerMethodField()

    class Meta:
        model = StudyRoom

        fields = [
            'id',
            'name',
            'description',
            'owner',
            'owner_username',
            'max_members',
            'is_private',
            'join_code',
            'is_active',
            'member_count',
            'current_user_membership',
            'is_member',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'owner',
            'owner_username',
            'member_count',
            'current_user_membership',
            'is_member',
            'created_at',
            'updated_at',
        ]

    def get_member_count(self, obj):
        return (
            RoomMembership.objects
            .filter(
                room=obj,
                is_active=True,
            )
            .count()
        )

    def get_current_user_membership(self, obj):
        request = self.context.get('request')

        if (
            not request
            or not request.user
            or not request.user.is_authenticated
        ):
            return None

        membership = (
            RoomMembership.objects
            .filter(
                room=obj,
                user=request.user,
                is_active=True,
            )
            .select_related('user')
            .first()
        )

        if not membership:
            return None

        return {
            'id': membership.id,
            'room': membership.room_id,
            'user': membership.user_id,
            'username': membership.user.username,
            'joined_at': membership.joined_at,
            'is_active': membership.is_active,
        }

    def get_is_member(self, obj):
        request = self.context.get('request')

        if (
            not request
            or not request.user
            or not request.user.is_authenticated
        ):
            return False

        return RoomMembership.objects.filter(
            room=obj,
            user=request.user,
            is_active=True,
        ).exists()


class RoomMembershipSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = RoomMembership

        fields = [
            'id',
            'room',
            'user',
            'username',
            'joined_at',
            'is_active',
        ]

        read_only_fields = [
            'user',
            'joined_at',
        ]


class StudySessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudySession

        fields = [
            'id',
            'membership',
            'started_at',
            'ended_at',
            'valid_study_seconds',
            'current_state',
            'status',
            'last_heartbeat_at',
            'is_active',
            'created_at',
        ]

        read_only_fields = [
            'membership',
            'started_at',
            'ended_at',
            'valid_study_seconds',
            'status',
            'last_heartbeat_at',
            'is_active',
            'created_at',
        ]