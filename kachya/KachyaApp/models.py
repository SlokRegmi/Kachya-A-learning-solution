from django.db import models

# Create your models here.
class StudentProfile(models.Model):
    Studentname = models.CharField(max_length=100)
    StudentEmail = models.EmailField(max_length=100)
    StudentPassword = models.CharField(max_length=100)

    def __str__(self):
        return self.Studentname
class TeacherProfile(models.Model):
    Teachername = models.CharField(max_length=100)
    TeacherEmail = models.EmailField(max_length=100)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # Add this line

    def __str__(self):
        return self.Teachername