from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('login', views.login_page),
    path('register', views.registration_page),
    path('registring', views.registration),
    path('loging_in', views.loging_in),
    path('logout', views.logout)
]
