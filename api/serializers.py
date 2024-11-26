from rest_framework import serializers
from snippets.models import Snippet, User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'language', 'code']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

        def create(self, validated_data):
            user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])
            return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user is not None:
                if not user.is_active:
                    raise serializers.ValidationError(_('User account is disabled.'))
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError(_('Unable to log in with provided credentials.'))
        else:
            raise serializers.ValidationError(_('Must include email and password.'))