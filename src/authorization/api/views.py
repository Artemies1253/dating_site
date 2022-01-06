from rest_framework import generics

from src.authorization.api.serializers import RegistrationSerializer


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
