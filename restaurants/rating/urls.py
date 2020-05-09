from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantView)
router.register(r'ratings', views.RatingView)
router.register(r'user/register', views.UserRegisterView)
router.register(r'user', views.UserGetUpdateView)


urlpatterns = [
    path('/', include(router.urls)),
]
