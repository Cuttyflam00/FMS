from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True),name='login'),
    path('userlogin', views.login_user, name="login-user"),
    path('user-register', views.registerUser, name="register-user"),
    path('logout',views.logoutuser,name='logout'),
    path('scanQRcode',views.scanQRcode,name='scanQRcode'),
    path('genQRcode',views.genQRcode,name='genQRcode'),
    # path('update-avatar',views.update_avatar,name='update-avatar'),
    path('', views.home, name='home-page'),
]
