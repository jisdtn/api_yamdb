from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from reviews.models import Title

from .serializers import ReviewSerializer


class AuthorOrReadOnly:
    pass


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
