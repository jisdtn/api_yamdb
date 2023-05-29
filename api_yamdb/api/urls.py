from django.urls import path, include
from rest_framework import routers

from .views import SignUpView, GetTokenView, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView, name='auth_sign_up'),
    path('v1/auth/token/', GetTokenView, name='auth_get_token')
]
