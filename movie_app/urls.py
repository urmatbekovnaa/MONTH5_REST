from django.urls import path
from movie_app import views

urlpatterns = [
    path('movie_list/', views.MovieListAPIView),
    path('<int:pk>/', views.MovieDetailAPIView),
    path('rewiew_list/', views.RewiewlistAPIView),
    path('<int:id>/', views.RewiewDetailAPIView),
    path('director_list/', views.DirectorListAPIView),
    path('<int:id>/', views.DirectorDetailAPIView),
    path('<int:id>/', views.MovieReviewAPIView)
]