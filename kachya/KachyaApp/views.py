from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login, logout
from KachyaApp.models import StudentProfile, TeacherProfile  

# Create your views here.
def index(request):

    return render (request, "login_student.html")
def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('email_login_student')
        password = request.POST.get('pass_login_student')
        if TeacherProfile.objects.filter(TeacherEmail=username).exists():
            user = auth.authenticate(email=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect ('dashboard_teacher/'+username)
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('login_student')
        else:
            user = auth.authenticate(email=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect ('dashboard_student/'+username)
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('login_student')
    
    else:
        return render(request, 'login_student.html')
    

def SignUpStudent(request):
     if request.method == 'POST':
        Studentname = request.POST.get('Student_Name')
        StudentEmail = request.POST.get('Student_Email')
        StudentPassword = request.POST.get('Student_Password1')
        StudentConfirmPassword = request.POST.get('Student_Password2')
        
        
        if TeacherProfile.objects.filter (TeacherEmail=StudentEmail).exists():
            messages.info(request, "Teacher Email Can't be a student email")
            return redirect('SignUpStudent')
        
        else:
            if StudentPassword == StudentConfirmPassword:
                
                if StudentProfile.objects.filter (StudentEmail=StudentEmail).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('SignUpStudent')
            
                else: 
                    user = User.objects.create_user(username=Studentname, email=StudentEmail, password=StudentPassword)
                    user.save()
                    student_profile = StudentProfile.objects.create(Studentname=Studentname, StudentEmail=StudentEmail, StudentPassword=StudentPassword, StudentConfirmPassword=StudentConfirmPassword)
                    student_profile.save()

                    return render(request, 'login_student.html')
            else:
                messages.info(request, 'Password not matching')
                return redirect('SignUpStudent')
     else:
        return render(request, 'signup.html')


def SignUpTeacher(request):
    if request.method == 'POST':
        teacher_name = request.POST.get('Teacher_Name')
        teacher_email = request.POST.get('Teacher_Email')
        teacher_password1 = request.POST.get('Teacher_Password1')
        teacher_password2 = request.POST.get('Teacher_Password2')
        resume = request.FILES.get('resume')  # Get the uploaded file

        if StudentProfile.objects.filter(email=teacher_email).exists():
            messages.info(request, "Student Email Can't be a teacher email")
            return redirect('SignUpTeacher')

        if teacher_password1 != teacher_password2:
            messages.info(request, 'Password not matching')
            return redirect('SignUpTeacher')

        if TeacherProfile.objects.filter(email=teacher_email).exists():
            messages.info(request, 'Email Taken')
            return redirect('SignUpTeacher')

        user = User.objects.create_user(username=teacher_name, email=teacher_email, password=teacher_password1)
        user.save()
        
        teacher_profile = TeacherProfile.objects.create(Teachername = teacher_name, TeacherEmail = teacher_email, resume=resume)
        teacher_profile.save()

        return render(request, 'login_teacher.html')
    else:
        return render(request, 'signup_teacher.html')

def about(request):

    return render (request, "about.html")  
 