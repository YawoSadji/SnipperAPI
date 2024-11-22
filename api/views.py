from rest_framework.response import Response
from rest_framework.decorators import api_view
from snippets.models import Snippet
from .serializers import SnippetSerializer
from rest_framework import status



@api_view(['GET', 'POST'])
def get_or_post_snippet(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_single_snippet(request, id):
    try:
        snippet = Snippet.objects.get(pk=id)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = SnippetSerializer(snippet)
    return Response(serializer.data)

@api_view(['GET'])
def get_snippet_by_language(request):
    language = request.query_params.get('language', None)
    if language:
        snippets = Snippet.objects.filter(language__iexact=language)
    else:
        snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response(serializer.data)