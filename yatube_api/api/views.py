from rest_framework import viewsets, permissions
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
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


class PostViewSet(viewsets.ModelViewSet):
    """
    API for Post model.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        add post author
        :param serializer:
        :return:
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for Group model.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    API for Comment model.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Comments for current post.
        :return:
        """
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        """
        Add comment author
        :param serializer:
        :return:
        """
        serializer.save(author=self.request.user)
