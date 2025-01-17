from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime




class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(null=True)
    username = models.CharField(max_length=100, null=True)
    Teachername = models.CharField(max_length=100, null=True)
    TeacherEmail = models.EmailField(max_length=100, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    assgined_course = models.CharField(max_length=100, null=True)
    hired = models.BooleanField(null=True)
    password = models.CharField(max_length=100, null=True)
    nextclassSchedule = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.nextclassSchedule:
            # Preserve the time part of nextclassSchedule
            original_time = self.nextclassSchedule.time()
            # Update only the date part to today's date
            self.nextclassSchedule = datetime.combine(date.today(), original_time)
        super(TeacherProfile, self).save(*args, **kwargs)

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
    teacher_teaching = models.CharField(max_length=100, null=True)
    course_requirement = models.TextField(null=True)
    course_small_description = models.TextField(null=True)
    zoom_link = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.course_name

class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_name = models.CharField(max_length=100, null=True)
    assignment_description = models.TextField(null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=100, null=True)
    due_date = models.DateField(null=True)
    assignment_file = models.FileField(upload_to='assignments/', blank=True, null=True)
    remarks = models.TextField(null=True)
    teacher_id = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.assignment_name

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'due_date': self.due_date.strftime('%Y-%m-%d %H:%M:%S') if self.due_date else None,
        }

    


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
    
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.Studentname} - {self.assignment.assignment_name}"
    
