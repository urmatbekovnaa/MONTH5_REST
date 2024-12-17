from rest_framework import serializers
from .models import Movie, Director, Review
from django.db.models import Avg
from rest_framework.exceptions import ValidationError


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'id title description duration director'.split()

class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=False)
    duration = serializers.IntegerField(min_value=1)
    director_id = serializers.IntegerField(min_value=1)

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError("Director does not exist!")
        return director_id

    def validate_title(self, title):
        if Movie.objects.filter(title__iexact=title).exists():
            raise ValidationError("Movie title already exists!")
        return title


class MovieUpdateSerializer(MovieValidateSerializer):
    def validate_title(self, title):
        movie = self.context.get('movie')
        if Movie.objects.filter(title__iexact=title).exclude(id=movie.id).exists():
            raise ValidationError("Movie title already exists!")
        return title


class MovieCreateSerializer(serializers.ModelSerializer):
    def validate_title(self, title):
        if Movie.objects.filter(title__iexact=title).exists():
            raise ValidationError("Movie title already exists!")
        return title


#review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie'.split()

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

#validate
class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, max_length=1000)
    movie_id = serializers.IntegerField(min_value=1)
    stars = serializers.IntegerField(min_value=1, max_value=5)

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValidationError("Movie does not exist!")
        return movie_id


class ReviewCreateSerializer(serializers.ModelSerializer):
    def validate_movie_id(self, movie_id):
        if Review.objects.filter(movie_id=movie_id).exists():
            raise ValidationError("Movie id already exists!")
        return movie_id

class ReviewUpdateSerializer(ReviewValidateSerializer):
    def validate_movie_id(self, movie_id):
        review = self.context.get('review')
        if Review.objects.filter(movie_id=movie_id).exists():
            raise ValidationError("Movie review already exists!")
        return movie_id


class MovieReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description duration director reviews rating'.split()

    def get_rating(self, movie):
        avg_rating = movie.reviews.aggregate(avg_stars=Avg('stars'))['avg_stars']
        return round(avg_rating, 1) if avg_rating else 0


#ditrcctor
class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField(source='movies.count', read_only=True)

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()

class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

#validate
class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate_name(self, name):
        if Director.objects.filter(name__iexact=name).exists():
            raise ValidationError("Director already exists!")
        return name

class DirectorUpdateSerializer(serializers.Serializer):
    def validate_name(self, name):
        director = self.context.get('director')
        if Director.objects.filter(name__iexact=name).exclude(id=director.id).exists():
            raise ValidationError("Director with this name already exists!")
        return name

class DirectorCreateSerializer(serializers.ModelSerializer):
    def validate_name(self, name):
        if Director.objects.filter(name__iexact=name):
            raise ValidationError("Director already exists!")
        return name