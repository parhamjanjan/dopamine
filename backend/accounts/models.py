from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # اطلاعات اولیه
    first_name = models.CharField(
        max_length=100,
        verbose_name='نام'
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name='نام خانوادگی'
    )

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        verbose_name='شماره تلفن'
    )

    # اطلاعات پروفایل

    gender = models.CharField(
    max_length=10,
    choices=[
        ('male', 'مرد'),
        ('female', 'زن'),
    ],
    blank=True,
    verbose_name='جنسیت'
    )

    bio = models.TextField(
    blank=True,
    verbose_name='درباره من'
    )

    # تاریخ تولد
    birth_date_gregorian = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاریخ تولد میلادی'
    )

    birth_date_jalali = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name='تاریخ تولد شمسی'
    )

    # اطلاعات تحصیلی
    GRADE_CHOICES = [
        ('10', 'دهم'),
        ('11', 'یازدهم'),
        ('12', 'دوازدهم'),
    ]

    FIELD_CHOICES = [
        ('experimental', 'تجربی'),
        ('mathematics', 'ریاضی'),
        ('humanities', 'انسانی'),
    ]

    grade = models.CharField(
        max_length=2,
        choices=GRADE_CHOICES,
        null=True,
        blank=True,
        verbose_name='پایه تحصیلی'
    )

    field = models.CharField(
        max_length=20,
        choices=FIELD_CHOICES,
        null=True,
        blank=True,
        verbose_name='رشته تحصیلی'
    )

    province = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='استان'
    )

    school = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='مدرسه'
    )

    # تنظیمات ظاهری
    THEME_CHOICES = [
        ('light', 'روشن'),
        ('dark', 'تیره'),
        ('system', 'سیستمی'),
    ]

    theme = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='system',
        verbose_name='تم'
    )

    primary_color = models.CharField(
        max_length=7,
        default='#7055e8',
        verbose_name='رنگ اصلی'
    )

    def __str__(self):
        return self.username