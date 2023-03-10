from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from posts.models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (PostSerializer, CommentSerializer, GroupSerializer,
                          FollowSerializer)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthorOrReadOnly, ]
    serializer_class = GroupSerializer
    http_method_names = ['get', 'head']


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def get_post(self):
        return get_object_or_404(
            Post, pk=self.kwargs.get('post_id')
        )

    def get_queryset(self):
        return self.get_post().comments.all()


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ('following__username', 'user__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
