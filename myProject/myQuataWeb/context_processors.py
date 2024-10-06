from django.contrib.auth.models import User
from .models import Student

def student_processor(request):
    student = None
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(stu_id=request.user)
        except Student.DoesNotExist:
            student = None
    return {'student': student}
