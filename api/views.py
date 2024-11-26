from rest_framework.response import Response
from rest_framework.decorators import api_view
from snippets.models import Snippet
from .serializers import SnippetSerializer, UserSerializer, LoginSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login as django_login
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password
from myapi import settings

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        password = make_password(serializer.validated_data['password'])
        serializer.validated_data['password'] = password
        serializer.save()
        return Response({'message':'User registered'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data = request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            django_login(request._request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error':'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def post_snippet(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = SnippetSerializer(data=request.data)
    if serializer.is_valid():
        f = Fernet(settings.key)
        encrypted_code = f.encrypt(serializer.validated_data['code'].encode('utf-8')).decode('utf-8')
        snippet = Snippet.objects.create(
            user=user, 
            language=serializer.validated_data['language'], 
            code=encrypted_code
        )
        return Response(
            {'message': 'Snippet created successfully'}, 
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_snippets(request):
    user = request.user
    if user.is_authenticated:
        snippets = Snippet.objects.filter(user=user)
        decrypted_snippets = []
        for snippet in snippets:
            f = Fernet(settings.key)
            code = f.decrypt(snippet.code.encode('utf-8')).decode('utf-8')
            decrypted_snippet = {
                'id': snippet.id,
                'language': snippet.language,
                'code': code
            }
            decrypted_snippets.append(decrypted_snippet)
        serializer = SnippetSerializer(decrypted_snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error':'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_single_snippet(request, id):
    user = request.user
    if user.is_authenticated:
        try:
            snippet = Snippet.objects.get(pk=id, user=user)
        except Snippet.DoesNotExist:
            return Response({'error':'Snippet not found'}, status=status.HTTP_404_NOT_FOUND)
        f = Fernet(settings.key)
        code = f.decrypt(snippet.code.encode('utf-8')).decode('utf-8')
        decrypted_snippet = {
                'id': snippet.id,
                'language': snippet.language,
                'code': code
            }
        serializer = SnippetSerializer(decrypted_snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error':'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)