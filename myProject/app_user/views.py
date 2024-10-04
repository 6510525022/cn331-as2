from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from myQuataWeb.models import Student

def register(request):
    return render(request, 'registration/register.html')





    # if request.method == "POST":
    #     username = request.POST["username"]
    #     password = request.POST["password"]
    #     repeat_password = request.POST["repeat_password"]
    #     firstname = request.POST["firstname"]
    #     lastname = request.POST["lastname"]
    #     faculty = request.POST["faculty"]
    #     profile_pic = request.FILES.get("profile_pic")

    #     # ตรวจสอบชื่อผู้ใช้งาน
    #     if Student.objects.filter(stu_id=username).exists():
    #         return redirect('/register')

    #     # ตรวจสอบรหัสผ่าน
    #     if password != repeat_password:
    #         return redirect('/register')

    #     # บันทึกข้อมูลนักเรียนใหม่
    #     student = Student.objects.create(
    #         stu_id=username,
    #         password=password,
    #         first_name=firstname,
    #         last_name=lastname,
    #         faculty=faculty,
    #          profile_pic=profile_pic if profile_pic else 'media/profile_photos/default.jpg',
    #     )

    #     return redirect('/')

    # return render(request, 'register.html')