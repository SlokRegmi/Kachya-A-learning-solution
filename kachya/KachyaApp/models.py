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


class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=100)
    course_description = models.TextField()
    course_live = models.BooleanField()
    course_picture = models.ImageField(upload_to='course_pictures/', blank=True, null=True)


    def __str__(self):
        return self.course_name

class Assignment (models.Model):
    assignment_id = models.IntegerField(primary_key=True)
    assignment_name = models.CharField(max_length=100)
    assignment_description = models.TextField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    assignment_file = models.FileField(upload_to='assignments/', blank=True, null=True)

    def __str__(self):
        return self.assignment_name