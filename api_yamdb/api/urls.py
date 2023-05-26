from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet

app_name = 'api'


router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
