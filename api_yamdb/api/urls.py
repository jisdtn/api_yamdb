from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),

]
