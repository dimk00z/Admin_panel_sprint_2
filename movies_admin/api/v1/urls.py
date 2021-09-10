from api.v1.views import MoviesDetailApi, MoviesList
from django.urls import path

urlpatterns = [
    path("movies/", MoviesList.as_view()),
    path("movies/<uuid:pk>/", MoviesDetailApi.as_view()),
]
