from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin', views.admin, name="user-lists"),
    path('delete_user', views.delete_user, name='delete-user'),
]
