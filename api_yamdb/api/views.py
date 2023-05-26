from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions

from .permissions import AuthorOrReadOnly
from .serializers import CommentSerializer
from .reviews.models import Review


# Create your views here.

class CommentViewSet(viewsets.ModelViewSet):
    """
    Комментарии к Публикации.
    """
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
