from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import update_session_auth_hash

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
)

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'message': 'حساب کاربری با موفقیت ساخته شد.',

                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'theme': user.theme,
                        'primary_color': user.primary_color,
                    },

                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'message': 'اطلاعات ارسال‌شده معتبر نیست.',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'message': 'ورود با موفقیت انجام شد.',

                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    },

                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'message': 'اطلاعات ورود صحیح نیست.',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser,
    ]

    def get(self, request):

        serializer = ProfileSerializer(
            request.user,
            context={
                'request': request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request):

        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={
                'request': request
            }
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                ProfileSerializer(
                    user,
                    context={
                        'request': request
                    }
                ).data,
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'message': 'اطلاعات ارسال‌شده معتبر نیست.',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={
                'request': request
            }
        )

        if not serializer.is_valid():

            return Response(
                {
                    'message': 'اطلاعات واردشده معتبر نیست.',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user

        user.set_password(
            serializer.validated_data['new_password']
        )

        user.save(
            update_fields=['password']
        )

        update_session_auth_hash(
            request,
            user
        )

        return Response(
            {
                'message': 'رمز عبور با موفقیت تغییر کرد.'
            },
            status=status.HTTP_200_OK
        )