import json
import os
from django.test import TestCase,Client
from django.urls import reverse
from app_user.forms import StudentForm, UserRegisterForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from myQuataWeb.models import Student
from unittest.mock import patch

# Create your tests here.

class RegisterViewTest(TestCase):

    def setUp(self):
        self.register_url = reverse('register')


    def test_get_register_page(self):
        c=Client()
        response = c.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertIsInstance(response.context['user_form'], UserRegisterForm)
        self.assertIsInstance(response.context['student_form'], StudentForm)

    def test_post_valid_data(self):

        c=Client()
        
        user_data = {
            "username": "testcase",
            "password1": "test1Password!",
            "password2": "test1Password!"
        }

        student_data = {
            "first_name": "John",
            "last_name": "Lennon",
            "faculty": "Engineering",
            "profile_pic" : "media/profile_photos/R.jpg"
        }

        response = c.post(self.register_url, {**user_data, **student_data}, follow=True)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username="testcase").exists())
        self.assertTrue(Student.objects.filter(stu_id="testcase").exists())

    def test_post_not_valid_user_data(self):
        c = Client()
    
        user_data = {
        "username": "",  
        "password1": "test1Password!",
        "password2": "test1Password!"
        }

        response = c.post(self.register_url, user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertFalse(User.objects.exists())

    def test_post_not_valid_student_data(self):
        c = Client()
    
        student_data = {
            "first_name": "John",
            "last_name": "",
            "faculty": "Engineering",
            "profile_pic" : "media/profile_photos/R.jpg"
        }

        response = c.post(self.register_url, student_data, follow=False)  
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertFalse(Student.objects.exists())

    def test_post_no_profile_pic(self):
        c = Client()
        user_data = {
            "username": "testuser2",
            "password1": "complex_password_123",
            "password2": "complex_password_123",
        }
        student_data = {
            "first_name": "Test2",
            "last_name": "User2",
            "faculty": "Engineering",
        }
        response = c.post(self.register_url, {**user_data, **student_data}, follow=True)
        self.assertEqual(response.status_code, 200)  
        student = Student.objects.get(stu_id="testuser2")
        self.assertEqual(student.profile_pic.url, '/media/media/profile_photos/default.jpg')

    def test_add_quota_request_subject_does_not_exist(self):
        '''test เมื่อ add_quota_request แล้วไม่มีวิชานั้น'''
        data = {
            'sub_id': "999"  
        }

       
        with patch('myQuataWeb.models.Subject.objects.get', side_effect=Subject.DoesNotExist):
            response = self.client.post(
                reverse('add_quota_request'),
                data=json.dumps(data),
                content_type='application/json'
            )

        # ตรวจสอบ response status และ error message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": False, "error": "Invalid student or subject."})

    def test_add_quota_request_invalid_method(self):
        '''ทดสอบว่า add_quota_request จะตอบกลับ error กรณีที่ไม่ใช่ POST method ได้หรือไม่'''

        response = self.client.get(reverse('add_quota_request'))
    
        # ตรวจสอบว่า status code เป็น 200 เมื่อ method ไม่ใช่ POST
        self.assertEqual(response.status_code, 200)
        # ตรวจสอบว่า JSON response มีข้อความ error ที่ถูกต้อง
        self.assertEqual(response.json(), {"success": False, "error": "Invalid request method."})

    
    def test_cancel_quota_request_invalid_method(self):
        '''ทดสอบว่า cancel_quota_request จะตอบกลับ error กรณีที่ไม่ใช่ POST method ได้หรือไม่'''

        response = self.client.get(reverse('cancel_quota_request', kwargs={
            'student_id': self.student2.user_id,
            'subject_id': self.subject2.sub_id,
        }), content_type='application/json')

        # ตรวจสอบว่า status code เป็น 400 เมื่อ method ไม่ใช่ POST
        self.assertEqual(response.status_code, 400)
        # ตรวจสอบว่า JSON response มีข้อความ error ที่ถูกต้อง
        self.assertEqual(response.json(), {'status': 'error', 'message': 'Invalid request method'})

        


    
    

