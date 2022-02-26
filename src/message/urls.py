from django.urls import path

from src.message.views import MessageCreate, MessageListView, MessageUpdateOrDelete

urlpatterns = [
    path('create', MessageCreate.as_view(), name='message_create'),
    path('list_with_user/<int:pk>', MessageListView.as_view(), name='message_list'),
    path('<int:message_id>', MessageUpdateOrDelete.as_view(), name='message_update_or_delete'),
]
