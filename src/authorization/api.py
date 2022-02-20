from django.contrib import auth
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from src.authorization.serializers import RegistrationSerializer, LoginSerializer
from src.user.models import User
from .services import create_token


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = User.objects.get(email=serializer.validated_data.get("email"))

            return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            user = User.objects.filter(email=email, is_delete=False)

            if not user:
                raise AuthenticationFailed("Нет пользователя с данным email")

            password = serializer.validated_data.get("password")
            user = auth.authenticate(
                username=email, password=password
            )

            if not user:
                raise AuthenticationFailed("Не правильно ведён пароль")

            auth_data = create_token(user_id=user.id)
            auth_data.pop("token_type")

            return Response(auth_data, status=status.HTTP_201_CREATED)
