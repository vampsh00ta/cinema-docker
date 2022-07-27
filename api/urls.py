from django.urls import path,include,re_path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
# from rest_framework_jwt.views import verify_jwt_token,obtain_jwt_token

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('get/',views.List.as_view(),name = 'get_users'),
    path('film/', views.FilmListView.as_view(), name='get_films'),

    path('logIn',views.LogIn.as_view()),
    path('signUp', views.SignUp.as_view()),
    path('logOut', views.LogOut.as_view()),
    path('addFavFilm', views.addFavFilm),
    path('delFavFilm', views.delFavFilm),
    path('resetPass', views.PassRecovery.as_view()),
    path('changePass', views.ChangePass.as_view()),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]