from django.urls import path
from movie_app import views

urlpatterns = [
    path('movie_list/', views.MovieListCreateAPIView.as_view()),
    path('<int:pk>/', views.MovieDetailAPIView.as_view()),
    path('rewiew_list/', views.ReviewListAPIView.as_view()),
    path('<int:id>/', views.ReviewDetailAPIView.as_view()),
    path('director_list/', views.DirectorListAPIView.as_view()),
    path('<int:id>/', views.DirectorDetailAPIView.as_view()),
    # path('<int:id>/', views.MovieReviewAPIView)
]