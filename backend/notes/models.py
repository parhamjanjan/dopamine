import uuid
from django.conf import settings
from django.db import models

class Note(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [(DRAFT, 'پیش‌نویس'), (PUBLISHED, 'منتشرشده')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=220, verbose_name='عنوان')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='زیرعنوان')
    subject = models.CharField(max_length=80, blank=True, db_index=True, verbose_name='درس')
    grade = models.CharField(max_length=40, blank=True, db_index=True, verbose_name='پایه')
    cover_color = models.CharField(max_length=7, default='#7055e8')
    cover_icon = models.CharField(max_length=20, default='📘')
    estimated_minutes = models.PositiveSmallIntegerField(default=10)
    tags = models.JSONField(default=list, blank=True)
    chapters = models.JSONField(default=list, blank=True)
    blocks = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=DRAFT, db_index=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at', '-updated_at']
        indexes = [models.Index(fields=['status', 'subject', 'grade'])]

    def __str__(self):
        return self.title

class NoteBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='note_bookmarks')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'note'], name='unique_note_bookmark')]

class NoteProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='note_progress')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='progress_records')
    completed_blocks = models.JSONField(default=list, blank=True)
    last_block = models.PositiveIntegerField(default=0)
    percent = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'note'], name='unique_note_progress')]

class NoteRevision(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='revisions')
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    snapshot = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
