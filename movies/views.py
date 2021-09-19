from rest_framework import generics, request


from django.db import models
from .models import Movie, Actor
from .serializers import (
    MovieListSerializers,
    MovieDetailSerializer,
    ReviewCreateSerializers,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)

from .service import get_client_ip


class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializers


    def get_queryset(self):
              movies = Movie.objects.filter(draft=False).annotate(
                    rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self, self.request)))
              ).annotate(
                    middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
              )
              return movies






    # def get(self, request):
    #     #     movies = Movie.objects.filter(draft=False).annotate(
    #     #         rating_user=models.Case(
    #     #             models.When(ratings__ip=get_client_ip(self, request), then=True),
    #     #                default=False,
    #     #                output_field=models.BooleanField()
    #     #             ),
    #     #     )
    #     #     serializer = MovieListSerializers(movies, many=True)
    #     #     return Response(serializer.data)



class MovieDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer



class ReviewCreateView(generics.CreateAPIView):
    """Добавления отзыва к фильму"""
    serializer_class = ReviewCreateSerializers



class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(request, self.request))


class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""


    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer



class ActorsDetailView(generics.RetrieveAPIView):
    """Вывод  актера или режесёра"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
