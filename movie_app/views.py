from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Director, Review
from .serializers import (MovieSerializer, MovieDetailSerializer, ReviewDetailSerializer,
                          ReviewSerializer, DirectorSerializer, DirectorDetailSerializer)


@api_view(http_method_names=['GET'])
def MovieListAPIView(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(instance=movies, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def MovieDetailAPIView(request, id):
    movie = Movie.objects.get(id=id)
    data = MovieDetailSerializer(movie).data
    return Response(data)



@api_view(http_method_names=['GET'])
def RewiewlistAPIView(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(instance=reviews, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def RewiewDetailAPIView(request, id):
    review = Review.objects.get(id=id)
    data = ReviewDetailSerializer(review).data
    return Response(data)



@api_view(http_method_names=['GET'])
def DirectorListAPIView(request):
    directors = Director.objects.all()
    serializer = DirectorSerializer(instance=directors, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def DirectorDetailAPIView(request, id):
    director = Director.objects.get(id=id)
    data = DirectorDetailSerializer(director).data
    return Response(data)