from django.urls import path
from . import sviews



urlpatterns = [
    path('', sviews.home, name='home'),
    ]