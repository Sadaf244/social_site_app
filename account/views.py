from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .models import *
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password

class CreateAccount(APIView):

    def post(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            create_user_manager = UserAccountManager(request)
            save_user_resp = create_user_manager.start_on_boarding()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
        except Exception as e:
            logging.error('Error in creating account', repr(e))
        return JsonResponse(resp_dict, status=200)


class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials')

        if not check_password(password, user.password):
            raise AuthenticationFailed('Invalid credentials')

        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token}, status=status.HTTP_200_OK)