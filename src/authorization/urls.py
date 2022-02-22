from django.urls import path
from .api import RegistrationAPIView, LoginAPIView, VerifyEmailAPIView

urlpatterns = [
    path("register", RegistrationAPIView.as_view()),
    path("login", LoginAPIView.as_view()),
    path("verify_email/<str:token>", VerifyEmailAPIView.as_view(), name="verify_email"),
]
