from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Snippet
from .serializers import SnippetSerializer
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']