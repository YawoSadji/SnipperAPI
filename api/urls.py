from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_or_post_snippet),
    path('<int:id>', views.get_single_snippet),
    path('language/', views.get_snippet_by_language),
    ]