#/usr/bin/env python
#-*- coding:utf8 -*-

from .views import DashboardView, SettingsView,MessageView,AlertsView,TasksView,SearchView

urlpatterns = ("/system",
    ('/dashboard/', DashboardView.as_view('dashboard',template = 'dashboard.html')),

    ('/settings/', SettingsView.as_view('settings',template = 'settings.html')),
    ('/message/', MessageView.as_view('message',template = 'settings.html')),
    ('/alerts/', AlertsView.as_view('alerts',template = 'settings.html')),
    ('/tasks/', TasksView.as_view('tasks',template = 'settings.html')),
    ('/search/', SearchView.as_view('search',template = 'settings.html')),

)