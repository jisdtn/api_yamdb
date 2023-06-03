from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework.authentication import get_user_model
from users.models import User
from titles.models import Title, Genre, Category, GenreTitle

User = get_user_model()


class Review(models.Model):

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField(max_length=200)
    score = models.SmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-pub_date"]
        constraints = (models.UniqueConstraint(
            fields=['title', 'author'], name='unique_review'),
        )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
