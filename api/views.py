from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    # def create(self, request, *args, **kwargs):
    #     print('running this post function...')
    #     return Response({
    #         'proceed': True,
    #         'content': None,
    #         'message': None
    #     })


    @action(detail=False, methods=['post'], url_path='authorize')
    def authorize(self, request, *args, **kwargs):
        proceed = False
        content = None

        try:
            db_user = User.objects.filter(username=request.data['username']).first()
            proceed = db_user.password == request.data['password']
            message = "Authorized" if proceed else 'Invalid credentials'
        except Exception:
            message = 'Invalid credentials'


        return Response({
            'proceed': proceed,
            'content': content,
            'message': message
        })