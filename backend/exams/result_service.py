from decimal import Decimal, ROUND_HALF_UP

from .models import (
    ExamAttempt,
    ExamAttemptStatus,
    ExamBooklet,
    ExamResult,
    ExamBookletResult,
)


NEGATIVE_MARKING_DENOMINATOR = Decimal("3")


def to_decimal(value):
    return Decimal(
        str(value or 0)
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def get_answer(data, question_number):
    if not isinstance(data, dict):
        return None

    value = data.get(str(question_number))

    if value is None:
        value = data.get(question_number)

    if value in (None, "", 0, "0"):
        return None

    try:
        value = int(value)
    except (TypeError, ValueError):
        return None

    return value if value in (1, 2, 3, 4) else None


def negative_percentage(correct, wrong, total):
    """
    درصد با نمره منفی:

    (3 * درست - غلط)
    ---------------- × 100
         3 * کل
    """

    if total <= 0:
        return Decimal("0.00")

    value = (
        (
            Decimal(correct)
            * NEGATIVE_MARKING_DENOMINATOR
            - Decimal(wrong)
        )
        / (
            Decimal(total)
            * NEGATIVE_MARKING_DENOMINATOR
        )
        * Decimal("100")
    )

    return to_decimal(value)


def raw_percentage(correct, total):
    """
    درصد خام بدون نمره منفی.
    """

    if total <= 0:
        return Decimal("0.00")

    return to_decimal(
        Decimal(correct)
        / Decimal(total)
        * Decimal("100")
    )


def calculate_counts(
    *,
    answers,
    answer_key,
    start,
    end,
):
    correct = 0
    wrong = 0
    unanswered = 0

    for q in range(start, end + 1):
        user_answer = get_answer(
            answers,
            q,
        )

        correct_answer = get_answer(
            answer_key,
            q,
        )

        if user_answer is None:
            unanswered += 1

        elif (
            correct_answer is not None
            and user_answer == correct_answer
        ):
            correct += 1

        else:
            wrong += 1

    total = (
        correct
        + wrong
        + unanswered
    )

    return {
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "unanswered": unanswered,
        "score": negative_percentage(
            correct,
            wrong,
            total,
        ),
        "raw_score": raw_percentage(
            correct,
            total,
        ),
    }


def calculate_attempt_stats(attempt):
    """
    درصد ساده کل آزمون.

    برای سازگاری با بخش‌های قدیمی پروژه نگه داشته شده است.

    برای درصد رسمی آزمون‌های چنددفترچه‌ای،
    از calculate_weighted_exam_stats استفاده کنید.
    """

    exam = attempt.exam

    return calculate_counts(
        answers=attempt.answers or {},
        answer_key=exam.answer_key or {},
        start=1,
        end=exam.total_questions,
    )


def calculate_booklet_stats(attempt, booklet):
    return calculate_counts(
        answers=attempt.answers or {},
        answer_key=attempt.exam.answer_key or {},
        start=booklet.start_question,
        end=booklet.end_question,
    )


def calculate_weighted_exam_stats(attempt, booklets=None):
    """
    محاسبه رسمی درصد کل آزمون بر اساس ضریب دفترچه‌ها.

    درصد هر دفترچه:

        (3 * correct - wrong)
        --------------------- * 100
              3 * total

    درصد کل:

        SUM(booklet_percentage * booklet_factor)
        ----------------------------------------
                  SUM(booklet_factor)

    بنابراین رتبه‌بندی کلی آزمون نیز بر اساس همین
    درصد کل ضریب‌دار انجام می‌شود.
    """

    if booklets is None:
        booklets = list(
            attempt.exam.booklets.all().order_by("order")
        )

    weighted_score_sum = Decimal("0.00")
    weighted_raw_sum = Decimal("0.00")
    total_factor = Decimal("0.00")

    total = 0
    correct = 0
    wrong = 0
    unanswered = 0

    booklet_stats = []

    for booklet in booklets:
        stats = calculate_booklet_stats(
            attempt,
            booklet,
        )

        factor = Decimal(
            str(booklet.factor or 0)
        )

        # دفترچه بدون ضریب معتبر
        # در محاسبه درصد کل شرکت نمی‌کند.
        if factor <= 0:
            continue

        weighted_score_sum += (
            stats["score"] * factor
        )

        weighted_raw_sum += (
            stats["raw_score"] * factor
        )

        total_factor += factor

        total += stats["total"]
        correct += stats["correct"]
        wrong += stats["wrong"]
        unanswered += stats["unanswered"]

        booklet_stats.append(
            {
                "booklet": booklet,
                "stats": stats,
                "factor": factor,
            }
        )

    if total_factor <= 0:
        overall_score = Decimal("0.00")
        overall_raw_score = Decimal("0.00")

    else:
        overall_score = to_decimal(
            weighted_score_sum / total_factor
        )

        overall_raw_score = to_decimal(
            weighted_raw_sum / total_factor
        )

    return {
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "unanswered": unanswered,
        "score": overall_score,
        "raw_score": overall_raw_score,
        "booklet_stats": booklet_stats,
        "total_factor": total_factor,
    }


# برای سازگاری با هر بخشی از پروژه که قبلاً
# این نام را import کرده باشد.
calculate_weighted_exam_scores = calculate_weighted_exam_stats


def competition_rank(values, target):
    """
    رتبه‌بندی نزولی بر اساس درصد.

    مقدار بالاتر = رتبه بهتر.
    """

    ordered = sorted(
        (
            to_decimal(value)
            for value in values
        ),
        reverse=True,
    )

    target = to_decimal(target)

    for index, value in enumerate(
        ordered,
        start=1,
    ):
        if value <= target:
            return index

    return len(ordered) + 1


def calculate_decile(target, values):
    values = [
        to_decimal(value)
        for value in values
    ]

    if not values:
        return 1

    if len(values) == 1:
        return 10

    below_or_equal = sum(
        1
        for value in values
        if value <= to_decimal(target)
    )

    percentile = (
        Decimal(below_or_equal)
        / Decimal(len(values))
        * Decimal("100")
    )

    decile = int(
        (
            percentile
            + Decimal("9.999999")
        )
        // Decimal("10")
    )

    return max(
        1,
        min(10, decile),
    )


def get_performance_text(score, decile):
    if decile >= 9:
        return (
            "عملکرد درخشان",
            "در این دفترچه عملکرد بسیار خوبی داشتی. همین روند را حفظ کن و برای کاهش خطاهای کوچک و رسیدن به سطح بالاتر تلاش کن.",
        )

    if decile >= 7:
        return (
            "عملکرد خوب",
            "عملکردت بالاتر از بخش قابل‌توجهی از شرکت‌کنندگان قرار گرفته است. با کمی دقت و مرور اشتباهات می‌توانی یک پله دیگر هم بالاتر بروی.",
        )

    if decile >= 5:
        return (
            "یک گام تا بهتر شدن",
            "وضعیتت در محدوده میانی قرار دارد. مرور سوالات غلط و نزده این دفترچه می‌تواند بیشترین کمک را برای آزمون بعدی به تو بکند.",
        )

    if decile >= 3:
        return (
            "جای پیشرفت جدی",
            "این دفترچه فرصت خوبی برای پیشرفت دارد. اشتباهاتت را دسته‌بندی کن، مباحث ضعیف را مرور کن و برای آزمون بعدی یک هدف مشخص تعیین کن.",
        )

    return (
        "نیازمند توجه ویژه",
        "این دفترچه فعلاً یکی از بخش‌های نیازمند تمرکز بیشتر است. نتیجه امروز ثابت نیست؛ با مرور هدفمند و تمرین منظم می‌توانی مسیرت را تغییر بدهی.",
    )


def _profile_image(user, request=None):
    image = getattr(
        user,
        "profile_image",
        None,
    )

    if not image:
        return None

    try:
        url = image.url
    except (AttributeError, ValueError):
        return None

    if request and url.startswith("/"):
        return request.build_absolute_uri(url)

    return url


def _booklet_for_question(booklets, q):
    for booklet in booklets:
        if (
            booklet.start_question
            <= q
            <= booklet.end_question
        ):
            return booklet

    return None


def build_personalized_review(
    attempt,
    booklets,
):
    answers = attempt.answers or {}
    answer_key = attempt.exam.answer_key or {}

    review = []

    for q in range(
        1,
        attempt.exam.total_questions + 1,
    ):
        user_answer = get_answer(
            answers,
            q,
        )

        correct_answer = get_answer(
            answer_key,
            q,
        )

        booklet = _booklet_for_question(
            booklets,
            q,
        )

        if user_answer is None:
            status = "unanswered"

        elif (
            correct_answer is not None
            and user_answer == correct_answer
        ):
            status = "correct"

        else:
            status = "wrong"

        review.append(
            {
                "question_number": q,
                "booklet_id": (
                    booklet.id
                    if booklet
                    else None
                ),
                "booklet_title": (
                    booklet.title
                    if booklet
                    else None
                ),
                "subject": (
                    booklet.subject
                    if booklet
                    else None
                ),
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "status": status,
                "options": [
                    {
                        "value": 1,
                        "selected": user_answer == 1,
                        "correct": correct_answer == 1,
                    },
                    {
                        "value": 2,
                        "selected": user_answer == 2,
                        "correct": correct_answer == 2,
                    },
                    {
                        "value": 3,
                        "selected": user_answer == 3,
                        "correct": correct_answer == 3,
                    },
                    {
                        "value": 4,
                        "selected": user_answer == 4,
                        "correct": correct_answer == 4,
                    },
                ],
            }
        )

    return review


def _completed_attempts(
    exam,
    exclude_id=None,
):
    queryset = (
        ExamAttempt.objects
        .select_related(
            "user",
            "exam",
        )
        .prefetch_related(
            "exam__booklets",
        )
        .filter(
            exam=exam,
            status__in=[
                ExamAttemptStatus.SUBMITTED,
                ExamAttemptStatus.EXPIRED,
            ],
        )
        .order_by(
            "submitted_at",
            "id",
        )
    )

    if exclude_id:
        queryset = queryset.exclude(
            id=exclude_id
        )

    return list(queryset)


def _previous_attempt_for_user(attempt):
    return (
        ExamAttempt.objects
        .select_related("exam")
        .prefetch_related("exam__booklets")
        .filter(
            user=attempt.user,
            status__in=[
                ExamAttemptStatus.SUBMITTED,
                ExamAttemptStatus.EXPIRED,
            ],
            submitted_at__lt=(
                attempt.submitted_at
                if attempt.submitted_at
                else attempt.created_at
            ),
        )
        .exclude(
            id=attempt.id
        )
        .order_by(
            "-submitted_at",
            "-id",
        )
        .first()
    )


def build_exam_result(
    *,
    attempt,
    request=None,
):
    attempt = (
        ExamAttempt.objects
        .select_related(
            "exam",
            "user",
        )
        .prefetch_related(
            "exam__booklets",
        )
        .get(
            id=attempt.id
        )
    )

    exam = attempt.exam

    booklets = list(
        exam.booklets.all().order_by("order")
    )

    result, _ = ExamResult.objects.get_or_create(
        attempt=attempt,
        defaults={
            "user": attempt.user,
            "exam": exam,
            "is_final": False,
        },
    )

    attempts = _completed_attempts(exam)

    if attempt.id not in {
        item.id for item in attempts
    }:
        attempts.append(attempt)

    # =========================================================
    # درصد کل همه شرکت‌کنندگان با ضریب دفترچه‌ها
    # =========================================================

    attempt_stats = {
        item.id: calculate_weighted_exam_stats(
            item,
            list(
                item.exam.booklets.all()
                .order_by("order")
            ),
        )
        for item in attempts
    }

    current = attempt_stats[attempt.id]

    # این مقادیر درصد کل ضریب‌دار هستند.
    country_scores = [
        item["score"]
        for item in attempt_stats.values()
    ]

    province = (
        getattr(
            attempt.user,
            "province",
            "",
        )
        or ""
    ).strip()

    province_scores = [
        attempt_stats[item.id]["score"]
        for item in attempts
        if (
            province
            and (
                getattr(
                    item.user,
                    "province",
                    "",
                )
                or ""
            ).strip()
            == province
        )
    ]

    result.total_questions = current["total"]
    result.correct_count = current["correct"]
    result.wrong_count = current["wrong"]
    result.unanswered_count = current["unanswered"]

    # درصد رسمی = درصد کل ضریب‌دار
    result.score = current["score"]

    # درصد خام = درصد خام کل ضریب‌دار
    result.raw_score = current["raw_score"]

    # رتبه کشوری بر اساس درصد کل ضریب‌دار
    result.national_rank = competition_rank(
        country_scores,
        current["score"],
    )

    result.national_participants = len(
        country_scores
    )

    # رتبه استانی بر اساس درصد کل ضریب‌دار
    result.provincial_rank = (
        competition_rank(
            province_scores,
            current["score"],
        )
        if province_scores
        else None
    )

    result.provincial_participants = len(
        province_scores
    )

    result.user = attempt.user
    result.exam = exam

    result.save()

    booklet_payload = []

    for booklet in booklets:
        stats_by_attempt = {
            item.id: calculate_booklet_stats(
                item,
                booklet,
            )
            for item in attempts
        }

        current_booklet = stats_by_attempt[
            attempt.id
        ]

        # رتبه دفترچه همچنان بر اساس خود همان دفترچه است.
        national_values = [
            item["score"]
            for item in stats_by_attempt.values()
        ]

        province_values = [
            stats_by_attempt[item.id]["score"]
            for item in attempts
            if (
                province
                and (
                    getattr(
                        item.user,
                        "province",
                        "",
                    )
                    or ""
                ).strip()
                == province
            )
        ]

        decile = calculate_decile(
            current_booklet["score"],
            national_values,
        )

        (
            performance_title,
            performance_message,
        ) = get_performance_text(
            current_booklet["score"],
            decile,
        )

        br, _ = ExamBookletResult.objects.get_or_create(
            result=result,
            booklet=booklet,
        )

        br.total_questions = current_booklet[
            "total"
        ]

        br.correct_count = current_booklet[
            "correct"
        ]

        br.wrong_count = current_booklet[
            "wrong"
        ]

        br.unanswered_count = current_booklet[
            "unanswered"
        ]

        br.score = current_booklet["score"]
        br.raw_score = current_booklet[
            "raw_score"
        ]

        br.decile = decile

        br.national_rank = competition_rank(
            national_values,
            current_booklet["score"],
        )

        br.national_participants = len(
            national_values
        )

        br.provincial_rank = (
            competition_rank(
                province_values,
                current_booklet["score"],
            )
            if province_values
            else None
        )

        br.provincial_participants = len(
            province_values
        )

        br.national_average = (
            to_decimal(
                sum(national_values)
                / len(national_values)
            )
            if national_values
            else Decimal("0.00")
        )

        br.provincial_average = (
            to_decimal(
                sum(province_values)
                / len(province_values)
            )
            if province_values
            else Decimal("0.00")
        )

        br.performance_title = (
            performance_title
        )

        br.performance_message = (
            performance_message
        )

        br.save()

        booklet_payload.append(
            {
                "id": booklet.id,
                "title": booklet.title,
                "subject": booklet.subject,
                "order": booklet.order,
                "factor": booklet.factor,
                "start_question": booklet.start_question,
                "end_question": booklet.end_question,
                "question_count": current_booklet[
                    "total"
                ],
                "correct": current_booklet[
                    "correct"
                ],
                "wrong": current_booklet[
                    "wrong"
                ],
                "unanswered": current_booklet[
                    "unanswered"
                ],
                "percentage": float(
                    current_booklet["score"]
                ),
                "score": float(
                    current_booklet["score"]
                ),
                "raw_percentage": float(
                    current_booklet["raw_score"]
                ),
                "raw_score": float(
                    current_booklet["raw_score"]
                ),
                "decile": decile,
                "national_rank": br.national_rank,
                "national_participants": (
                    br.national_participants
                ),
                "provincial_rank": (
                    br.provincial_rank
                ),
                "provincial_participants": (
                    br.provincial_participants
                ),
                "country_average": float(
                    br.national_average
                ),
                "province_average": float(
                    br.provincial_average
                ),
                "national_average": float(
                    br.national_average
                ),
                "provincial_average": float(
                    br.provincial_average
                ),
                "performance_title": (
                    performance_title
                ),
                "performance_message": (
                    performance_message
                ),
            }
        )

    booklet_comparison = [
        {
            "booklet_id": item["id"],
            "booklet_title": item["title"],
            "user_percentage": item[
                "percentage"
            ],
            "user_raw_percentage": item[
                "raw_percentage"
            ],
            "country_average": item[
                "country_average"
            ],
            "province_average": item[
                "province_average"
            ],
        }
        for item in booklet_payload
    ]

    previous_attempt = (
        _previous_attempt_for_user(attempt)
    )

    history = list(
        ExamAttempt.objects
        .select_related("exam")
        .prefetch_related(
            "exam__booklets"
        )
        .filter(
            user=attempt.user,
            status__in=[
                ExamAttemptStatus.SUBMITTED,
                ExamAttemptStatus.EXPIRED,
            ],
        )
        .order_by(
            "submitted_at",
            "id",
        )
    )[-10:]

    progress = []

    for item in history:
        item_booklets = list(
            item.exam.booklets.all()
            .order_by("order")
        )

        stats = calculate_weighted_exam_stats(
            item,
            item_booklets,
        )

        progress.append(
            {
                "attempt_id": item.id,
                "exam_id": item.exam_id,
                "exam_title": item.exam.title,
                "date": (
                    item.submitted_at
                    or item.created_at
                ).isoformat(),
                "percentage": float(
                    stats["score"]
                ),
                "score": float(
                    stats["score"]
                ),
                "raw_percentage": float(
                    stats["raw_score"]
                ),
                "raw_score": float(
                    stats["raw_score"]
                ),
                "correct": stats["correct"],
                "wrong": stats["wrong"],
                "unanswered": stats[
                    "unanswered"
                ],
            }
        )

    previous_data = None

    if previous_attempt:
        previous_booklets = list(
            previous_attempt.exam.booklets.all()
            .order_by("order")
        )

        previous_stats = (
            calculate_weighted_exam_stats(
                previous_attempt,
                previous_booklets,
            )
        )

        previous_data = {
            "attempt_id": previous_attempt.id,
            "exam_id": previous_attempt.exam_id,
            "exam_title": previous_attempt.exam.title,
            "score": float(
                previous_stats["score"]
            ),
            "raw_score": float(
                previous_stats["raw_score"]
            ),
            "correct": previous_stats["correct"],
            "wrong": previous_stats["wrong"],
            "unanswered": previous_stats[
                "unanswered"
            ],
            "score_change": float(
                current["score"]
                - previous_stats["score"]
            ),
            "raw_score_change": float(
                current["raw_score"]
                - previous_stats["raw_score"]
            ),
        }

    return {
        "id": result.id,
        "attempt_id": attempt.id,
        "is_final": result.is_final,
        "finalized_at": result.finalized_at,
        "created_at": result.created_at,
        "updated_at": result.updated_at,

        "exam": {
            "id": exam.id,
            "title": exam.title,
            "description": exam.description,
            "category": exam.category,
            "category_label": (
                exam.get_category_display()
            ),
            "start_at": exam.start_at,
            "end_at": exam.end_at,
            "duration_minutes": (
                exam.duration_minutes
            ),
            "total_questions": (
                exam.total_questions
            ),
            "question_pdf_url": (
                exam.questions_pdf_url
            ),
        },

        "user": {
            "id": attempt.user.id,
            "username": attempt.user.username,
            "first_name": (
                attempt.user.first_name
            ),
            "last_name": (
                attempt.user.last_name
            ),
            "full_name": (
                f"{attempt.user.first_name} "
                f"{attempt.user.last_name}"
            ).strip(),
            "profile_image": _profile_image(
                attempt.user,
                request,
            ),
            "gender": getattr(
                attempt.user,
                "gender",
                "",
            ),
            "grade": getattr(
                attempt.user,
                "grade",
                None,
            ),
            "field": getattr(
                attempt.user,
                "field",
                None,
            ),
            "province": getattr(
                attempt.user,
                "province",
                "",
            ),
            "school": getattr(
                attempt.user,
                "school",
                "",
            ),
        },

        "summary": {
            "total_questions": current[
                "total"
            ],
            "correct_count": current[
                "correct"
            ],
            "wrong_count": current[
                "wrong"
            ],
            "unanswered_count": current[
                "unanswered"
            ],

            # درصد کل ضریب‌دار
            "score": float(
                current["score"]
            ),

            "percentage": float(
                current["score"]
            ),

            # درصد خام کل ضریب‌دار
            "raw_score": float(
                current["raw_score"]
            ),

            "raw_percentage": float(
                current["raw_score"]
            ),

            "negative_marking": True,

            "total_factor": float(
                current["total_factor"]
            ),
        },

        "ranking": {
            "national_rank": (
                result.national_rank
            ),
            "national_participants": (
                result.national_participants
            ),
            "provincial_rank": (
                result.provincial_rank
            ),
            "provincial_participants": (
                result.provincial_participants
            ),
            "province": province or None,
        },

        "booklets": booklet_payload,

        "charts": {
            "booklet_comparison": (
                booklet_comparison
            ),
            "progress": progress,
            "previous_attempt": previous_data,
        },

        "progress": progress,

        "previous_attempt": previous_data,

        "personalized_review": (
            build_personalized_review(
                attempt,
                booklets,
            )
        ),
    }