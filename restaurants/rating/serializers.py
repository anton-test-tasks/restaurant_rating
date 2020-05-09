from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class RestaurantSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False, allow_empty_file=True)

    class Meta:
        model = models.Restaurant
        fields = ('id', 'url', 'name', 'food_type', 'address', 'website', 'phone', 'cost_level', 'work_time_from',
                  'work_time_till', 'working_days', 'longitude', 'latitude', 'review_count', 'image',
                  'overall_rating')
        read_only_fields = ('id', 'url', 'overall_rating', 'review_count')

    def create(self, validated_data):
        restaurant = models.Restaurant(**validated_data)
        restaurant.save()
        return restaurant

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.food_type = validated_data.get('food_type', instance.food_type)
        instance.address = validated_data.get('address', instance.address)
        instance.website = validated_data.get('website', instance.website)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.work_time_from = validated_data.get('work_time_from', instance.work_time_from)
        instance.work_time_till = validated_data.get('work_time_till', instance.work_time_till)
        instance.working_days = validated_data.get('working_days', instance.working_days)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Rating
        fields = ('id', 'url', 'user', 'restaurant', 'rating')
        read_only_fields = ('id', 'url')

    def create(self, validated_data):
        rating = models.Rating(**validated_data)
        rating.save()
        return rating

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
