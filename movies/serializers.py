from rest_framework import serializers
from .models import Movie, Category, Review


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


class RecursiveSerializer(serializers.ModelSerializer):
    """Вывод рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


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


    def get_profit(self, obj):
        return obj.fess_in_world - obj.budget

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'profit', 'reviews', 'movieshots_set', 'rating_set', 'genres')
        # depth = 2


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft", )

