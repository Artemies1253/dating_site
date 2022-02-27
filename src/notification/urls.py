from django.urls import path

from src.notification import api

urlpatterns = [
    path('list', api.NotificationListView.as_view(), name='notification_list'),
]
