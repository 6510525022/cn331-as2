from django.db import models
from django.core.exceptions import ValidationError
import os

# Create your models here.

class Student(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    stu_id = models.CharField(max_length=10, unique=True)
    faculty = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='media/profile_photos/', blank=True, null=True)
    
    def __str__(self):
        return f"user_id: {self.user_id} stu_id: {self.stu_id}, name: {self.first_name} {self.last_name}, faculty:{self.faculty}"


class Subject(models.Model):
    SEM1 = "semester1"
    SEM2 = "semester2"
    OP = "Open"
    CL = "Close" 
    STA_DICT = {
        OP: "Open",
        CL : "Close"
    }
    SEM_DICT = {
        SEM1 : "Semester1",
        SEM2 : "semester2"
    }
    sub_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=5)
    sub_name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    quota_limit = models.IntegerField(default=9999)
    semester = models.CharField(choices=SEM_DICT, max_length=20)
    status = models.CharField(choices=STA_DICT, max_length=10)

    def __str__(self):
        return f"id: {self.sub_id}, code: {self.code}, limit: {self.quota_limit} semester: {self.semester} status: {self.status}"


class QuotaRequest(models.Model):
    YES = "Y"
    NO = "N"
    WAIT = "W"
    STATUS_DICT = {
        YES: 'Approved',
        NO: 'Denied',
        WAIT: 'Wait'
    }
    request_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="quota_requests")
    status = models.CharField(choices=STATUS_DICT, default=WAIT, max_length=30)
    sub_id = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="quota_requests")

    def clean(self):
        # ตรวจสอบว่า quota_limit เกินแล้วหรือยัง
        if self.sub_id.quota_requests.count() >= self.sub_id.quota_limit:
            raise ValidationError(f"The quota limit for {self.sub_id.sub_name} has been reached.")

        # ตรวจสอบว่าวิชานั้นถูกปิดหรือไม่
        if self.sub_id.status == 'Close':
            raise ValidationError(f"Subject {self.sub_id.sub_name} is closed and not accepting quota requests.")

    def save(self, *args, **kwargs):
        # เรียก clean() ก่อนทำการบันทึกเพื่อการตรวจสอบ
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Request {self.request_id} by {self.user_id.stu_id} {self.user_id.first_name} {self.user_id.last_name}"


class Approval(models.Model):
    apprv_id = models.AutoField(primary_key=True)
    request_id = models.ForeignKey(QuotaRequest, on_delete=models.CASCADE, related_name="approvals")
    approval_date = models.DateField(auto_now_add=True) 
    decision = models.CharField(max_length=10, choices=[("Approved", "Approved"), ("Denied", "Denied")])

    def __str__(self):
        return f"Approval {self.approval_date} for Request {self.request_id}"