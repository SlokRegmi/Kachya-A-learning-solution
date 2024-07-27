
from audioop import reverse
from http.client import HTTPResponse
import json
import logging
import traceback
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login, logout
from KachyaApp.models import Assignment, Course, StudentProfile, TeacherProfile  
import google.generativeai as genai
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

import os
from datetime import datetime
import pytz
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    return render (request, "login_student.html")
def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('email_login_student')
        password = request.POST.get('pass_login_student')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if TeacherProfile.objects.filter(user=user).exists():
                usering = TeacherProfile.objects.get(user=user)
                courseslist = usering.assigned_course.split(",")  # Update this line with the correct attribute name
                classTime = usering.nextclassSchedule
                naive_dt = datetime.now()
                aware_naive_dt = pytz.utc.localize(naive_dt)

                if classTime is not None and aware_naive_dt < classTime:
                    classing = classTime.strftime("%H:%M:%S")
                    data = {
                        'username': usering.username,
                        'name': usering.Teachername,
                        'email': usering.TeacherEmail,
                        'courses': courseslist,
                        "nextclass": classing,
                        "is_today_class": "Today"
                    }
                    return render(request, 'dashboard_teacher.html', data)
                else:
                    classing = classTime.strftime("%H:%M:%S") if classTime else "N/A"
                    data = {
                        'username': usering.username,
                        'name': usering.Teachername,
                        'email': usering.TeacherEmail,
                        'courses': courseslist,
                        "nextclass": classing,
                        "is_today_class": "tomorrow" if classTime else "N/A"
                    }
                    return render(request, 'dashboard_teacher.html', data)
            elif StudentProfile.objects.filter(user=user).exists():
                susering = StudentProfile.objects.get(user=user)
                courseslist = susering.course_taken.split(",")
                name = susering.Studentname
                noofcourses = len(courseslist)
                course_id = []
                for course in courseslist:
                    try:
                        course_obj = Course.objects.get(course_name=course)
                        course_id.append(course_obj.course_id)
                    except Course.DoesNotExist:
                        print(f"Course does not exist: {course}")
                        continue
                assignments = []
                try:
                    for course in course_id:
                        assigns = Assignment.objects.filter(course_id=course)
                        for assign in assigns:
                            if assign.due_date is not None and assign.due_date < timezone.now():
                                assignments.append(assign)
                except Exception as e:
                    print(f"Error fetching assignments: {e}")

                noofassignments = len(assignments)

                # Set session data for the student
                data = {
                    'name': name,
                    'courses': courseslist,
                    "role": "Student",
                    "noofcourses": noofcourses,
                    "assignments": [assignment.to_dict() for assignment in assignments],  # Convert assignments to a serializable format
                    "noofassignments": noofassignments
                }
                return render(request,'dashboard_student.html',data)
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
        teacher_password1 = 'abc'
        teacher_password2 = 'abc'
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
                    messages.error(request, 'An error occurred during sign up')
                    return redirect('SignUpTeacher')
        else:
            messages.info(request, 'Password not matching')
            return redirect('SignUpTeacher')
    else:
        return render(request, 'singup_teacher.html')






def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            try:
                reply = get_gemini_reply(message+ "Write in maximum two lines and don't give Sure I'll tell you and all straight to the point and if I'm asking for code just give me straight up code no text and all not anything" )
                return JsonResponse({'reply': reply})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'No message provided'}, status=400)

def get_gemini_reply(message):
    api_key = ""
 
    genai.configure(api_key=api_key)
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(message)
        
        return response.text  
    except Exception as e:
        raise RuntimeError(f"Failed to get reply from Gemini API: {str(e)}")
    
    
    '''
    api_key = ''
    url = 'https://api.gemini.com/v1/some_endpoint'  # Replace with the actual Gemini API endpoint

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'input': message
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get('reply')
    else:
        return f"Error: {response.status_code} - {response.text}"
'''
def dashboard_teacher(request,data):


    

    return render(request, 'dashboard_teacher.html',{'username':data['username']})

@login_required
def dashboard_student(request,data):
    
    
    return render(request, 'dashboard_student.html',{'username':data['name']})


def course_category(request):
    if request.method == "GET":
        names = Course.objects.values_list('course_name', flat=True)
        names_json = json.dumps(list(names), cls=DjangoJSONEncoder)
        return render(request, 'course_category.html', {'names': names_json})
    else:
        return render(request, 'course_category.html')

@csrf_exempt
def submit_category(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        category = data.get('category')

        print(category)
        return JsonResponse({'redirect_url': f'/course_desc/?category={category}'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
def course_desc(request, category):
    try:
        course_description = Course.objects.get(course_name=category)
        coursereq = course_description.course_requirement
        listofcourserequire = coursereq.split('.')
    except Course.DoesNotExist:
        logging.error(f'Course with name {category} not found')

        # Handle the case where no course is found
    return render(request, 'course_desc.html', {
            'coursename': course_description.course_name,
            'course_description': course_description.course_description,
            'course_price': course_description.course_price,
            'teacher_teaching': course_description.teacher_teaching,
            'course_requirement': listofcourserequire,
            'course_small_description': course_description.course_small_description,
            'live': course_description.course_live,
            'course_schedule': course_description.schedule,
            'image': course_description.course_picture

        })

def cccc(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
     

        course = Course.objects.create(course_name=course_name)
        course.save()
        return redirect('cccc')
    else:
        return render(request, 'cccc.html')            
def assignment(request):
    if request.user.is_authenticated:
        sample_assignments = {
            "Python": [
                "Assignment 1",
                "Learn the basics of Python programming.",
                "2024-08-01"
            ],
            "Django": [
                "Assignment 2",
                "Build a simple Django application.",
                "2024-08-15"
            ],
            "JavaScript": [
                "Assignment 3",
                "Create a dynamic web page using JavaScript.",
                "2024-08-20"
            ]
        }

        courses = sample_assignments.keys()
        
        # Convert the dictionary to a JSON string
        assignments_json = json.dumps(sample_assignments)
        
        return render(request, 'courses.html', {
            'name': "Student Name",
            'courses': courses,
            'assignments': assignments_json
        })
    else:
        return redirect('login_student')
''' username = request.user.username
        StdProfile = StudentProfile.objects.get(Studentname=username)
        courses = StdProfile.course_taken.split(",")
        AssignmentHaruBhako = {}

        for course in courses:
            try:
                course_obj = Course.objects.get(course_name=course)
            except Course.DoesNotExist:
                print(f"Course does not exist: {course}")
                continue
            assignments = Assignment.objects.get(course_name=course_obj.course_name)
            AssignmentHaruBhako[course] = [
                assignments.assignment_name,
                assignments.assignment_description,
                assignments.due_date.strftime('%Y-%m-%d')  # Ensure date is JSON serializable
            ]
       '''    
        # Convert the dictionary to a JSON string
'''  assignments_json = json.dumps(AssignmentHaruBhako)
        
        return render(request, 'courses.html', {
            'name': StdProfile.Studentname,
            'courses': courses,
            'assignments': assignments_json
        })
    else:
        return redirect('login_student')'''
    