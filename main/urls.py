from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.main_page, name='index'),
    path("404/", views.page_not_found_view, name='error'),
    path('account/', views.account, name='account'),
    path('filmpage/', views.filmpage, name='filmpage'),
    path('serialpage/', views.serialpage, name='serialpage'),
    path("film/<int:pk>", views.film_detail, name='film_detail'),
    path('list-of-films/', views.list_of_films, name='list_of_films'),

    # доступна только через почту (не трогать)
    path('recovery-new-password/', views.recovery_new_password, name='recovery_new_password'),
    # доступна только через почту (не трогать)
    path('change-new-password/', views.change_new_password, name='change_new_password'),
    # доступна только через почту (не трогать)
    path("recovery-page/", views.recovery_page, name="recovery_page"),

    path('recovery-email/', views.recovery_page_email),

    path('sign-up-page/', views.sign_up_page, name='sign_up_page'),
    path("films_genres/", views.films_genres, name="films_genres"),
    path("moderator/", views.moderator, name="moderator"),  # доступна только модератору
    path("sign-in-page/", views.sign_in_page, name="sign_in_page"),
    path("sign-up-email/", views.sign_up_email, name="sign_up-email"),

    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('reset/<slug:uidb64>/<slug:token>/', views.set_recovery_pass, name='reset'),

    path('about', views.main_page, name='about'),



    path('slatt',views.slatt)

]
