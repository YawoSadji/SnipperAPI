from django.shortcuts import render
from rest_framework import viewsets
from .models import Snippet
from .serializers import SnippetSerializer
# Create your views here.

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer