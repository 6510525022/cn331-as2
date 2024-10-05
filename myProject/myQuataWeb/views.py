from django.shortcuts import render, redirect
from .models import Subject ,Student, QuotaRequest, Approval
from django.contrib.auth.models import User
# Create your views here.


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
    #MyQuota = get_subjects_with_Approval_Approval(student_id)
    #waitList = get_subjects_without_Approval(student_id)
    #Result = get_subjects_with_Approval(student_id)
    return render(request, "myQuota.html"  , {'subjects': list(subjects)})

def findSub(request):
    #subjects = get_subjects_without_quota_request_by_student(student_id)
    subjects = Subject.objects.all().values("sub_id",
    "code",
    "sub_name",
    "faculty",
    "quota_limit",
    "semester",
    "status")
    return render(request, "findSub.html" , {'subjects': list(subjects)})

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
def get_subjects_with_Approval(student_id):
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
