from django.conf import settings

from rest_framework import serializers

from .models import (
    Exam,
    ExamBooklet,
    ExamAttempt,
    ExamResult,
    ExamBookletResult,
    ExamAttemptStatus,
)


class ExamBookletSerializer(serializers.ModelSerializer):
    end_question = serializers.IntegerField(
        read_only=True
    )

    question_range = serializers.SerializerMethodField()

    class Meta:
        model = ExamBooklet

        fields = [
            "id",
            "title",
            "subject",
            "order",
            "factor",
            "start_question",
            "question_count",
            "end_question",
            "question_range",
        ]

    def get_question_range(self, obj):
        if obj.question_count <= 0:
            return ""

        return (
            f"{obj.start_question} تا "
            f"{obj.end_question}"
        )


class ExamListSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(
        source="get_category_display",
        read_only=True,
    )

    status = serializers.SerializerMethodField()

    questions_pdf_url = serializers.SerializerMethodField()
    answer_pdf_url = serializers.SerializerMethodField()

    has_attempt = serializers.SerializerMethodField()
    attempt_id = serializers.SerializerMethodField()
    attempt_status = serializers.SerializerMethodField()

    result_available = serializers.SerializerMethodField()
    can_start = serializers.SerializerMethodField()

    booklets = ExamBookletSerializer(
        many=True,
        read_only=True,
    )

    booklet_count = serializers.SerializerMethodField()

    class Meta:
        model = Exam

        fields = [
            "id",
            "title",
            "description",

            "category",
            "category_label",

            "start_at",
            "end_at",
            "duration_minutes",

            "total_questions",
            "booklet_count",
            "booklets",

            "questions_pdf_url",
            "answer_pdf_url",

            "status",
            "is_active",

            "has_attempt",
            "attempt_id",
            "attempt_status",

            "result_available",
            "can_start",
        ]

    def get_status(self, obj):
        return obj.get_status()

    def get_booklet_count(self, obj):
        return obj.booklets.count()

    def _file_url(
        self,
        obj,
        file_field_name,
        external_url_field_name,
    ):
        external_url = getattr(
            obj,
            external_url_field_name,
            "",
        )

        if external_url:
            return external_url

        file = getattr(
            obj,
            file_field_name,
            None,
        )

        if not file:
            return None

        request = self.context.get(
            "request"
        )

        url = file.url

        return (
            request.build_absolute_uri(url)
            if request
            else url
        )

    def get_questions_pdf_url(self, obj):
        return self._file_url(
            obj,
            "questions_pdf",
            "questions_pdf_url",
        )

    def get_answer_pdf_url(self, obj):
        return self._file_url(
            obj,
            "answer_pdf",
            "answer_pdf_url",
        )

    def get_current_attempt(self, obj):
        attempts = getattr(
            obj,
            "current_user_attempts",
            [],
        )

        return (
            attempts[0]
            if attempts
            else None
        )

    def get_has_attempt(self, obj):
        return (
            self.get_current_attempt(obj)
            is not None
        )

    def get_attempt_id(self, obj):
        attempt = self.get_current_attempt(
            obj
        )

        return (
            attempt.id
            if attempt
            else None
        )

    def get_attempt_status(self, obj):
        attempt = self.get_current_attempt(
            obj
        )

        return (
            attempt.status
            if attempt
            else None
        )

    def get_result_available(self, obj):
        attempt = self.get_current_attempt(
            obj
        )

        if not attempt:
            return False

        return attempt.status in [
            ExamAttemptStatus.SUBMITTED,
            ExamAttemptStatus.EXPIRED,
        ]

    def get_can_start(self, obj):
        attempt = self.get_current_attempt(
            obj
        )

        if attempt:
            return (
                attempt.status
                == ExamAttemptStatus.IN_PROGRESS
            )

        return (
            obj.get_status()
            == "running"
        )


class ExamDetailSerializer(ExamListSerializer):
    class Meta(ExamListSerializer.Meta):
        fields = ExamListSerializer.Meta.fields


class ExamAttemptSerializer(
    serializers.ModelSerializer
):
    exam_title = serializers.CharField(
        source="exam.title",
        read_only=True,
    )

    remaining_seconds = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = ExamAttempt

        fields = [
            "id",
            "exam",
            "exam_title",

            "started_at",
            "expires_at",
            "submitted_at",

            "status",
            "answers",

            "score",
            "raw_score",

            "correct_count",
            "wrong_count",
            "unanswered_count",

            "remaining_seconds",
        ]

        read_only_fields = fields


class SaveAnswersSerializer(
    serializers.Serializer
):
    answers = serializers.DictField(
        child=serializers.IntegerField(
            min_value=1,
            max_value=4,
        ),
        allow_empty=True,
    )


class ExamBookletResultSerializer(
    serializers.ModelSerializer
):
    booklet_title = serializers.CharField(
        source="booklet.title",
        read_only=True,
    )

    subject = serializers.CharField(
        source="booklet.subject",
        read_only=True,
    )

    booklet_order = serializers.IntegerField(
        source="booklet.order",
        read_only=True,
    )

    booklet_factor = serializers.IntegerField(
        source="booklet.factor",
        read_only=True,
    )

    class Meta:
        model = ExamBookletResult

        fields = [
            "id",

            "booklet",
            "booklet_title",
            "subject",
            "booklet_order",
            "booklet_factor",

            "total_questions",
            "correct_count",
            "wrong_count",
            "unanswered_count",

            "score",
            "raw_score",

            "decile",

            "national_rank",
            "national_participants",

            "provincial_rank",
            "provincial_participants",

            "national_average",
            "provincial_average",

            "performance_title",
            "performance_message",
        ]

        read_only_fields = fields


class ExamResultSerializer(
    serializers.ModelSerializer
):
    exam_title = serializers.CharField(
        source="exam.title",
        read_only=True,
    )

    exam_category = serializers.CharField(
        source="exam.category",
        read_only=True,
    )

    exam_category_label = serializers.CharField(
        source="exam.get_category_display",
        read_only=True,
    )

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    user_first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )

    user_last_name = serializers.CharField(
        source="user.last_name",
        read_only=True,
    )

    user_province = serializers.CharField(
        source="user.province",
        read_only=True,
    )

    booklet_results = (
        ExamBookletResultSerializer(
            many=True,
            read_only=True,
        )
    )

    class Meta:
        model = ExamResult

        fields = [
            "id",

            "exam",
            "exam_title",
            "exam_category",
            "exam_category_label",

            "user",
            "username",
            "user_first_name",
            "user_last_name",
            "user_province",

            "is_final",
            "finalized_at",

            "total_questions",
            "correct_count",
            "wrong_count",
            "unanswered_count",

            "score",
            "raw_score",

            "national_rank",
            "national_participants",

            "provincial_rank",
            "provincial_participants",

            "booklet_results",

            "created_at",
            "updated_at",
        ]

        read_only_fields = fields