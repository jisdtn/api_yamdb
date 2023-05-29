from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    pass

class Title(models.Model):
    pass


class Review(models.Model):

    author = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
            Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(1)])
    created = models.DateTimeField(
            'Дата добавления', auto_now_add=True, db_index=True)

    def rating(self):
        reviews = self.reviews.all()
        score = int(input())
        rating = 0
        for i in reviews:
            rating = rating + score
        return rating / len(reviews)
      
    def __str__(self):
        return self.text
 

class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text

   
