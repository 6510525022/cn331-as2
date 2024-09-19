from django.shortcuts import render
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
    return render(request, "findSub.html")

def setting(request):
    return render(request, "setting.html")