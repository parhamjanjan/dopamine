from django.contrib import admin

from .models import (
    StudyRoom,
    RoomMembership,
    StudySession,
)
from .models import RoomChatMessage


class RoomMembershipInline(admin.TabularInline):
    model = RoomMembership

    extra = 0

    fields = [
        'user',
        'joined_at',
        'is_active',
    ]

    readonly_fields = [
        'joined_at',
    ]

    show_change_link = True

    ordering = [
        'joined_at',
    ]


@admin.register(StudyRoom)
class StudyRoomAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'name',
        'owner',
        'member_count',
        'max_members',
        'is_private',
        'is_active',
        'created_at',
    ]

    list_display_links = [
        'id',
        'name',
    ]

    list_filter = [
        'is_active',
        'is_private',
    ]

    search_fields = [
        'name',
        'description',
        'owner__username',
        'join_code',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    fields = [
        'name',
        'description',
        'owner',
        'max_members',
        'is_private',
        'join_code',
        'is_active',
        'created_at',
        'updated_at',
    ]

    inlines = [
        RoomMembershipInline,
    ]

    def member_count(self, obj):
        return obj.memberships.filter(
            is_active=True
        ).count()

    member_count.short_description = 'تعداد اعضای فعال'


@admin.register(RoomMembership)
class RoomMembershipAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'room',
        'user',
        'is_active',
        'joined_at',
    ]

    list_filter = [
        'is_active',
        'room',
    ]

    search_fields = [
        'room__name',
        'user__username',
    ]

    readonly_fields = [
        'joined_at',
    ]

    list_select_related = [
        'room',
        'user',
    ]


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'membership',
        'current_state',
        'status',
        'valid_study_seconds',
        'is_active',
        'started_at',
        'ended_at',
    ]

    list_filter = [
        'status',
        'current_state',
        'is_active',
    ]

    search_fields = [
        'membership__user__username',
        'membership__room__name',
    ]

    readonly_fields = [
        'created_at',
    ]

    list_select_related = [
        'membership',
        'membership__user',
        'membership__room',
    ]


@admin.register(RoomChatMessage)
class RoomChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'room',
        'user',
        'message_preview',
        'created_at',
    )

    list_filter = (
        'room',
        'created_at',
    )

    search_fields = (
        'message',
        'user__username',
        'room__name',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )

    def message_preview(self, obj):
        return obj.message[:70]

    message_preview.short_description = 'پیام'
