"""my_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from account_app import views
from django.views.static import serve

urlpatterns = [
    path('', views.loginRedirect),
    path('register/', views.register),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('me/', views.me),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout),
    path('server/',views.landing,name='landing'),
    path('upload/',views.upload),
    path('main/',views.main),
    path('checkfile/', views.checkfile),
    re_path(r'^upload/pic/(?P<path>.*)$', serve, {'document_root': 'F:\\final\pic'}),
    re_path(r'^main/pic/(?P<path>.*)$', serve, {'document_root': 'F:\\final\pic'})
]
