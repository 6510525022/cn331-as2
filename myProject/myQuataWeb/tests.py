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

    def test_can_cancel_quota_request(self):
        """ทดสอบการยกเลิกคำขอโควต้า"""

        # จำลองการส่งคำขอผ่าน fetch (โดยใช้ client.post แทน)
        response = self.client.post(reverse('cancel_quota_request', kwargs={
            'student_id': self.student2.user_id,
            'subject_id': self.subject1.sub_id,
        }), content_type='application/json', HTTP_X_CSRFTOKEN=self.csrf_token)

        # ตรวจสอบการตอบสนอง
        self.assertFalse(QuotaRequest.objects.filter(user_id=self.student2, sub_id=self.subject1).exists())


    def test_cannot_cancel_quota_request(self):
        """ทดสอบการยกเลิกคำขอที่ไม่มีอยู่จริง"""
        
        # ส่งคำขอยกเลิกที่ไม่มีอยู่
        response = self.client.post(reverse('cancel_quota_request', kwargs={
            'student_id': self.student2.user_id,
            'subject_id': self.subject2.sub_id,
        }), content_type='application/json', HTTP_X_CSRFTOKEN=self.csrf_token)

        # ตรวจสอบการตอบสนอง
        self.assertEqual(response.status_code, 404)


    def test_add_quota_request(self):
        # จำลองการเข้าสู่ระบบก่อนทำคำขอโควต้า
        
        # ส่งคำขอโควต้า
        self.assertTrue(self.subject2.quota_count() == 0)
        data = {
            'sub_id': self.subject2.sub_id,
        }
                
        response = self.client.post(
            reverse('add_quota_request'), 
            data=json.dumps(data), 
            content_type='application/json'  # Ensure the request is sent as JSON
        )
        
        self.assertTrue(self.subject2.quota_count() == 1)
        
    def test_add_duplicate_quota_request(self):
        # ทดสอบการส่งคำขอโควต้าซ้ำ
        
        self.subject1.quota_limit = 2
        self.subject1.save()
        
        # สร้างคำขอแรก
        QuotaRequest.objects.create(user_id=self.student1, sub_id=self.subject1)
        
        # ส่งคำขอโควต้าอีกครั้ง
        response = self.client.post(reverse('add_quota_request'), json.dumps({
            "sub_id": self.subject1.sub_id
        }), content_type="application/json")
        
        self.assertEqual(json.loads(response.content)["error"], "Quota request already exists.")
        
    def test_add_closed_subject_quota_request(self):
        """ ทดสอบการส่งคำขอโควต้าของรายวิชาที่ปิดรับแล้ว """

        # สร้าง QuotaRequest ใหม่ แต่ยังไม่บันทึกลงฐานข้อมูล
        quota_request = QuotaRequest(user_id=self.student1, sub_id=self.subject3)

        # ตรวจสอบว่าเมื่อเรียก full_clean จะเกิด ValidationError ขึ้น
        with self.assertRaises(ValidationError) as cm:
            quota_request.full_clean()  # เรียกใช้ full_clean แทนที่จะเป็น save()
        
        # ตรวจสอบข้อความของ ValidationError
        self.assertEqual(
            str(cm.exception.messages[0]), 
            f"Subject {self.subject3.sub_name} is closed and not accepting quota requests."
        )


    def test_add_full_subject_quota_request(self):
        """ทดสอบการส่งคำขอโควต้าสำหรับรายวิชาที่เต็มแล้ว"""
        
        # ตั้ง quota_limit ให้ subject1 และบันทึกข้อมูล
        self.subject1.quota_limit = 1
        self.subject1.save()


        # สร้าง QuotaRequest ใหม่ แต่ยังไม่บันทึกลงฐานข้อมูล
        quota_request = QuotaRequest(user_id=self.student1, sub_id=self.subject1)

        # ตรวจสอบว่าเมื่อเรียก full_clean จะเกิด ValidationError ขึ้น
        with self.assertRaises(ValidationError) as cm:
            quota_request.full_clean()  # เรียกใช้ full_clean แทนที่จะเป็น save()
        
        # ตรวจสอบข้อความของ ValidationError
        self.assertEqual(
            str(cm.exception.messages[0]), 
            f"The quota limit for {self.subject1.sub_name} has been reached."
        )
    
    def test_cancel_quota_request(self):
        # จำลองการสร้างคำขอแล้วทำการยกเลิก
        
        # ยกเลิกคำขอ
        response = self.client.post(reverse('cancel_quota_request', args=[self.student1.user_id, self.subject1.sub_id]))
        
        self.assertFalse(QuotaRequest.objects.filter(user_id=self.student1, sub_id=self.subject1).exists())

    def test_myQuota_view(self):
        # จำลองการเข้าสู่ระบบและทดสอบการดึงข้อมูลในหน้า myQuota
        response = self.client.get(reverse('myQuota'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myQuota.html")
    
    def test_findSub_view(self):
        # จำลองการเข้าสู่ระบบและทดสอบการดึงข้อมูลในหน้า findSub
        response = self.client.get(reverse('findSub'))
        
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, "findSub.html")
