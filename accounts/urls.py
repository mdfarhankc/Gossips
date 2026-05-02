from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('sign-up/', views.signup, name='signup'),
    path('sign-in/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
]