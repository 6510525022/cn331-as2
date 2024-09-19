from django.urls import path
from myQuataWeb import views

urlpatterns = [
    path('', views.home),
    path('myQuota', views.myQuota),
    path('result', views.result),
    path('waitList', views.waitList),
    path('findSub', views.findSub),
    path('setting', views.setting),
]