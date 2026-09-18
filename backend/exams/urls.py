from django.urls import path

from .views import (
    ExamListView,
    ExamDetailView,
    StartExamView,
    AttemptDetailView,
    AttemptAnswersView,
    SubmitExamView,
    ExamResultView,
)


urlpatterns = [
    path(
        "",
        ExamListView.as_view(),
        name="exam-list",
    ),

    path(
        "<int:pk>/",
        ExamDetailView.as_view(),
        name="exam-detail",
    ),

    path(
        "<int:exam_id>/start/",
        StartExamView.as_view(),
        name="exam-start",
    ),

    path(
        "attempts/<int:pk>/",
        AttemptDetailView.as_view(),
        name="attempt-detail",
    ),

    path(
        "attempts/<int:attempt_id>/answers/",
        AttemptAnswersView.as_view(),
        name="attempt-answers",
    ),

    path(
        "attempts/<int:attempt_id>/submit/",
        SubmitExamView.as_view(),
        name="attempt-submit",
    ),

    path(
        "attempts/<int:pk>/result/",
        ExamResultView.as_view(),
        name="attempt-result",
    ),
]