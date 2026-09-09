from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'اطلاعات دوپامین',
            {
                'fields': (
                    'phone_number',
                    'birth_date_gregorian',
                    'birth_date_jalali',
                    'grade',
                    'field',
                    'province',
                    'school',
                    'theme',
                    'primary_color',
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'اطلاعات دوپامین',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'phone_number',
                    'birth_date_gregorian',
                    'birth_date_jalali',
                    'grade',
                    'field',
                    'province',
                    'school',
                    'theme',
                    'primary_color',
                )
            },
        ),
    )