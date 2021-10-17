from rest_framework import serializers
from .models import Movie, Category, Review, Rating, Actor


class CategorySerializers(serializers.ModelSerializer):
    """Категории"""

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'url')


class ReviewCreateSerializers(serializers.ModelSerializer):
    """Добавления отзыва"""

    class Meta:
        model = Review
        fields = '__all__'


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариевб тоько parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorListSerializer(serializers.ModelSerializer):
    """Вывод списка акиёров и режесёров"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    """Вывод полного списка акиёра и режесёра"""

    class Meta:
        model = Actor
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")



class MovieListSerializers(serializers.ModelSerializer):
    """Список фильмов"""
    category = CategorySerializers()
    profit = serializers.SerializerMethodField(method_name='get_profit')
    reviews = ReviewCreateSerializers(many=True)
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    def get_profit(self, obj):
        return obj.fess_in_world - obj.budget

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'profit', 'reviews', 'movieshots_set', 'genres', 'rating_user', "middle_star")



class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft", )


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""

    class Meta:
        model = Rating
        fields = ('star', "movie")

    def create(self, validated_data):
        print(validated_data)
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get("star")}

        )
        print(rating)
        return rating

