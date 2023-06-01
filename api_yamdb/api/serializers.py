import re
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.authentication import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailValidator
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from django.shortcuts import get_object_or_404
from datetime import datetime

from reviews.models import Title, Category, Genre, Comment,  Review


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[
            EmailValidator(),
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Can\'t use this username!')
        if not re.match(r"^[\w.@+-]+$", value):
            raise ValidationError('Incorrect username!')
        return value


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.SlugField(
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Can\'t use this username!')
        return value

    def validate(self, data):
        username = data['username']
        email = data['email']
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise ValidationError('Wrong email!')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.username != username:
                raise ValidationError(
                    {'email': ['Email must be unique!',]}
                )
        return data


class UserTokenSerializer(serializers.Serializer):
    username = serializers.SlugField(
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    def validate(self, data):
        # Check if user exists
        user = get_object_or_404(User, username=data['username'])
        # Check if confirmation code is correct
        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                {'confirmation_code': ['Wrong confirmation code!',]}
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', )
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    
    def validate_year(self, data):
        if data >= datetime.now().year:
            raise serializers.ValidationError(
                f'Год {data} не может быть больше текущего года!',
            )
        return data


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description',
        )
        

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'title', 'review')
        model = Comment

        
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date', 'title')
        model = Review

