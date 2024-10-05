import json
from django.shortcuts import render, redirect
from .models import Subject ,Student, QuotaRequest, Approval
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
# Create your views here.

student_id = 12

def greeting(request):
    return render(request, 'greeting.html')

def home(request):
    current_user = request.user
    student = Student.objects.filter(stu_id=current_user.username).first()
    return render(request, "home.html", {'student': student})

def myQuota(request):
    subjects = Subject.objects.all().values("sub_id",
    "code",
    "sub_name",
    "faculty",
    "quota_limit",
    "semester",
    "status")
    MyQuota = get_subjects_with_Approval_Approval(student_id)
    waitList = get_subjects_without_Approval(student_id)
    Result = get_subjects_with_Approval_Denied(student_id)
    return render(request, "myQuota.html", 
                  {'subjects': list(subjects),
                   'myQuota': MyQuota,
                   'waitList': waitList,
                   'result': Result}
                  )

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

def login(request):
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
        return render(request, "login.html")


#แสดงใน findsub
def get_subjects_without_quota_request_by_student(student_id):
    requested_subjects = QuotaRequest.objects.filter(user_id=student_id).values_list('sub_id', flat=True)
    subjects_without_request = Subject.objects.exclude(sub_id__in=requested_subjects).values(
    "sub_id",
    "code",
    "sub_name",
    "faculty",
    "quota_limit",
    "semester",
    "status")
    
    return subjects_without_request

#แสดงใน MyQuata
def get_subjects_with_Approval_Approval(student_id):
    approval_subjects = Subject.objects.filter(
        quota_requests__user_id=student_id,
        quota_requests__approvals__decision="Approved"
    ).values(
    "sub_id",
    "code",
    "sub_name",
    "faculty",
    "quota_limit",
    "semester",
    "status")
    
    return approval_subjects

#แสดงใน MyQuata
def get_subjects_with_Approval_Denied(student_id):
    result_subjects = Subject.objects.filter(
        quota_requests__user_id=student_id,
        quota_requests__approvals__decision="Denied"
    ).values(
    "sub_id",
    "code",
    "sub_name",
    "faculty",
    "quota_limit",
    "semester",
    "status")
    
    return result_subjects

#แสดงใน MyQuata
def get_subjects_without_Approval(student_id):
    subjects_without_approval = Subject.objects.filter(
        quota_requests__user_id=student_id
    ).filter(quota_requests__approvals__isnull=True).values(
    "sub_id",
    "code",
    "sub_name",
    "faculty",
    "quota_limit",
    "semester",
    "status")
    
    return subjects_without_approval




    
#findSub Request
def add_quota_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student_id = data.get("student_id")
        sub_id = data.get("sub_id")

        try:
            student = Student.objects.get(user_id=student_id)
            subject = Subject.objects.get(sub_id=sub_id)

            # Check if the student has already requested this quota
            existing_request = QuotaRequest.objects.filter(user_id=student, sub_id=subject).first()
            if existing_request:
                return JsonResponse({"success": False, "error": "Quota request already exists."})
            
            # Create a new quota request
            quota_request = QuotaRequest(user_id=student, sub_id=subject)
            quota_request.save()

            return JsonResponse({"success": True})
        except (Student.DoesNotExist, Subject.DoesNotExist):
            return JsonResponse({"success": False, "error": "Invalid student or subject."})
    
    return JsonResponse({"success": False, "error": "Invalid request method."})


def cancel_quota_request(request, student_id, subject_id):
    if request.method == 'POST':
        # ค้นหาคำขอตาม student_id และ subject_id
        quota_request = get_object_or_404(QuotaRequest, user_id=student_id, sub_id=subject_id)
        # ลบคำขอ
        quota_request.delete()
        return JsonResponse({'status': 'success', 'message': 'Request cancelled successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)