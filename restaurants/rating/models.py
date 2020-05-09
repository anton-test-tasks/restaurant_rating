from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator, FileExtensionValidator
from django.core.exceptions import ValidationError


class Restaurant(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50, unique=True, error_messages={
        'blank': 'Blank field not allowed',
        'null': 'Null field not allowed',
        'max_length': 'Only 50 symbols allowed',
        'unnique': 'Seems like this restaurant already exists'
    })
    food_type = models.CharField(blank=False, null=False, max_length=100, error_messages={
        'blank': 'Blank field not allowed',
        'null': 'Null field not allowed',
        'max_length': 'Only 100 symbols allowed',
    })
    address = models.CharField(blank=False, null=False, max_length=300, error_messages={
        'blank': 'Blank field not allowed',
        'null': 'Null field not allowed',
        'max_length': 'Only 300 symbols allowed',
    })
    website = models.URLField(default='', max_length=30, blank=True, null=True,
                              validators=[URLValidator(schemes=['http', 'https'], message='Invalid URL')])
    phone = models.CharField(default='', max_length=15, blank=True, null=True)
    cost_level = models.IntegerField(default=1, null=True, blank=True, validators=[MinValueValidator(1),
                                                                                   MaxValueValidator(3)])
    work_time_from = models.TimeField(blank=True, null=True)
    work_time_till = models.TimeField(blank=True, null=True)
    working_days = models.CharField(default='M, TU, W, TH, F, SA, SU', blank=True, null=True, max_length=30)
    longitude = models.FloatField(default=0, blank=True, null=True)
    latitude = models.FloatField(default=0, blank=True, null=True)
    review_count = models.IntegerField(default=0, blank=True, null=True)
    image = models.ImageField(default='media/restaurant_images/default-image-name.jpeg',
                              upload_to='media/restaurant_images',
                              null=True,
                              blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg'],
                                                                 message='Invalid file extension')])
    overall_rating = models.DecimalField(default=0, max_length=1, max_digits=5, decimal_places=1,
                                         blank=True, null=True, validators=[MinValueValidator(0.0),
                                                                            MaxValueValidator(5.0)],
                                         error_messages={'max_length': 'Value should be in range 1 - 5',
                                                         'max_digits': 'Value should be in range 1 - 5'})

    def __str__(self):
        return self.name


def update_overall_rating(restaurant):
    """ Update overall_rating field for restaurant """
    overall_rating = Rating.objects.filter(restaurant=restaurant).aggregate(r=Avg("rating"))["r"] or 0
    restaurant_to_update = Restaurant.objects.get(pk=restaurant.id)
    restaurant_to_update.overall_rating = overall_rating
    restaurant_to_update.save()


def update_review_count(restaurant):
    """ Update review_count field for restaurant """
    review_count = Rating.objects.filter(restaurant=restaurant).aggregate(r=Count("rating"))["r"] or 0
    restaurant_to_update = Restaurant.objects.get(pk=restaurant.id)
    restaurant_to_update.review_count = review_count
    restaurant_to_update.save()


class Rating(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, error_messages={
        'blank': 'Blank field not allowed',
        'null': 'Null field not allowed'
    })
    restaurant = models.ForeignKey(Restaurant, blank=False, null=False, on_delete=models.CASCADE, error_messages={
        'blank': 'Blank field not allowed',
        'null': 'Null field not allowed'
    })
    rating = models.DecimalField(blank=False, null=False, decimal_places=1, max_length=1, max_digits=5, error_messages={
        'blank': 'Blank field not allowed',
        'null': 'Null field not allowed',
        'max_length': 'Value should be in range 1 - 5',
        'max_digits': 'Value should be in range 1 - 5'
    })

    def __str__(self):
        return self.restaurant.name + str(self.rating)

    def update(self, *args, **kwargs):
        super(Rating, self).update(*args, **kwargs)
        update_overall_rating(self.restaurant)

    def save(self, *args, **kwargs):
        rating = Rating.objects.filter(user=self.user, restaurant=self.restaurant)
        if not rating.exists():
            super(Rating, self).save(*args, **kwargs)
            update_review_count(self.restaurant)
            update_overall_rating(self.restaurant)
