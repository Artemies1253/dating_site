from django.urls import path

from src.notification import views

urlpatterns = [
    path('list', views.NotificationListView.as_view(), name='notification_list'),
]
