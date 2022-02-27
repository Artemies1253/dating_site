import jwt
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from src.authorization.serializers import RegistrationSerializer, LoginSerializer
from src.user.models import User
from .services import create_token, verify_user_email_by_token


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = auth.authenticate(
                username=email, password=password
            )

            if not user:
                raise AuthenticationFailed("Не правильно ведён пароль")

            auth_data = create_token(user_id=user.id)
            auth_data.pop("token_type")

            return Response(auth_data, status=status.HTTP_201_CREATED)


class VerifyEmailAPIView(generics.GenericAPIView):

    def get(self, request, token):
        verify_user_email_by_token(token)
        return HttpResponseRedirect(redirect_to="/")
