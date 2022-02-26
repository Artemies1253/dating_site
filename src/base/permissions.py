from rest_framework import permissions


class IsAuthor(permissions.IsAuthenticated):
    def get_object_permission(self, request, obj):
        return obj.user == request.user


class IsAuthorOrReceiver(permissions.IsAuthenticated):
    def get_object_permission(self, request, obj):
        return obj.user == request.user or obj.reciever == request.user

