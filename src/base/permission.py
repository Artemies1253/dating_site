from rest_framework import permissions


class IsOwnerUserPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.owner_user == request.user
