from django.shortcuts import render
from .models import Subject
# Create your views here.

def home(request):
    return render(request, "home.html")

def myQuota(request):
    return render(request, "myQuota.html")

def result(request):
    return render(request, "result.html")

def waitList(request):
    return render(request, "waitList.html")

def findSub(request):
    subjects = Subject.objects.all().values("sub_id",
    "code",
    "sub_name",
    "faculty",
    "quota_limit",
    "semester",
    "status")
    return render(request, "findSub.html" , {'subjects': list(subjects)})

def setting(request):
    return render(request, "setting.html")
