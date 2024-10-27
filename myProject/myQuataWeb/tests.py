from django.forms import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from .models import Student, Subject, QuotaRequest, Approval
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
import json

class QuotaAppTests(TestCase):

    def setUp(self):
        # สร้าง Subject สำหรับใช้ในการทดสอบ
        self.subject1 = Subject.objects.create(
            code="CN001",
            sub_name="Computer 001",
            faculty="Engineer",
            quota_limit=1,
            semester="Semester1",
            status="Open"
        )
        
        self.subject2 = Subject.objects.create(
            code="CN002",
            sub_name="Computer 002",
            faculty="Engineer",
            quota_limit=2,
            semester="Semester1",
            status="Open"
        )
        
        self.subject3 = Subject.objects.create(
            code="CN003",
            sub_name="Computer 003",
            faculty="Engineer",
            quota_limit=2,
            semester="Semester1",
            status="Close"
        )
        
        # สร้างผู้ใช้ (สำหรับการเข้าสู่ระบบ)
        
        self.client=Client()
        
        user_data = {
            "username": "testcase",
            "password1": "test1Password!",
            "password2": "test1Password!"
        }

        student_data = {
            "first_name": "Sakura",
            "last_name": "Haruka",
            "faculty": "Engineering",
            "profile_pic" : "media/profile_photos/R.jpg"
        }

        response = self.client.post(reverse('register'), {**user_data, **student_data}, follow=True)
        self.student1 = Student.objects.get(stu_id="testcase")
        
        user_data_2 = {
            "username": "6510685099",
            "password1": "test1!12312",
            "password2": "test1!12312"
        }

        student_data_2 = {
            "first_name": "Dora",
            "last_name": "Yaki",
            "faculty": "Engineering",
        }
        
        c=Client()
        response = c.post(reverse('register'), {**user_data_2, **student_data_2}, follow=True)
        self.student2 = Student.objects.get(stu_id="6510685099")
        
        self.quotaRequest1 = QuotaRequest.objects.create(user_id=self.student2, sub_id=self.subject1)
        self.approval1 = Approval.objects.create(request_id=self.quotaRequest1, decision="Approved")
        response = self.client.get(reverse('myQuota'))
        self.csrf_token = response.cookies.get('csrftoken').value
