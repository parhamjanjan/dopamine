from django.conf import settings
from django.db import models
from django.db.models import Q


class StudyRoom(models.Model):
    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True,
        default=''
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_study_rooms'
    )

    max_members = models.PositiveIntegerField(
        default=20
    )

    is_private = models.BooleanField(
        default=False
    )

    join_code = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class RoomMembership(models.Model):
    room = models.ForeignKey(
        StudyRoom,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_room_memberships'
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        constraints = [
            # هر کاربر در هر سالن فقط یک رکورد عضویت دارد
            models.UniqueConstraint(
                fields=['room', 'user'],
                name='unique_room_membership'
            ),

            # هر کاربر در کل سیستم فقط یک عضویت فعال دارد
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(is_active=True),
                name='unique_active_room_per_user'
            ),
        ]

        ordering = ['joined_at']

    def __str__(self):
        return f'{self.user} - {self.room}'


class StudySession(models.Model):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'فعال'
        COMPLETED = 'completed', 'تمام شده'
        INTERRUPTED = 'interrupted', 'متوقف شده'

    class StudyState(models.TextChoices):
        FOCUSED = 'focused', 'متمرکز'
        DISTRACTED = 'distracted', 'حواس پرت'
        AWAY = 'away', 'غایب'

    membership = models.ForeignKey(
        RoomMembership,
        on_delete=models.CASCADE,
        related_name='study_sessions'
    )

    started_at = models.DateTimeField()

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # فقط زمانی که وضعیت focused باشد
    # زمان مطالعه معتبر افزایش پیدا می‌کند.
    valid_study_seconds = models.PositiveIntegerField(
        default=0
    )

    # وضعیت فعلی تشخیص داده شده توسط Frontend
    current_state = models.CharField(
        max_length=20,
        choices=StudyState.choices,
        default=StudyState.AWAY
    )

    # وضعیت خود Session
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    # آخرین heartbeat دریافت شده از Frontend
    last_heartbeat_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return (
            f'{self.membership.user} - '
            f'{self.membership.room} - '
            f'{self.status}'
        )

class StudyTimeLog(models.Model):
    class StudyState(models.TextChoices):
        FOCUSED = 'focused', 'متمرکز'
        DISTRACTED = 'distracted', 'حواس پرت'
        AWAY = 'away', 'غایب'

    session = models.ForeignKey(
        StudySession,
        on_delete=models.CASCADE,
        related_name='time_logs'
    )

    state = models.CharField(
        max_length=20,
        choices=StudyState.choices
    )

    started_at = models.DateTimeField()

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    duration_seconds = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['started_at']

    def __str__(self):
        return (
            f'{self.session.membership.user} - '
            f'{self.state} - '
            f'{self.duration_seconds}s'
        )

class RoomChatMessage(models.Model):

    room = models.ForeignKey(
        StudyRoom,
        on_delete=models.CASCADE,
        related_name='chat_messages',
        verbose_name='سالن'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='room_chat_messages',
        verbose_name='کاربر'
    )

    message = models.TextField(
        max_length=1000,
        verbose_name='پیام'
    )

    client_id = models.CharField(
        max_length=100,
        blank=True,
        default='',
        db_index=True,
        verbose_name='شناسه کلاینت'
    )

    # -----------------------------------------
    # Reply
    # -----------------------------------------

    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='پاسخ به پیام'
    )

    # -----------------------------------------
    # Edit
    # -----------------------------------------

    edited_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='زمان آخرین ویرایش'
    )

    # -----------------------------------------
    # Soft Delete
    # -----------------------------------------

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='حذف شده'
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='زمان حذف'
    )

    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_room_chat_messages',
        verbose_name='حذف شده توسط'
    )

    # -----------------------------------------
    # Created
    # -----------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ارسال'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'پیام چت سالن'
        verbose_name_plural = 'پیام‌های چت سالن'

    def __str__(self):

        if self.is_deleted:
            text = '[پیام حذف شده]'
        else:
            text = self.message[:40]

        return (
            f'{self.user.username} - '
            f'{self.room.name} - '
            f'{text}'
        )


class RoomChatMessageEditHistory(models.Model):

    message = models.ForeignKey(
        RoomChatMessage,
        on_delete=models.CASCADE,
        related_name='edit_history',
        verbose_name='پیام'
    )

    old_message = models.TextField(
        max_length=1000,
        verbose_name='متن قبل از ویرایش'
    )

    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='room_chat_message_edits',
        verbose_name='ویرایش شده توسط'
    )

    edited_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ویرایش'
    )

    class Meta:
        ordering = ['-edited_at']
        verbose_name = 'سابقه ویرایش پیام'
        verbose_name_plural = 'سوابق ویرایش پیام‌ها'

    def __str__(self):

        return (
            f'{self.message_id} - '
            f'{self.edited_by}'
        )


class RoomChatReaction(models.Model):

    class ReactionType(models.TextChoices):

        CRY = 'cry', 'گریه'

        LAUGH = 'laugh', 'خنده'

        HEART = 'heart', 'قلب'

        LIKE = 'like', 'لایک'

        DISLIKE = 'dislike', 'دیسلایک'

    message = models.ForeignKey(
        RoomChatMessage,
        on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name='پیام'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='room_chat_reactions',
        verbose_name='کاربر'
    )

    reaction = models.CharField(
        max_length=20,
        choices=ReactionType.choices,
        verbose_name='واکنش'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان واکنش'
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'message',
                    'user',
                ],
                name='unique_chat_message_user_reaction'
            )
        ]

        ordering = ['created_at']

        verbose_name = 'واکنش پیام'
        verbose_name_plural = 'واکنش‌های پیام'

    def __str__(self):

        return (
            f'{self.user.username} - '
            f'{self.message_id} - '
            f'{self.get_reaction_display()}'
        )