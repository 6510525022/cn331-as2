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
        # photo = request.FILES.get("photo")

        if password != repeat_password:  
            # แสดงข้อความเตือน
            return redirect('/register')  # หรือ render กลับไปยัง template

        else:
            Student.objects.create(
                stu_id=username,
                password=password,
                first_name=firstname,
                last_name=lastname,
                faculty=faculty,
                # photo=photo,  # บันทึกภาพ
            )

            return render(request, 'home.html')
        
    return render(request, 'register.html')

