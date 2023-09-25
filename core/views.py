from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status
from django.conf import settings
import jwt
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, VerifySerializer
from .email import *
# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        data = request.data
        is_staff = True
        data['is_staff'] = is_staff
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('verify-users')
        absUrl = 'http://' + current_site+relativeLink+"?token="+str(token)
        
        message = 'Use link to register\n' + absUrl
        data = {'message': message, 'email': user.email}

        send_email(data)
        return Response(user_data,status=status.HTTP_201_CREATED)
            


class VerifyView(APIView):
    def post(self,request):
        token = request.GET.get('token')
        serializer = VerifySerializer(data=request.data)

        if serializer.is_valid():
            password = serializer.validated_data['password']
            try:
                payload = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(id=payload['user_id'])
                if not user.is_verified:
                    try:
                        user.is_verified = True
                        user.save()
                    except:
                        user.is_verified = False

                if user.password=='':
                    try:
                        user.set_password(password)
                        user.save()
                        return Response('Password set successfully', status=status.HTTP_200_OK)
                    except:
                        return Response('Something went wrong!', status=status.HTTP_400_BAD_REQUEST)

                return Response('Password already set', status=status.HTTP_400_BAD_REQUEST)
            
            except User.DoesNotExist:
                return Response('User not found.', status=status.HTTP_404_NOT_FOUND)

            # Set the new password for the user
            except jwt.ExpiredSignatureError:
                return Response('Activation Expired', status=status.HTTP_400_BAD_REQUEST)
            except jwt.DecodeError:
                return Response('Invalid Token', status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user 
        if user.is_staff:
            return Response("Hello staff", status=status.HTTP_200_OK)
        else:
            return Response("Hello user", status=status.HTTP_200_OK)
