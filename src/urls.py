from django.urls import include, path

urlpatterns = [
    path("auth/", include("src.authorization.urls")),
    path("like/", include("src.like.urls")),
    path("user/", include("src.user.urls")),
    path("message/", include("src.message.urls")),
    path("notification/", include("src.notification.urls")),
]
