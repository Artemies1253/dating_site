from django.urls import include, path

urlpatterns = [
    path("auth/", include("src.authorization.urls")),
    path("like/", include("src.like.urls")),
]
