from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import models
from .models import Movie
from .serializers import MovieListSerializers, MovieDetailSerializer, ReviewCreateSerializers, CreateRatingSerializer
from .service import get_client_ip


class MovieListView(APIView):
    """Вывод списка фильмов"""

    def get(self, request):
              movies = Movie.objects.filter(draft=False).annotate(
                    rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self, request)))
              ).annotate(
                    middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
              )
              serializer = MovieListSerializers(movies, many=True)
              return Response(serializer.data)





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



class MovieDetailView(APIView):
    """Вывод фильма"""

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Добавления отзыва к фильму"""

    def post(self, request):
        review = ReviewCreateSerializers(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Добавление рейтинга к фильму"""


    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(ip=get_client_ip(self, request))
        return Response(serializer.data, status=201)


