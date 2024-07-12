from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True)
    Studentname = models.CharField(max_length=100, null=True)
    StudentEmail = models.EmailField(max_length=100, null=True)
    StudentPassword = models.CharField(max_length=100, null=True)
    course_taken = models.CharField(max_length=100, null=True)
    assignment_completed = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.Studentname

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True)
    Teachername = models.CharField(max_length=100, null=True)
    TeacherEmail = models.EmailField(max_length=100, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    assgined_course = models.CharField(max_length=100, null=True)
    hired = models.BooleanField(null=True)
    password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.Teachername

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=100, null=True)
    course_description = models.TextField(null=True)
    course_live = models.BooleanField(null=True)
    course_picture = models.ImageField(upload_to='course_pictures/', blank=True, null=True)
    no_of_assignment = models.IntegerField(null=True)
    course_category = models.CharField(max_length=100, null=True)
    schedule = models.DateTimeField(null=True)
    course_price = models.IntegerField(null=True)

    def __str__(self):
        return self.course_name

class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_name = models.CharField(max_length=100, null=True)
    assignment_description = models.TextField(null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    due_date = models.DateField(null=True)
    assignment_file = models.FileField(upload_to='assignments/', blank=True, null=True)

    def __str__(self):
        return self.assignment_name
