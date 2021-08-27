from rest_framework import serializers
from .models import Movie, Category, Review


class CategorySerializers(serializers.ModelSerializer):
    """Категории"""

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'url')


class ReviewSerializers(serializers.ModelSerializer):
    """Отзывы к фильму"""

    class Meta:
        model = Review
        fields = '__all__'


class MovieListSerializers(serializers.ModelSerializer):
    """Список фильмов"""
    category = CategorySerializers()
    profit = serializers.SerializerMethodField(method_name='get_profit')
    reviews = ReviewSerializers(many=True, source='review_set')


    def get_profit(self, obj):
        return obj.fess_in_world - obj.budget

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'profit', 'reviews', 'movieshots_set', 'rating_set', 'genres')
        depth = 2


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = Movie
        exclude = ("draft", )

