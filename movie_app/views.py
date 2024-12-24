from collections import OrderedDict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .models import Movie, Director, Review
from .serializers import (
    MovieSerializer, MovieDetailSerializer, ReviewSerializer, ReviewDetailSerializer,
    DirectorSerializer, DirectorDetailSerializer, MovieReviewSerializer,
    MovieValidateSerializer, DirectorValidateSerializer, ReviewValidateSerializer,
    DirectorUpdateSerializer, MovieCreateSerializer, MovieUpdateSerializer,

)


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class MovieListCreateAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination


class MovieDetailAPIView(RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.all()
    lookup_field = 'id'


class ReviewListAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = CustomPagination


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'


class DirectorListAPIView(ListAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    pagination_class = CustomPagination


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorDetailSerializer
    queryset = Director.objects.all()
    lookup_field = 'id'

#
# @api_view(['GET'])
# def MovieReviewAPIView(request):
#     movies = Movie.objects.prefetch_related('reviews').select_related('director').all()
#     serializer = MovieReviewSerializer(instance=movies, many=True)
#     return Response(data=serializer.data, status=status.HTTP_200_OK)


