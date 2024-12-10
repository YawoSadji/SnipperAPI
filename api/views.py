from rest_framework.response import Response
from rest_framework.decorators import api_view
from snippets.models import Snippet
from .serializers import SnippetSerializer, UserSerializer, LoginSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login as django_login, logout
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password
from myapi import settings
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
#.........................................................................................................
import json
from authlib.integrations.django_client import OAuth
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

oauth = OAuth()

oauth.register(
    'auth0',
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid profile email'},
)

@api_view(['GET'])
def login(request):
    return oauth.auth0.authorize_redirect(request, request.build_absolute_uri(reverse('callback')))

@api_view(['GET'])
def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session['user'] = token
    return redirect(reverse('index'))

@api_view(['GET', 'POST'])
def logout_user(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                'returnTo': request.build_absolute_uri(reverse('index')),
                'client_id': settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )

def index(request):
    return render(
        request,
        'index.html',
        context={
            'session': request.session.get('user'),
            'pretty': json.dumps(request.session.get('user'), indent=4),
        },
    )








#...............................................................................................................
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        password = make_password(serializer.validated_data['password'])
        serializer.validated_data['password'] = password
        serializer.save()
        return Response({'message':'User registered'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login(request):
#     serializer = LoginSerializer(data = request.data)
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']
#         user = authenticate(email=email, password=password)
#         if user is not None:
#             django_login(request._request, user)
#             return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#         return Response({'error':'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def logout_user(request):
#     user = request.user
#     if user.is_authenticated:
#         logout(request)
#         return Response({'message': 'You are successfully logged out'}, status=status.HTTP_200_OK)
#     return Response({'error':'You are not logged in'}, status=status.HTTP_401_UNAUTHORIZED)


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