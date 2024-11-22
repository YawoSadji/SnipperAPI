from rest_framework.response import Response
from rest_framework.decorators import api_view
from snippets.models import Snippet
from .serializers import SnippetSerializer

@api_view(['GET'])
def getData(request):
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response(serializer.data)