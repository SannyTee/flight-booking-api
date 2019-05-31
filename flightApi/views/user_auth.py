"""UserAuthViewSet to create an account and login """
from django.contrib.auth.base_user import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.renderers import (HTMLFormRenderer, JSONRenderer,
                                      BrowsableAPIRenderer)
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from flightApi.models import User
from flightApi.serializers import UserSerializer
from flightApi.util.helpers import upload_image, generate_token


# pylint: disable=no-self-use
class UserAuthViewSet(ViewSet):
    """ Users viewset."""
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request):
        """Create a User"""
        user_info = request.data.copy()
        if user_info['password'] != user_info['confirm_password']:
            data = {
                'status': "error",
                'error': "password and confirm_password does not match",
                'message': "check the password and confirm_password"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(user_info['password'])
            user_info['profile_picture'] = upload_image(user_info['profile_picture'])
            serializer = UserSerializer(data=user_info, context={
                'request': request
            })
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(user_info['password'])
                serializer.save()

                user = User.objects.get(email=user_info['email'])
                token = generate_token(user)
                data = {
                    'status': 'success',
                    'token': token,
                    'message': 'Account successfully created'
                }
                return Response(data, status=status.HTTP_201_CREATED)
            data = {
                'status': 'error',
                'error': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as err:
            data = {
                'status': 'error',
                'error': err
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
