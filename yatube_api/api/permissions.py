from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Author: read/write permission
    Other: read permission
    """

    def has_object_permission(self, request, view, obj):
        """
        Only author can change/delete.
        :param request:
        :param view:
        :param obj: post or comment
        :return: Boolean
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author
