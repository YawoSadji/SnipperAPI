from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('add', views.post_snippet),
    path('<int:id>', views.get_single_snippet),
    path('', views.get_all_snippets),
    # path('language/', views.get_snippet_by_language),
    ]