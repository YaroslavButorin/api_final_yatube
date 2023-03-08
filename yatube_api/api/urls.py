from django.urls import include, path
from rest_framework import routers

from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet, basename='follows')
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comments')

urlpatterns = [
    # path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
