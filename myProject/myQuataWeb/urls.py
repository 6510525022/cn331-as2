from django.urls import path
from myQuataWeb import views

urlpatterns = [
    path('', views.greeting, name='greeting'),
    path('home', views.home, name='home'),
    path('myQuota', views.myQuota, name='myQuota'),
    path('findSub', views.findSub, name='findSub'),

]

