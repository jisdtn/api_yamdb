from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.authentication import get_user_model
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import AdminOnly
from .serializers import (UserSerializer,
                          UserSignUpSerializer,
                          UserTokenSerializer)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'
    permission_classes = (AdminOnly, )
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                if (request.data.get('role')
                   and (user.role != 'admin' or not user.is_superuser)):
                    return Response(serializer.data,
                                    status=status.HTTP_403_FORBIDDEN)
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['post'])
@permission_classes([AllowAny])
def SignUpView(request):
    serializer = UserSignUpSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        user, _ = User.objects.get_or_create(**validated_data)
        confirmation_code = default_token_generator.make_token(user)
        email = user.email
        send_mail(
            "Confirmation code",
            confirmation_code,
            "from@example.com",
            [email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['post'])
@permission_classes([AllowAny])
def GetTokenView(request):
    serializer = UserTokenSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data.get('username')
        user = User.objects.get(username=username)
        token = AccessToken.for_user(user)
        token.set_exp(lifetime=timedelta(days=1))
        response = {"token": str(token)}
        return Response(data=response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
