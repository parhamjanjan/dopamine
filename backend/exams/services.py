from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import (
    Exam,
    ExamAttempt,
    ExamAttemptStatus,
)

from .result_service import (
    calculate_attempt_stats,
)


class ExamError(Exception):
    pass


def get_exam_status(exam):
    now = timezone.now()

    if not exam.is_active:
        return "inactive"

    if now < exam.start_at:
        return "not_started"

    if now >= exam.end_at:
        return "ended"

    return "running"


@transaction.atomic
def start_exam(*, user, exam_id):
    exam = (
        Exam.objects
        .select_for_update()
        .filter(
            id=exam_id,
            is_active=True,
        )
        .first()
    )

    if not exam:
        raise ExamError(
            "آزمون موردنظر پیدا نشد."
        )

    now = timezone.now()

    if now < exam.start_at:
        raise ExamError(
            "زمان شروع این آزمون هنوز نرسیده است."
        )

    if now >= exam.end_at:
        raise ExamError(
            "زمان شرکت در این آزمون به پایان رسیده است."
        )

    existing = (
        ExamAttempt.objects
        .filter(
            user=user,
            exam=exam,
        )
        .first()
    )

    if existing:
        if (
            existing.status
            == ExamAttemptStatus.IN_PROGRESS
        ):
            if (
                timezone.now()
                < existing.expires_at
            ):
                return existing

            existing.status = (
                ExamAttemptStatus.EXPIRED
            )

            existing.submitted_at = (
                timezone.now()
            )

            existing.save(
                update_fields=[
                    "status",
                    "submitted_at",
                    "updated_at",
                ]
            )

            raise ExamError(
                "زمان این آزمون برای شما به پایان رسیده است."
            )

        raise ExamError(
            "شما قبلاً در این آزمون شرکت کرده‌اید."
        )

    duration_end = (
        now
        + timedelta(
            minutes=exam.duration_minutes
        )
    )

    real_expires_at = min(
        duration_end,
        exam.end_at,
    )

    return ExamAttempt.objects.create(
        user=user,
        exam=exam,
        expires_at=real_expires_at,
        answers={},
        status=ExamAttemptStatus.IN_PROGRESS,
    )


def normalize_answers(
    answers,
    total_questions,
):
    if not isinstance(answers, dict):
        raise ExamError(
            "فرمت پاسخ‌ها نامعتبر است."
        )

    normalized = {}

    for question_number, answer in (
        answers.items()
    ):
        try:
            question_number = int(
                question_number
            )
        except (TypeError, ValueError):
            continue

        if not (
            1
            <= question_number
            <= total_questions
        ):
            continue

        if answer in (
            None,
            "",
            0,
            "0",
        ):
            continue

        try:
            answer = int(answer)
        except (TypeError, ValueError):
            continue

        if answer not in {
            1,
            2,
            3,
            4,
        }:
            continue

        normalized[
            str(question_number)
        ] = answer

    return normalized


@transaction.atomic
def save_attempt_answers(
    *,
    user,
    attempt_id,
    answers,
):
    attempt = (
        ExamAttempt.objects
        .select_for_update()
        .select_related("exam")
        .filter(
            id=attempt_id,
            user=user,
        )
        .first()
    )

    if not attempt:
        raise ExamError(
            "آزمون شما پیدا نشد."
        )

    if (
        attempt.status
        != ExamAttemptStatus.IN_PROGRESS
    ):
        raise ExamError(
            "این آزمون دیگر در حال اجرا نیست."
        )

    now = timezone.now()

    if now >= attempt.expires_at:
        attempt.status = (
            ExamAttemptStatus.EXPIRED
        )

        attempt.submitted_at = now

        attempt.save(
            update_fields=[
                "status",
                "submitted_at",
                "updated_at",
            ]
        )

        raise ExamError(
            "زمان آزمون به پایان رسیده است."
        )

    attempt.answers = normalize_answers(
        answers,
        attempt.exam.total_questions,
    )

    attempt.save(
        update_fields=[
            "answers",
            "updated_at",
        ]
    )

    return attempt


@transaction.atomic
def submit_attempt(
    *,
    user,
    attempt_id,
    answers=None,
    force_expired=False,
):
    attempt = (
        ExamAttempt.objects
        .select_for_update()
        .select_related("exam")
        .prefetch_related("exam__booklets")
        .filter(
            id=attempt_id,
            user=user,
        )
        .first()
    )

    if not attempt:
        raise ExamError(
            "آزمون شما پیدا نشد."
        )

    if (
        attempt.status
        != ExamAttemptStatus.IN_PROGRESS
    ):
        return attempt

    now = timezone.now()

    if answers is not None:
        attempt.answers = normalize_answers(
            answers,
            attempt.exam.total_questions,
        )

    attempt.status = (
        ExamAttemptStatus.EXPIRED
        if (
            now >= attempt.expires_at
            or force_expired
        )
        else ExamAttemptStatus.SUBMITTED
    )

    # ---------------------------------------------------------
    # آمار مستقیم کل سوالات
    # ---------------------------------------------------------

    stats = calculate_attempt_stats(
        attempt
    )

    # ---------------------------------------------------------
    # درصد کل وزنی دفترچه‌ها
    # ---------------------------------------------------------

    booklets = list(
        attempt.exam.booklets.all()
        .order_by("order")
    )

    weighted = (
        calculate_weighted_exam_scores(
            attempt,
            booklets,
        )
    )

    attempt.correct_count = stats[
        "correct"
    ]

    attempt.wrong_count = stats[
        "wrong"
    ]

    attempt.unanswered_count = stats[
        "unanswered"
    ]

    # درصد رسمی کل آزمون
    attempt.score = weighted[
        "score"
    ]

    # درصد خام کل آزمون
    attempt.raw_score = weighted[
        "raw_score"
    ]

    attempt.submitted_at = now

    attempt.save(
        update_fields=[
            "answers",
            "status",
            "correct_count",
            "wrong_count",
            "unanswered_count",
            "score",
            "raw_score",
            "submitted_at",
            "updated_at",
        ]
    )

    # نتیجه نهایی بعداً توسط finalize_exam
    # یا build_exam_result ساخته/به‌روزرسانی می‌شود.

    return attempt