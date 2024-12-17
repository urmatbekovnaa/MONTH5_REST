from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from setuptools.config.pyprojecttoml import validate

from .models import Movie, Director, Review
from .serializers import (MovieSerializer, MovieDetailSerializer, ReviewSerializer, ReviewDetailSerializer,
                          DirectorSerializer, DirectorDetailSerializer, MovieReviewSerializer)
from .serializers import (MovieValidateSerializer, DirectorValidateSerializer, ReviewValidateSerializer,
                          DirectorUpdateSerializer, MovieCreateSerializer, MovieUpdateSerializer)


@api_view(http_method_names=['GET', 'POST'])
def MovieListAPIView(request):
        if request.method == 'GET':
            movies = Movie.objects.all()
            serializer = MovieSerializer(instance=movies, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            serializer = MovieCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            movie = Movie.objects.create(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED,
                            data=MovieListAPIView(movie).data,)


@api_view(['GET', 'PUT', 'DELETE'])
def MovieDetailAPIView(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'message': 'Movie not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieDetailSerializer(movie).data
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = MovieUpdateSerializer(data=request.data, context={'movie': movie})
        serializer.is_valid(raise_exception=True)

        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director_id')
        movie.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=MovieDetailSerializer(movie).data)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(http_method_names=['GET', 'POST'])
def RewiewlistAPIView(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(instance=reviews, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = Review.objects.create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED, data=ReviewDetailSerializer(review).data)


@api_view(['GET', 'PUT', 'DELETE'])
def RewiewDetailAPIView(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'message': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewDetailSerializer(review)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ReviewUpdateSerializer(data=request.data, context={'review': review})
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(review).data)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def DirectorListAPIView(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(instance=directors, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = DirectorCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        director = Director.objects.create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorListAPIView(director).data)


@api_view(['GET', 'PUT', 'DELETE'])
def DirectorDetailAPIView(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'message': 'Director does not exist'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DirectorDetailSerializer(director).data
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = DirectorUpdateSerializer(data=request.data, context={'director': director})
        serializer.is_valid(raise_exception=True)

        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorDetailSerializer(director).data)

    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(http_method_names=['GET'])
def MovieReviewAPIView(request):
    movies = Movie.objects.prefetch_related('reviews').select_related('director').all()
    serializer = MovieReviewSerializer(instance=movies, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
