from logging import exception

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .middleware import encrypt, decrypt

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
        print('running this post function...')
        proceed = False
        content = None
        encrypt_id = None

        try:
            db_user = User.objects.filter(username=request.data['username'])[0]
            print(db_user)
            proceed = db_user.password == request.data['password']
            message = "Authorized" if proceed else 'Invalid credentials'
            # encrypt_id = encrypt(db_user.id)



        except Exception as e:
            print('exception occured', e)
            message = 'Invalid credentials'

        response = Response({
            'proceed': proceed,
            'content': db_user.extract_json(),
            'message': message
        })

        response.set_cookie(key='quiz_token', value="sachindu Kavishka", max_age=3600*24*365, httponly=True, secure=False, samesite='Lax', path="/")

        return response