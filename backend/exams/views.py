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
        user_attempts = ExamAttempt.objects.filter(user=self.request.user)
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
    queryset = Exam.objects.filter(is_active=True).prefetch_related("booklets")


class StartExamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, exam_id):
        try:
            attempt = start_exam(user=request.user, exam_id=exam_id)
        except ExamError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            ExamAttemptSerializer(attempt, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
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


class AttemptAnswersView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, attempt_id):
        serializer = SaveAnswersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            attempt = save_attempt_answers(
                user=request.user,
                attempt_id=attempt_id,
                answers=serializer.validated_data["answers"],
            )
        except ExamError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "id": attempt.id,
            "answers": attempt.answers,
            "status": attempt.status,
            "remaining_seconds": attempt.remaining_seconds,
        })


class SubmitExamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, attempt_id):
        answers = request.data.get("answers")

        if answers is not None:
            serializer = SaveAnswersSerializer(data={"answers": answers})
            serializer.is_valid(raise_exception=True)
            answers = serializer.validated_data["answers"]

        try:
            attempt = submit_attempt(
                user=request.user,
                attempt_id=attempt_id,
                answers=answers,
            )
        except ExamError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            ExamAttemptSerializer(attempt, context={"request": request}).data
        )


class ExamResultView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            ExamAttempt.objects
            .select_related("exam", "user")
            .prefetch_related("exam__booklets")
            .filter(
                user=self.request.user,
                status__in=[
                    ExamAttemptStatus.SUBMITTED,
                    ExamAttemptStatus.EXPIRED,
                ],
            )
        )

    def retrieve(self, request, *args, **kwargs):
        attempt = self.get_object()
        return Response(build_exam_result(attempt=attempt, request=request))
