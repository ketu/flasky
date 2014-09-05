#/usr/bin/env python
#-*- coding:utf8 -*-


from helper.urls import patterns

from .views import ProfileView,LoginView,RegisterView,LogoutView

urlpatterns = ("/account",
    ('/profile/', ProfileView.as_view('profile',template = 'profile.html')),
    ('/login/', LoginView.as_view('login',template = 'login.html')),
    ('/register/', RegisterView.as_view('register',template = 'register.html')),
    ('/logout/', LogoutView.as_view('logout',template = 'logout.html')),
)

