from django.urls import path
from . import views


urlpatterns = [
    path('logIn',views.logIn),
    path('signUp', views.signUp),
    path('logOut', views.logOut),
    path('addFavFilm', views.addFavFilm),
    path('delFavFilm', views.delFavFilm),
    path('resetPass', views.passRecovery),
    path('changePass', views.change_pass),
]