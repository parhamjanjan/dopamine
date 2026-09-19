from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import Prefetch

from .models import Exam, ExamAttempt, ExamAttemptStatus
from .serializers import (
    ExamListSerializer,
    ExamDetailSerializer,
    ExamAttemptSerializer,
    SaveAnswersSerializer,
)
from .services import (
    ExamError,
    start_exam,
    save_attempt_answers,
    submit_attempt,
)
from .result_service import build_exam_result


class ExamListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExamListSerializer

    def get_queryset(self):
        user_attempts = ExamAttempt.objects.filter(
            user=self.request.user
        )

        return (
            Exam.objects
            .filter(is_active=True)
            .prefetch_related(
                "booklets",
                Prefetch(
                    "attempts",
                    queryset=user_attempts,
                    to_attr="current_user_attempts",
                ),
            )
            .order_by("start_at")
        )


class ExamDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExamDetailSerializer

    def get_queryset(self):
        user_attempts = ExamAttempt.objects.filter(
            user=self.request.user
        )

        return (
            Exam.objects
            .filter(is_active=True)
            .prefetch_related(
                "booklets",
                Prefetch(
                    "attempts",
                    queryset=user_attempts,
                    to_attr="current_user_attempts",
                ),
            )
        )


class StartExamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, exam_id):
        try:
            attempt = start_exam(
                user=request.user,
                exam_id=exam_id,
            )

            serializer = ExamAttemptSerializer(attempt)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        except ExamError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as error:
            return Response(
                {
                    "detail": "خطایی هنگام شروع آزمون رخ داد.",
                    "error": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AttemptDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExamAttemptSerializer

    def get_queryset(self):
        return (
            ExamAttempt.objects
            .select_related("exam", "user")
            .filter(user=self.request.user)
        )

    def retrieve(self, request, *args, **kwargs):
        attempt = self.get_object()

        # اگر آزمون در حال اجرا باشد ولی زمان آن تمام شده باشد،
        # وضعیت آن به منقضی‌شده تغییر می‌کند.
        if (
            attempt.status == ExamAttemptStatus.IN_PROGRESS
            and attempt.is_expired
        ):
            attempt.status = ExamAttemptStatus.EXPIRED
            attempt.submitted_at = attempt.expires_at

            attempt.save(
                update_fields=[
                    "status",
                    "submitted_at",
                    "updated_at",
                ]
            )

        serializer = self.get_serializer(attempt)

        return Response(serializer.data)


class AttemptAnswersView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, attempt_id):
        serializer = SaveAnswersSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:
            attempt = save_attempt_answers(
                user=request.user,
                attempt_id=attempt_id,
                answers=serializer.validated_data["answers"],
            )

            return Response(
                ExamAttemptSerializer(attempt).data,
                status=status.HTTP_200_OK,
            )

        except ExamError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as error:
            return Response(
                {
                    "detail": "خطایی هنگام ذخیره پاسخ‌ها رخ داد.",
                    "error": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SubmitExamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, attempt_id):
        answers = request.data.get("answers")

        force_expired = bool(
            request.data.get("force_expired", False)
        )

        try:
            attempt = submit_attempt(
                user=request.user,
                attempt_id=attempt_id,
                answers=answers,
                force_expired=force_expired,
            )

            return Response(
                ExamAttemptSerializer(attempt).data,
                status=status.HTTP_200_OK,
            )

        except ExamError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as error:
            return Response(
                {
                    "detail": "خطایی هنگام ثبت نهایی آزمون رخ داد.",
                    "error": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExamResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        attempt = (
            ExamAttempt.objects
            .select_related("exam", "user")
            .prefetch_related("exam__booklets")
            .filter(
                id=pk,
                user=request.user,
            )
            .first()
        )

        if not attempt:
            return Response(
                {"detail": "آزمون موردنظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if attempt.status not in [
            ExamAttemptStatus.SUBMITTED,
            ExamAttemptStatus.EXPIRED,
        ]:
            return Response(
                {
                    "detail": "کارنامه این آزمون هنوز قابل مشاهده نیست."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = build_exam_result(
                attempt=attempt,
                request=request,
            )

            return Response(
                result,
                status=status.HTTP_200_OK,
            )

        except Exception as error:
            return Response(
                {
                    "detail": "خطایی هنگام ساخت کارنامه رخ داد.",
                    "error": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )