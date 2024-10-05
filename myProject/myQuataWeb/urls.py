from django.urls import path
from myQuataWeb import views

urlpatterns = [
    path('', views.home),
    path('myQuota', views.myQuota),
    path('findSub', views.findSub),
    path('register', views.register),
    path('login', views.login),
    
    path('add-quota-request/', views.add_quota_request, name='add_quota_request'),
    path('cancel-quota-request/<int:student_id>/<int:subject_id>/', views.cancel_quota_request, name='cancel_quota_request'),
    path('', views.greeting, name='greeting'),
    path('home', views.home, name='home'),
    path('myQuota', views.myQuota, name='myQuota'),
    path('findSub', views.findSub, name='findSub'),

]

