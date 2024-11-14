from rest_framework import serializers
from .models import User, Snippet

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id','language','code']