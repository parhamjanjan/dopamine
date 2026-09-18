from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from .models import (
    Exam,
    ExamAttempt,
    ExamAttemptStatus,
    ExamResult,
    ExamBookletResult,
)

from .result_service import (
    calculate_attempt_stats,
    competition_rank,
    calculate_decile,
    get_performance_text,
)


@transaction.atomic
def finalize_exam(exam_id):
    exam = (
        Exam.objects
        .select_for_update()
        .get(id=exam_id)
    )

    booklets = list(
        exam.booklets.all().order_by("order")
    )

    attempts = list(
        ExamAttempt.objects
        .select_related("user", "exam")
        .filter(
            exam=exam,
            status__in=[
                ExamAttemptStatus.SUBMITTED,
                ExamAttemptStatus.EXPIRED,
            ],
        )
        .order_by("id")
    )

    if not attempts:
        return {
            "exam": exam,
            "participants": 0,
            "results_created": 0,
            "results_updated": 0,
        }

    # ---------------------------------------------------------
    # محاسبه تمام آمار از صفر
    # ---------------------------------------------------------

    attempt_data = {}

    for attempt in attempts:
        direct_stats = calculate_attempt_stats(
            attempt
        )

        weighted_stats = (
            calculate_weighted_exam_scores(
                attempt,
                booklets,
            )
        )

        attempt_data[attempt.id] = {
            "attempt": attempt,
            "stats": direct_stats,
            "weighted": weighted_stats,
        }

    # ---------------------------------------------------------
    # درصد کل وزنی تمام شرکت‌کنندگان
    # این مقادیر مبنای رتبه کشوری هستند.
    # ---------------------------------------------------------

    overall_scores = [
        data["weighted"]["score"]
        for data in attempt_data.values()
    ]

    overall_scores_sorted = sorted(
        overall_scores,
        reverse=True,
    )

    now = timezone.now()

    results_created = 0
    results_updated = 0

    # ---------------------------------------------------------
    # ساخت / به‌روزرسانی کارنامه هر شرکت‌کننده
    # ---------------------------------------------------------

    for attempt in attempts:
        data = attempt_data[attempt.id]

        stats = data["stats"]
        weighted = data["weighted"]

        # -----------------------------------------------------
        # Attempt از صفر آپدیت می‌شود
        # -----------------------------------------------------

        attempt.score = weighted["score"]
        attempt.raw_score = weighted["raw_score"]

        attempt.correct_count = stats[
            "correct"
        ]

        attempt.wrong_count = stats[
            "wrong"
        ]

        attempt.unanswered_count = stats[
            "unanswered"
        ]

        attempt.save(
            update_fields=[
                "score",
                "raw_score",
                "correct_count",
                "wrong_count",
                "unanswered_count",
                "updated_at",
            ]
        )

        # -----------------------------------------------------
        # رتبه کشوری بر اساس درصد وزنی
        # -----------------------------------------------------

        national_rank = competition_rank(
            overall_scores_sorted,
            weighted["score"],
        )

        # -----------------------------------------------------
        # رتبه استانی بر اساس درصد وزنی
        # -----------------------------------------------------

        province = (
            getattr(
                attempt.user,
                "province",
                "",
            )
            or ""
        ).strip()

        province_scores = [
            other["weighted"]["score"]
            for other in attempt_data.values()
            if (
                province
                and (
                    getattr(
                        other["attempt"].user,
                        "province",
                        "",
                    )
                    or ""
                ).strip()
                == province
            )
        ]

        provincial_rank = (
            competition_rank(
                province_scores,
                weighted["score"],
            )
            if province_scores
            else None
        )

        # -----------------------------------------------------
        # ExamResult
        # -----------------------------------------------------

        result, created = (
            ExamResult.objects.get_or_create(
                attempt=attempt,
                defaults={
                    "user": attempt.user,
                    "exam": exam,
                },
            )
        )

        if created:
            results_created += 1
        else:
            results_updated += 1

        result.user = attempt.user
        result.exam = exam

        result.is_final = True
        result.finalized_at = now

        result.total_questions = stats[
            "total"
        ]

        result.correct_count = stats[
            "correct"
        ]

        result.wrong_count = stats[
            "wrong"
        ]

        result.unanswered_count = stats[
            "unanswered"
        ]

        # درصد کل وزنی
        result.score = weighted["score"]

        # درصد خام کل وزنی
        result.raw_score = weighted[
            "raw_score"
        ]

        result.national_rank = national_rank
        result.national_participants = len(
            overall_scores
        )

        result.provincial_rank = (
            provincial_rank
        )

        result.provincial_participants = len(
            province_scores
        )

        result.save()

        # -----------------------------------------------------
        # نتایج قبلی دفترچه‌ها حذف می‌شوند
        # تا همه‌چیز از صفر ساخته شود.
        # -----------------------------------------------------

        result.booklet_results.all().delete()

        # -----------------------------------------------------
        # ساخت نتایج دفترچه‌ها
        # -----------------------------------------------------

        for booklet in booklets:
            booklet_stats = weighted[
                "booklets"
            ][booklet.id]

            national_values = [
                other["weighted"]["booklets"][
                    booklet.id
                ]["score"]
                for other in attempt_data.values()
            ]

            province_values = [
                other["weighted"]["booklets"][
                    booklet.id
                ]["score"]
                for other in attempt_data.values()
                if (
                    province
                    and (
                        getattr(
                            other["attempt"].user,
                            "province",
                            "",
                        )
                        or ""
                    ).strip()
                    == province
                )
            ]

            current_score = booklet_stats[
                "score"
            ]

            decile = calculate_decile(
                current_score,
                national_values,
            )

            (
                performance_title,
                performance_message,
            ) = get_performance_text(
                current_score,
                decile,
            )

            national_average = (
                sum(national_values)
                / len(national_values)
                if national_values
                else Decimal("0.00")
            )

            provincial_average = (
                sum(province_values)
                / len(province_values)
                if province_values
                else Decimal("0.00")
            )

            ExamBookletResult.objects.create(
                result=result,
                booklet=booklet,

                total_questions=(
                    booklet_stats["total"]
                ),

                correct_count=(
                    booklet_stats["correct"]
                ),

                wrong_count=(
                    booklet_stats["wrong"]
                ),

                unanswered_count=(
                    booklet_stats["unanswered"]
                ),

                score=current_score,

                raw_score=(
                    booklet_stats["raw_score"]
                ),

                decile=decile,

                national_rank=(
                    competition_rank(
                        national_values,
                        current_score,
                    )
                ),

                national_participants=len(
                    national_values
                ),

                provincial_rank=(
                    competition_rank(
                        province_values,
                        current_score,
                    )
                    if province_values
                    else None
                ),

                provincial_participants=len(
                    province_values
                ),

                national_average=(
                    national_average
                ),

                provincial_average=(
                    provincial_average
                ),

                performance_title=(
                    performance_title
                ),

                performance_message=(
                    performance_message
                ),
            )

    return {
        "exam": exam,
        "participants": len(attempts),
        "results_created": results_created,
        "results_updated": results_updated,
    }