from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name = 'accounts/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name = 'authorisation/logout.html'),
         name='logout'),
    path('upgrade/', upgrade_me, name = 'upgrade')
]