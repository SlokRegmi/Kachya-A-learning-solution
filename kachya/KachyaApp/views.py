
import logging
import traceback
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login, logout
from KachyaApp.models import StudentProfile, TeacherProfile  

# Create your views here.
def index(request):

    return render (request, "index.html")

def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('email_login_student')
        password = request.POST.get('pass_login_student')

      #  if not User.objects.filter(username=username).exists():
       #     messages.info(request, 'Invalid Credentials')
        #    return redirect('login_student')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if TeacherProfile.objects.filter(user=user).exists():
                return redirect('dashboard_teacher/' + username)
            elif StudentProfile.objects.filter(user=user).exists():
                return redirect('dashboard_student/' + username)
            else:
                messages.info(request, 'Profile not found')
                return redirect('login_student')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login_student')

    else:
        return render(request, 'login_student.html')

def SignUpStudent(request):
    if request.method == 'POST':
        student_name = request.POST.get('Student_Name')
        student_email = request.POST.get('Student_Email')
        student_password1 = request.POST.get('Student_Password1')
        student_password2 = request.POST.get('Student_Password2')

        if student_password1 == student_password2:
            if StudentProfile.objects.filter(StudentEmail=student_email).exists():
                messages.info(request, 'Email Taken')
                return redirect('SignUpStudent')
            else:
                try:
                    user = User.objects.create_user(username=student_name, email=student_email, password=student_password1)
                    user.save()
                    StudentProfile.objects.create(user=user, Studentname=student_name, StudentEmail=student_email, StudentPassword=student_password1)
                    return render(request, 'login_student.html')
                except Exception as e:
                   
                    messages.error(request, 'An error occurred during sign up')
                    return redirect('SignUpStudent')
        else:
            messages.info(request, 'Password not matching')
            return redirect('SignUpStudent')
    else:
        return render(request, 'signup_student.html')

def SignUpTeacher(request):
    if request.method == 'POST':
        teacher_name = request.POST.get('Teacher_Name')
        teacher_email = request.POST.get('Teacher_Email')
        teacher_password1 = request.POST.get('Teacher_Password1')
        teacher_password2 = request.POST.get('Teacher_Password2')
        resume = request.FILES.get('resume')

        if teacher_password1 == teacher_password2:
            if StudentProfile.objects.filter(StudentEmail=teacher_email).exists():
                messages.info(request, "Student Email Can't be a teacher email")
                return redirect('SignUpTeacher')

            if User.objects.filter(email=teacher_email).exists():
                messages.info(request, 'Email Taken')
                return redirect('SignUpTeacher')
            else:
                try:
                    user = User.objects.create_user(username=teacher_name, email=teacher_email, password=teacher_password1)
                    user.save()
                    TeacherProfile.objects.create(user=user, Teachername=teacher_name, TeacherEmail=teacher_email, resume=resume)
                    return render(request, 'login_student.html')
                except Exception as e:
                    logger.error("Database error: %s", e)
                    logger.error(traceback.format_exc())
                    messages.error(request, 'An error occurred during sign up')
                    return redirect('SignUpTeacher')
        else:
            messages.info(request, 'Password not matching')
            return redirect('SignUpTeacher')
    else:
        return render(request, 'singup_teacher.html')
