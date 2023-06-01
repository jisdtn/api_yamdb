from django.urls import path, include
from rest_framework import routers

from .views import (sign_up_view, get_token_view,
                    UserViewSet, CommentViewSet,
                    TitleViewSet, GenreViewSet,
                    CategoryViewSet, ReviewViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='сategories')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', sign_up_view, name='auth_sign_up'),
    path('v1/auth/token/',  get_token_view, name='auth_get_token')
]
