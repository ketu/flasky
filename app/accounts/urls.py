#/usr/bin/env python
#-*- coding:utf8 -*-
from flask import Blueprint
from .views import LoginView, RegisterView, LogoutView,ProfileView



urlpatterns = (
    #('/dashboard/', RegisterView.as_view('register')),
    ('/profile/', ProfileView.as_view('profile')),
    #('/settings/', RegisterView.as_view('register')),
    ('/login/', LoginView.as_view('login', template = 'accounts/login.html')),
    ('/register/', RegisterView.as_view('register')),
    ('/logout/', LogoutView.as_view('logout')),
)