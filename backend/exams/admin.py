from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse

from .models import (
    Exam,
    ExamBooklet,
    ExamAttempt,
    ExamResult,
    ExamBookletResult,
)

from .finalize_service import finalize_exam


class ExamBookletInline(admin.TabularInline):
    model = ExamBooklet

    extra = 1

    fields = (
        "title",
        "subject",
        "order",
        "factor",
        "start_question",
        "question_count",
        "end_question_display",
    )

    readonly_fields = (
        "end_question_display",
    )

    ordering = ("order",)

    def end_question_display(self, obj):
        if not obj.pk:
            return "-"

        return obj.end_question

    end_question_display.short_description = (
        "شماره پایان"
    )


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "start_at",
        "end_at",
        "duration_minutes",
        "total_questions",
        "is_active",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )

    ordering = ("-start_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        ExamBookletInline
    ]

    fieldsets = (
        (
            "اطلاعات آزمون",
            {
                "fields": (
                    "title",
                    "description",
                    "category",
                    "is_active",
                )
            },
        ),

        (
            "زمان‌بندی",
            {
                "fields": (
                    "start_at",
                    "end_at",
                    "duration_minutes",
                )
            },
        ),

        (
            "فایل‌ها",
            {
                "fields": (
                    "questions_pdf",
                    "questions_pdf_url",
                    "answer_pdf",
                    "answer_pdf_url",
                )
            },
        ),

        (
            "تصحیح",
            {
                "fields": (
                    "total_questions",
                    "answer_key",
                )
            },
        ),

        (
            "سیستم",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "<path:object_id>/finalize/",
                self.admin_site.admin_view(
                    self.finalize_view
                ),
                name="exams_exam_finalize",
            ),
        ]

        return custom_urls + urls

    def finalize_view(
        self,
        request,
        object_id,
    ):
        exam = self.get_object(
            request,
            object_id,
        )

        if exam is None:
            self.message_user(
                request,
                "آزمون موردنظر پیدا نشد.",
                level=messages.ERROR,
            )

            return HttpResponseRedirect(
                reverse(
                    "admin:exams_exam_changelist"
                )
            )

        if not self.has_change_permission(
            request,
            exam,
        ):
            self.message_user(
                request,
                "شما اجازه انجام این عملیات را ندارید.",
                level=messages.ERROR,
            )

            return HttpResponseRedirect(
                reverse(
                    "admin:exams_exam_change",
                    args=[exam.pk],
                )
            )

        try:
            result = finalize_exam(
                exam_id=exam.id
            )

            self.message_user(
                request,
                (
                    "تصحیح و رتبه‌بندی از صفر انجام شد. "
                    f'شرکت‌کنندگان: {result["participants"]} نفر. '
                    f'کارنامه جدید: {result["results_created"]}. '
                    f'کارنامه به‌روزشده: {result["results_updated"]}.'
                ),
                level=messages.SUCCESS,
            )

        except Exception as error:
            self.message_user(
                request,
                (
                    "در فرایند تصحیح و رتبه‌بندی خطایی رخ داد: "
                    f"{error}"
                ),
                level=messages.ERROR,
            )

        return HttpResponseRedirect(
            reverse(
                "admin:exams_exam_change",
                args=[exam.pk],
            )
        )


@admin.register(ExamBooklet)
class ExamBookletAdmin(admin.ModelAdmin):
    list_display = (
        "exam",
        "title",
        "subject",
        "order",
        "factor",
        "start_question",
        "question_count",
        "end_question_display",
    )

    list_filter = (
        "subject",
        "exam",
    )

    search_fields = (
        "exam__title",
        "title",
        "subject",
    )

    ordering = (
        "exam",
        "order",
    )

    readonly_fields = (
        "end_question_display",
    )

    def end_question_display(self, obj):
        return obj.end_question

    end_question_display.short_description = (
        "شماره پایان"
    )


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "exam",
        "status",
        "started_at",
        "expires_at",
        "submitted_at",
        "score",
        "raw_score",
    )

    list_filter = (
        "status",
        "exam",
    )

    search_fields = (
        "user__username",
        "exam__title",
    )

    readonly_fields = (
        "user",
        "exam",
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
        "created_at",
        "updated_at",
    )


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "exam",
        "is_final",
        "score",
        "raw_score",
        "national_rank",
        "provincial_rank",
        "finalized_at",
    )

    list_filter = (
        "is_final",
        "exam",
    )

    search_fields = (
        "user__username",
        "exam__title",
    )


@admin.register(ExamBookletResult)
class ExamBookletResultAdmin(admin.ModelAdmin):
    list_display = (
        "result",
        "booklet",
        "score",
        "raw_score",
        "decile",
        "national_rank",
        "provincial_rank",
    )

    list_filter = (
        "booklet",
        "decile",
    )

    search_fields = (
        "result__user__username",
        "result__exam__title",
        "booklet__title",
    )