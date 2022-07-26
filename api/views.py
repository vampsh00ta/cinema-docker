from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication

from main.models import Film
from django.contrib.auth import get_user_model
from rest_framework import status,generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


from django.http import JsonResponse
from datetime import datetime, timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .token import token_generator
from django.core.mail import send_mail
import pytz
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

utc = pytz.UTC
expiration_time = 5



# class CustomAuthToken(ObtainAuthToken):
#
#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         response = Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })
#         response['www-authenticate'] = 'Basic realm="My Realm'
#         return response


class LogIn(APIView):
    permission_classes = []
    def post(self,request,format = None):
        data = request.data

        user = authenticate(username=data['email'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'login_pass': True})
            else:
                return JsonResponse({'login_pass': False})
        else:
            return JsonResponse({'login_pass': None})

        return HttpResponse(status=status.HTTP_200_OK)

class LogOut(APIView):
    permission_classes = []

    def post(self,request,format = None):
        logout(request)
        return HttpResponse(status=status.HTTP_200_OK)

class SignUp(APIView):
    permission_classes = []

    def post(self,request,format = None):
        data = request.data
        try:
            user = get_user_model().objects.create_user(email=data['email'], password=data['password'],
                                                        username=data['username'])
        except:
            return JsonResponse({"user_reg": True})
        user.is_active = False
        table_expire_datetime = datetime.now() + timedelta(minutes=expiration_time)
        expired_on = table_expire_datetime.replace(tzinfo=utc)
        user.verif_time = expired_on
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activation link has been sent to your email'
        message = render_to_string('main/email/email-registration.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        })

        send_mail(
            mail_subject,
            message,
            'opiumgang111@yandex.ru',
            [data['email']],
            fail_silently=False,
        )

        request.session['email'] = data['email']
        return HttpResponse(status=status.HTTP_200_OK)



@api_view(['POST'])
@login_required()
def addFavFilm(request):
    user = request.user
    data = request.data
    movie_type = data['movie_type']
    movie_id = int(str(data['movie_id'])[0])
    if movie_type == 'film':
        try:
            movie = Film.objects.get(id=movie_id)
            user.fav_films.add(movie)
            return JsonResponse({'done': True})
        except:
            return JsonResponse({'status': 'failed to fetch the film'})
    elif movie_type == 'serial':
        pass
    elif movie_type == 'episode':
        pass
    return JsonResponse({'done': False})

@api_view(['POST'])
@login_required()
def delFavFilm(request):
    user = request.user
    data = request.data
    movie_type = data['movie_type']
    movie_id = int(str(data['movie_id'])[0])
    if movie_type == 'film':
        try:
            movie = Film.objects.get(id=movie_id)
            user.fav_films.remove(movie)
            return JsonResponse({'done': True})
        except:
            return JsonResponse({'status': 'failed to fetch the film'})

    elif movie_type == 'serial':
        pass
    elif movie_type == 'episode':
        pass
    return JsonResponse({'done': False})

class ChangePass(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format = None):
        data = request.data
        if data['password1'] == data['password2']:
            user = request.user

            user.set_password(data['password1'])
            user.save()
            login(request, user)
            return JsonResponse({"result": True})
        return JsonResponse({"result": False}, status=status.HTTP_400_BAD_REQUEST)

class PassRecovery(APIView):
    permission_classes = []

    def post(self,request,format = None):
        data = request.data
        user = get_user_model().objects.get(email=data['email'])

        if user:
            table_expire_datetime = datetime.now() + timedelta(minutes=expiration_time)
            expired_on = table_expire_datetime.replace(tzinfo=utc)
            user.verif_time = expired_on
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Reset link has been sent to your email'
            print(1)

            message = render_to_string('main/email/email-recovery.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })
            print(2)
            send_mail(
                mail_subject,
                message,
                'opiumgang111@yandex.ru',
                [data['email']],
                fail_silently=False,
            )

            request.session['email'] = data['email']
            return HttpResponse(200)

class UsersListView(generics.ListAPIView):
    queryset =     get_user_model().objects.all()
    serializer_class = CustomerSelializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)

class FilmListView(generics.ListAPIView):
    queryset =     Film.objects.all()
    serializer_class = FilmsSelializer
    permission_classes = [IsAdminUser,]

class List(APIView):
    permission_classes = []
    def get(self,request):
        print(request.META.get('HTTP_AUTHORIZATION'))
        return HttpResponse("penis")

