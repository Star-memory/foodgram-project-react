from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyTag(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return False
