from rest_framework import permissions


class IsAuthor(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthorOrReceiver(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.reciever == request.user


class IsOwnerLike(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.owner_user == request.user
