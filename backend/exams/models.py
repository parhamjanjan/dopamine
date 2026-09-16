from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class ExamCategory(models.TextChoices):
    MAZ = "maz", "ماز"
    KANOON = "kanoon", "قلمچی"
    KHEILISABZ = "kheilisabz", "خیلی سبز"
    DOPAMINE = "dopamine", "دوپامین"
    OTHER = "other", "سایر"


class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    category = models.CharField(
        max_length=30,
        choices=ExamCategory.choices,
        default=ExamCategory.DOPAMINE,
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()

    questions_pdf = models.FileField(
        upload_to="exams/questions/",
        blank=True,
        null=True,
    )
    answer_pdf = models.FileField(
        upload_to="exams/answers/",
        blank=True,
        null=True,
    )

    answer_key = models.JSONField(default=dict, blank=True)
    total_questions = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_at"]
        indexes = [
            models.Index(fields=["start_at", "end_at", "is_active"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        if self.start_at and self.end_at and self.end_at <= self.start_at:
            raise ValidationError("زمان پایان آزمون باید بعد از زمان شروع باشد.")
        if self.duration_minutes is not None and self.duration_minutes <= 0:
            raise ValidationError("مدت آزمون باید بیشتر از صفر باشد.")

    @property
    def now(self):
        return timezone.now()

    @property
    def is_before_start(self):
        return timezone.now() < self.start_at

    @property
    def is_after_end(self):
        return timezone.now() >= self.end_at

    @property
    def is_running(self):
        now = timezone.now()
        return self.is_active and self.start_at <= now < self.end_at

    def get_status(self):
        if not self.is_active:
            return "inactive"
        now = timezone.now()
        if now < self.start_at:
            return "not_started"
        if now >= self.end_at:
            return "ended"
        return "running"


class ExamBooklet(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="booklets",
    )
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1)
    start_question = models.PositiveIntegerField(default=1)
    question_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["exam", "order"],
                name="unique_exam_booklet_order",
            )
        ]

    def __str__(self):
        return f"{self.exam.title} - {self.title}"

    @property
    def end_question(self):
        if self.question_count <= 0:
            return self.start_question - 1
        return self.start_question + self.question_count - 1

    def clean(self):
        if self.order < 1:
            raise ValidationError("شماره دفترچه باید حداقل ۱ باشد.")
        if self.start_question < 1:
            raise ValidationError("شماره شروع سوال باید حداقل ۱ باشد.")
        if self.question_count < 1:
            raise ValidationError("تعداد سوالات دفترچه باید بیشتر از صفر باشد.")


class ExamAttemptStatus(models.TextChoices):
    IN_PROGRESS = "in_progress", "در حال آزمون"
    SUBMITTED = "submitted", "ثبت شده"
    EXPIRED = "expired", "منقضی شده"


class ExamAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exam_attempts",
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="attempts",
    )

    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    submitted_at = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=ExamAttemptStatus.choices,
        default=ExamAttemptStatus.IN_PROGRESS,
    )

    answers = models.JSONField(default=dict, blank=True)

    # درصد رسمی با نمره منفی: (3*درست - غلط) / (3*کل) * 100
    score = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # درصد خام بدون نمره منفی: درست / کل * 100
    raw_score = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    correct_count = models.PositiveIntegerField(default=0)
    wrong_count = models.PositiveIntegerField(default=0)
    unanswered_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "exam"],
                name="unique_exam_attempt_per_user",
            )
        ]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["exam", "status"]),
            models.Index(fields=["expires_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.exam.title}"

    @property
    def is_expired(self):
        return (
            self.status == ExamAttemptStatus.IN_PROGRESS
            and timezone.now() >= self.expires_at
        )

    @property
    def remaining_seconds(self):
        if self.status != ExamAttemptStatus.IN_PROGRESS:
            return 0
        return max(0, int((self.expires_at - timezone.now()).total_seconds()))

    def save(self, *args, **kwargs):
        if self.started_at and self.expires_at and self.expires_at <= self.started_at:
            raise ValidationError("زمان انقضای آزمون نامعتبر است.")
        super().save(*args, **kwargs)


class ExamResult(models.Model):
    attempt = models.OneToOneField(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name="result",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exam_results",
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="results",
    )

    is_final = models.BooleanField(default=False)
    finalized_at = models.DateTimeField(null=True, blank=True)

    total_questions = models.PositiveIntegerField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    wrong_count = models.PositiveIntegerField(default=0)
    unanswered_count = models.PositiveIntegerField(default=0)

    score = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    raw_score = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    national_rank = models.PositiveIntegerField(null=True, blank=True)
    national_participants = models.PositiveIntegerField(default=0)
    provincial_rank = models.PositiveIntegerField(null=True, blank=True)
    provincial_participants = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["exam", "is_final"]),
            models.Index(fields=["user", "exam"]),
            models.Index(fields=["exam", "national_rank"]),
            models.Index(fields=["exam", "provincial_rank"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.exam.title} - کارنامه"


class ExamBookletResult(models.Model):
    result = models.ForeignKey(
        ExamResult,
        on_delete=models.CASCADE,
        related_name="booklet_results",
    )
    booklet = models.ForeignKey(
        ExamBooklet,
        on_delete=models.CASCADE,
        related_name="results",
    )

    total_questions = models.PositiveIntegerField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    wrong_count = models.PositiveIntegerField(default=0)
    unanswered_count = models.PositiveIntegerField(default=0)

    score = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    raw_score = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    decile = models.PositiveSmallIntegerField(null=True, blank=True)

    national_rank = models.PositiveIntegerField(null=True, blank=True)
    national_participants = models.PositiveIntegerField(default=0)
    provincial_rank = models.PositiveIntegerField(null=True, blank=True)
    provincial_participants = models.PositiveIntegerField(default=0)

    national_average = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    provincial_average = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    performance_title = models.CharField(max_length=100, blank=True, default="")
    performance_message = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["result", "booklet"],
                name="unique_result_booklet",
            )
        ]
        indexes = [
            models.Index(fields=["booklet", "score"]),
            models.Index(fields=["booklet", "national_rank"]),
            models.Index(fields=["booklet", "provincial_rank"]),
        ]

    def __str__(self):
        return f"{self.result.user.username} - {self.booklet.title}"
