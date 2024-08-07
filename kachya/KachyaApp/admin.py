from django.contrib import admin
from KachyaApp.models import  StudentProfile, TeacherProfile,Course,Assignment,Submission
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Submission)


# Register your models here.
