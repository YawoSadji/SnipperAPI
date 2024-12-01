from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout_user),
    path('add', views.post_snippet),
    path('<int:id>', views.get_single_snippet),
    path('', views.get_all_snippets),
    # path('<int:id>', views.update_snippet),
    # path('<int:id>', views.delete_single_snippet),
    # path('', views.delete_all_snippets),
    # path('language/', views.get_snippet_by_language),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]

