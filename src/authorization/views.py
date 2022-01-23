from django.contrib import auth
from rest_framework import generics, status, permissions
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

            user = User.object.get(email=serializer.validated_data.get("email"))

            return Response({"data": user.id}, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            user = User.object.filter(email=email)

            if not user:
                raise AuthenticationFailed("Нет пользователя с данным email")

            password = serializer.validated_data.get("password")
            user = auth.authenticate(
                username=email, password=password
            )

            if not user:
                raise AuthenticationFailed("Не правильно ведён пароль")

            auth_data = create_token(user_id=user.id)

            return Response({"data": auth_data})
