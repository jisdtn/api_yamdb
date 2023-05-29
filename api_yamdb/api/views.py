from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from .permissions import AuthorOrReadOnly

from rest_framework.filters import SearchFilter
from api.mixins import ModelMixinSet
from reviews.models import Genre, Title, Category, Review
from .serializers import (GenreSerializer, TitleCreateSerializer,
                          TitleReadSerializer, CategorySerializer,
                         CommentSerializer, ReviewSerializer)


class CategoryViewSet(ModelMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (HZ,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (HZ,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleReadSerializer
    permission_classes = (HZ,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleReadSerializer
      
      
class CommentViewSet(viewsets.ModelViewSet):
    """
    Комментарии к Публикации.
    """
    serializer_class = CommentSerializer
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        instance_review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=instance_review)
    
    
class ReviewViewSet(viewsets.ModelViewSet):
    """
    Отзыв на произведение.
    """
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    
    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        instance_title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=instance_title)
