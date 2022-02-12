from django.urls import path
from rest_framework import routers
from src.user.views import UserList, NearestUsers


# router = routers.SimpleRouter()
# router.register(r'nearest_users', NearestUsers, 'nearest')

urlpatterns = [
    path("list", UserList.as_view()),
    path('nearest_users/', NearestUsers.as_view())
]
