from rest_framework.response import Response
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView, exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions, status
from .validations import *
from .models import *
# from django.contrib.auth import login, logout # For sessionID
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
import threading
import jwt
from user_authentication.settings import SIMPLE_JWT
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        clean_data = user_validation(request.data)
        serializer = UserRegistrationSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create_normal_user(clean_data)
            if user:
                # Email Verification using token generations
                user_id = urlsafe_base64_encode(force_bytes(user.pk))
                user_token = MyTokenObtainPairSerializer.get_token(user)
                token = str(user_token.access_token)
                domain = get_current_site(request).domain

                activate_url = 'http://' + domain + '/api/activate/' + user_id + "/" + str(token)

                # Email Container for verification
                email_subject = 'Confirm your Email to Activate your account'
                email_body = 'Hello! ' + user.first_name + '\nPlease click the link to verify your account\n' + activate_url

                email = EmailMessage(email_subject, email_body, 'noreply@sample.com', [user.email])
                # send_mail(email_subject, email_body, 'noreply@sample.com', [user.email])
                EmailThread(email).start()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class VerificationView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, uidb64, token):

        try:
            decoded = jwt.decode(
                token,
                SIMPLE_JWT['SIGNING_KEY'],
                algorithms=[SIMPLE_JWT['ALGORITHM']],
            )

            user = MyUser.objects.get(pk=decoded['user_id'])

            if user.is_active:
                return Response(data={"message", "user already authenticated"} ,status=status.HTTP_200_OK)
            user.is_active = True
            user.save()
            
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(data={"message", "Successfully authenticated"}, status=status.HTTP_200_OK)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        assert email_validation(email)
        assert password_validation(password)

        user = MyUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('Invalid email or password')
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid email or password')
        # This came from serializers.py
        token = MyTokenObtainPairSerializer.get_token(user)

        # Gives session id
        # login(request, user)
        response = Response()
        response.set_cookie(key='refresh-token', value=str(token), httponly=True)
        response.data = {'refresh': str(token), 'access': str(token.access_token)}
        return response
    
class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (SessionAuthentication,)
    def get(self, request):
        print(request.user)
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def post(self, request):
        # bearer_token = request.headers['Authorization']
        # access_token = bearer_token.replace('Bearer ', "")

        refresh_token = request.COOKIES['refresh-token']
        token = RefreshToken(refresh_token)
        token.blacklist()
        response = Response()
        response.delete_cookie('refresh-token')
        response.data = {"message": "Successfully logout"}
        return response




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        return Response({"custom_key": "custom message"}, status=401)

    # else
    # default case
    return exception_handler(exc, context)

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)