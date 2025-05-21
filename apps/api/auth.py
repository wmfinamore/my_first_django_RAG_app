from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.api import serializers


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
        })


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)
        if allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY:
            return Response({'detail': 'Verification e-mail sent.'}, status=status.HTTP_201_CREATED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'email': user.email},
                        status=status.HTTP_201_CREATED)

