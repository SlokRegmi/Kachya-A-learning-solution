from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Studentname = models.CharField(max_length=100)
    StudentEmail = models.EmailField(max_length=100)
    StudentPassword = models.CharField(max_length=100)

    def __str__(self):
        return self.Studentname

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Teachername = models.CharField(max_length=100)
    TeacherEmail = models.EmailField(max_length=100)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.Teachername
