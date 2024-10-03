from django.urls import path
from myQuataWeb import views

urlpatterns = [
    path('', views.home),
    path('myQuota', views.myQuota),
    path('findSub', views.findSub),
    path('register', views.register),
]