from django.contrib import admin
from .models import StudentProfile, TeacherProfile, Course, Assignment


# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Course)
admin.site.register(Assignment)
