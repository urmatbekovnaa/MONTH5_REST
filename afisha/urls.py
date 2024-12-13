from django.contrib import admin
from django.urls import path
from movie_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/movies/', views.MovieListAPIView),
    path('api/v1/movies/<int:id>', views.MovieDetailAPIView),
    # path('api/v1/reviews/', views.RewiewlistAPIView),
    path('api/v1/reviews/<int:id>', views.RewiewDetailAPIView),
    # path('api/v1/directors/', views.DirectorListAPIView),
    path('api/v1/directors/<int:id>', views.DirectorDetailAPIView),
    path('api/v1/movies/reviews/', views.MovieReviewAPIView)
]
