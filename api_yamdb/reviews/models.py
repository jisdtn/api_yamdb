from rest_framework.authentication import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=200
    )

    slug = models.SlugField(
        verbose_name='Слаг категории',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=200
    )

    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200,
        db_index=True
    )

    year = models.IntegerField(
        verbose_name='Год произведения',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )

    description = models.TextField(
        verbose_name='Описание произведения',
        max_length=255,
        null=True,
        blank=True
    )

    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
            Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(max_length=200)
    score = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
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


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'
