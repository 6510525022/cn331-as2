# Generated by Django 5.1.1 on 2024-10-04 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myQuataWeb', '0004_student_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='profile_pic',
        ),
    ]
