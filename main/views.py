from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm
from .models import Comment, Film
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Customer
import json
from django.views.decorators.http import require_http_methods
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import token_generator
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.core import serializers
import pytz
from django.contrib.sessions.models import Session
from django.contrib.sessions.models import Session
import pickle

utc = pytz.UTC
expiration_time = 5


@require_http_methods(['POST'])
def logIn(request):
    data = json.loads(request.body)
    user = authenticate(username=data['email'], password=data['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            return JsonResponse({'login_pass': True})
        else:
            return JsonResponse({'login_pass': False})
    else:
        return JsonResponse({'login_pass': None})

    return HttpResponse(200)






def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        if datetime.now().replace(tzinfo=utc) > user.verif_time:
            user.verif_time = None
            return HttpResponse('Activation link has expired!')

        user.is_active = True
        user.save()
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')


def main_page(request):

    context = {'films': Film.objects.all()}
    return render(request, 'main/main_page.html', context=context)


def film_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    user = request.user
    if user.is_authenticated:
        return render(request, 'main/filmpage.html', {'film': film, 'fav_films': user.fav_films})


    return render(request, 'main/filmpage.html', {'film': film})


def comment_detail(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.Commment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.rating = form.cleaned_data['rating']
                comment.save()
                return redirect('')
    form = CommentForm()
    return render(request, 'main/filmpage.html', {'form': form})


@login_required()
def account(request):
    user = request.user

    return render(request, 'main/account.html',{"user":user})


def filmpage(request):
    return render(request, 'main/filmpage.html')


def list_of_films(request):
    return render(request, "main/List of films from user's account.html")


def recovery_new_password(request):
    return render(request, "main/recovery-new-password.html")


@login_required()
def change_new_password(request):
    return render(request, "main/change-new-password.html")


def sign_up_page(request):
    return render(request, "main/sign-up-page.html")


def films_genres(request):
    return render(request, 'main/Films sorted by genre.html')


def moderator(request):
    return render(request, 'main/moderator account.html')


def recovery_page(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/')
    return render(request, 'main/recovery-page.html')


def sign_in_page(request):
    return render(request, 'main/sign-in-page.html')


def sign_up_email(request):
    email = request.COOKIES.get('email')
    if email:
        response = render(request, 'main/sign-up-email.html', {'email': email})
        response.delete_cookie('email')
        return response
    return redirect('/')


def set_recovery_pass(request, token, uidb64):
    User = get_user_model()
    INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"
    reset_url_token = 'set-password'

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if request.method == 'GET':
        if token != reset_url_token:

            if user is not None and token_generator.check_token(user, token):
                if datetime.now().replace(tzinfo=utc) > user.verif_time:
                    user.verif_time = None
                    return HttpResponse('Activation link has expired!')
                request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                redirect_url = request.path.replace(
                    token, reset_url_token
                )
                return redirect(redirect_url)
            else:
                return HttpResponse('Activation link is invalid!')

        else:
            session_token = request.session.get(INTERNAL_RESET_SESSION_TOKEN)
            if token_generator.check_token(user, session_token):
                return render(request, 'main/recovery-new-password.html')
    elif request.method == "POST":
        session_token = request.session.get(INTERNAL_RESET_SESSION_TOKEN)
        if user is not None and token_generator.check_token(user, session_token):
            data = json.loads(request.body)
            if data['password1'] != data['password2']:
                return JsonResponse({'status': False})
            user.set_password(data['password1'])
            user.save()
            login(request, user)
            del request.session[INTERNAL_RESET_SESSION_TOKEN]
            return JsonResponse({'status': True})
        pass








def recovery_page_email(request):
    email = request.session.get('email')
    if email:
        del request.session['email']
        return render(request, 'main/recovery-page-email.html', {'email': email})
    else:
        return redirect('/')


def serialpage(request):
    return render(request, 'main/serialpage.html')


def page_not_found_view(request):
    return render(request, 'main/404.html')
