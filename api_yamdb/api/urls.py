from django.urls import include, path
# from rest_framework import routers
# from rest_framework.routers import DefaultRouter # какой из них используем 
from .views import CommentViewSet, TitleViewSet, GenreViewSet, CategoryViewSet

app_name = 'api'

# router = routers.DefaultRouter()
# router = DefaultRouter()


router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='сategories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
]
