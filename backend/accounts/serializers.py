from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.db import transaction

from rest_framework import serializers

from planner.models import PlannerList
from django.contrib.auth import password_validation


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    password_confirm = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'username',
            'password',
            'password_confirm',
            'gender',
            'bio',
            'birth_date_gregorian',
            'birth_date_jalali',
            'grade',
            'field',
            'province',
            'school',
            'theme',
            'primary_color',
        ]

    def validate_username(self, value):

        if User.objects.filter(
            username=value
        ).exists():

            raise serializers.ValidationError(
                'این نام کاربری قبلاً استفاده شده است.'
            )

        return value

    def validate_phone_number(self, value):

        if value and User.objects.filter(
            phone_number=value
        ).exists():

            raise serializers.ValidationError(
                'این شماره تلفن قبلاً ثبت شده است.'
            )

        return value

    def validate(self, attrs):

        if attrs['password'] != attrs['password_confirm']:

            raise serializers.ValidationError({
                'password_confirm':
                    'رمز عبور و تکرار آن یکسان نیستند.'
            })

        attrs.pop('password_confirm')

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        password = validated_data.pop(
            'password'
        )

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        # ========================================
        # لیست‌های پیش‌فرض کاربر
        # ========================================

        field_lists = {

            'experimental': [
                'زیست',
                'شیمی',
                'فیزیک',
                'ریاضی',
                'زمین',
            ],

            'mathematics': [
                'ریاضی',
                'فیزیک',
                'شیمی',
            ],

            'humanities': [
                'ریاضی و آمار',
                'اقتصاد',
                'علوم و فنون ادبی',
                'عربی',
                'تاریخ',
                'جغرافیا',
                'جامعه‌شناسی',
                'فلسفه و منطق',
                'روان‌شناسی',
            ],
        }

        # لیست دروس عمومی برای همه رشته‌ها
        default_lists = [
            'عمومی'
        ]

        # دروس اختصاصی رشته کاربر
        selected_field_lists = field_lists.get(
            user.field,
            []
        )

        lists_to_create = []

        for list_name in (
            selected_field_lists +
            default_lists
        ):

            lists_to_create.append(
                PlannerList(
                    user=user,
                    name=list_name,
                    color = user.primary_color
                )
            )

        PlannerList.objects.bulk_create(
            lists_to_create
        )

        return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if not user:

            raise serializers.ValidationError(
                'نام کاربری یا رمز عبور اشتباه است.'
            )

        if not user.is_active:

            raise serializers.ValidationError(
                'این حساب کاربری غیرفعال است.'
            )

        attrs['user'] = user

        return attrs

class ProfileSerializer(serializers.ModelSerializer):

    profile_image = serializers.ImageField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'gender',
            'bio',
            'birth_date_gregorian',
            'birth_date_jalali',
            'grade',
            'field',
            'province',
            'school',
            'theme',
            'primary_color',
            'profile_image',
            'is_staff'
        ]

        read_only_fields = [
            'id',
            'username',
        ]


class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField(
        write_only=True,
        required=True
    )

    new_password = serializers.CharField(
        write_only=True,
        required=True
    )

    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate_current_password(self, value):

        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                'رمز عبور فعلی صحیح نیست.'
            )

        return value

    def validate(self, attrs):

        new_password = attrs['new_password']
        new_password_confirm = attrs['new_password_confirm']

        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                'new_password_confirm':
                    'تکرار رمز عبور جدید با رمز عبور جدید یکسان نیست.'
            })

        if attrs['current_password'] == new_password:
            raise serializers.ValidationError({
                'new_password':
                    'رمز عبور جدید باید با رمز عبور فعلی متفاوت باشد.'
            })

        try:
            password_validation.validate_password(
                new_password,
                self.context['request'].user
            )
        except serializers.ValidationError as error:
            raise serializers.ValidationError({
                'new_password': error.messages
            })

        return attrs