from django.contrib import admin

from .models import (
    StudyRoom,
    RoomMembership,
    StudySession,
    RoomChatMessage,
    RoomChatMessageEditHistory,
    RoomChatReaction,
)

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
        'status',
        'edited_at',
        'deleted_at',
        'deleted_by',
        'created_at',
    )

    list_filter = (
        'room',
        'is_deleted',
        'edited_at',
        'created_at',
    )

    search_fields = (
        'message',
        'user__username',
        'room__name',
        'deleted_by__username',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
        'edited_at',
        'deleted_at',
    )

    list_select_related = (
        'room',
        'user',
        'deleted_by',
        'reply_to',
    )

    fieldsets = (
        (
            'اطلاعات پیام',
            {
                'fields': (
                    'room',
                    'user',
                    'message',
                    'client_id',
                    'reply_to',
                    'created_at',
                )
            }
        ),

        (
            'ویرایش',
            {
                'fields': (
                    'edited_at',
                )
            }
        ),

        (
            'حذف پیام',
            {
                'fields': (
                    'is_deleted',
                    'deleted_at',
                    'deleted_by',
                )
            }
        ),
    )

    def message_preview(self, obj):

        if obj.is_deleted:
            return '[پیام حذف شده]'

        return obj.message[:70]

    message_preview.short_description = 'پیش‌نمایش پیام'

    def status(self, obj):

        if obj.is_deleted:
            return 'حذف شده'

        if obj.edited_at:
            return 'ویرایش شده'

        return 'عادی'

    status.short_description = 'وضعیت'


@admin.register(RoomChatMessageEditHistory)
class RoomChatMessageEditHistoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'message',
        'edited_by',
        'edited_at',
        'old_message_preview',
    )

    list_filter = (
        'edited_at',
    )

    search_fields = (
        'old_message',
        'edited_by__username',
        'message__message',
    )

    ordering = (
        '-edited_at',
    )

    readonly_fields = (
        'message',
        'old_message',
        'edited_by',
        'edited_at',
    )

    list_select_related = (
        'message',
        'edited_by',
    )

    def old_message_preview(self, obj):

        return obj.old_message[:80]

    old_message_preview.short_description = 'متن قبلی'


@admin.register(RoomChatReaction)
class RoomChatReactionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'message',
        'user',
        'reaction_display',
        'created_at',
    )

    list_filter = (
        'reaction',
        'created_at',
    )

    search_fields = (
        'user__username',
        'message__message',
        'message__room__name',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )

    list_select_related = (
        'message',
        'user',
        'message__room',
    )

    def reaction_display(self, obj):

        return obj.get_reaction_display()

    reaction_display.short_description = 'واکنش'
