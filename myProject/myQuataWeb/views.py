from django.shortcuts import render, redirect
from .models import Subject ,Student
# Create your views here.


def home(request):
    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Student.objects.get(stu_id=username, password=password)
            print("เจอแล้ว!")
            return render(request, 'myQuota.html')  
        except Student.DoesNotExist:
            print("ไม่เจอ!")
            return redirect('/')
            
    else:
        return render(request, "home.html")

def myQuota(request):
    return render(request, "myQuota.html")

def findSub(request):
    subjects = Subject.objects.all().values("sub_id",
    "code",
    "sub_name",
    "faculty",
    "quota_limit",
    "semester",
    "status")
    return render(request, "findSub.html" , {'subjects': list(subjects)})

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        repeat_password = request.POST["repeat_password"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        faculty = request.POST["faculty"]
        profile_pic = request.FILES.get("profile_pic")

        # ตรวจสอบชื่อผู้ใช้งาน
        if Student.objects.filter(stu_id=username).exists():
            return redirect('/register')

        # ตรวจสอบรหัสผ่าน
        if password != repeat_password:
            return redirect('/register')

        # บันทึกข้อมูลนักเรียนใหม่
        student = Student.objects.create(
            stu_id=username,
            password=password,
            first_name=firstname,
            last_name=lastname,
            faculty=faculty,
             profile_pic=profile_pic if profile_pic else 'media/profile_photos/default.jpg',
        )

        return redirect('/')

    return render(request, 'register.html')
