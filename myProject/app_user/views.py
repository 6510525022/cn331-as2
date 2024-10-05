import json
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, StudentForm
from django.contrib.auth.models import User
from myQuataWeb.models import Student

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)  

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()  
            login(request, user)  

            profile_pic = student_form.cleaned_data.get('profile_pic') 
            if not profile_pic:  # ถ้าไม่มีการอัปโหลดไฟล์
                profile_pic = 'media/profile_photos/default.jpg'

            # บันทึกข้อมูลนักเรียน
            student = Student(
                first_name=student_form.cleaned_data['first_name'],
                last_name=student_form.cleaned_data['last_name'],
                stu_id=user.username,
                faculty=student_form.cleaned_data['faculty'],
                profile_pic=profile_pic, 
            )

            print(profile_pic)

            try:
                student.save() 
            except Exception as e:
                print(f"Error saving student: {e}")  

            return redirect('home')
    else:
        user_form = UserRegisterForm()
        student_form = StudentForm()

    context = {
        "user_form": user_form,
        "student_form": student_form,
    }
    return render(request, 'registration/register.html', context)
