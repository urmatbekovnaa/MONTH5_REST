from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Director, Review
from .serializers import (MovieSerializer, MovieDetailSerializer, ReviewSerializer, ReviewDetailSerializer,
                          DirectorSerializer, DirectorDetailSerializer, MovieReviewSerializer)


@api_view(http_method_names=['GET', 'POST'])
def MovieListAPIView(request):
        if request.method == 'GET':
            movies = Movie.objects.all()
            serializer = MovieSerializer(instance=movies, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            title = request.data.get('title')
            description = request.data.get('description')
            duration = request.data.get('duration')
            director_id = request.data.get('director_id')

            movie = Movie.objects.create(
                title=title,
                description=description,
                duration=duration,
                director_id=director_id)
            print(movie)
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
        data = MovieDetailSerializer(movie).data
        return Response(data=data)

    elif request.method == 'PUT':
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director_id')
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
        text = request.data.get('text')
        stars = request.data.get('stars')
        movie_id = request.data.get('movie_id')

        review = Review.objects.create(
            text=text,
            stars=stars,
            movie_id=movie_id
        )
        return Response(status=status.HTTP_201_CREATED,
                        data=MovieReviewSerializer(review).data)


@api_view(['GET', 'PUT', 'DELETE'])
def RewiewDetailAPIView(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'message': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ReviewDetailSerializer(review).data
        return Response(data=data)

    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.movie_id = request.data.get('movie_id')
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
        name = request.data.get('name')
        director = Director.objects.create(name=name)
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
        data = DirectorDetailSerializer(director).data
        return Response(data=data)

    elif request.method == 'PUT':
        director.name = request.data.get('name')
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