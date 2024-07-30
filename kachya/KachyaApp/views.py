
from audioop import reverse
from http.client import HTTPResponse
from itertools import count
import json
import logging
import random
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
from django.db.models import Count

import os
from datetime import datetime
import pytz
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

def index(request):
    # course_ids = list(Course.objects.values_list('course_id', flat=True))
    # random_ids = random.sample(course_ids, min(len(course_ids), 4)) 
    # courses = Course.objects.filter(course_id__in=random_ids)
    # course_details = courses.values_list('course_name', 'course_category','course_live')
    # category_counts_queryset = Course.objects.values('course_category').annotate(count=Count('course_id'))
    # category_counts = [[entry['course_category'], entry['count']] for entry in category_counts_queryset] 
    # context = {
    #     'course_details': course_details,
    #     'category_counts': category_counts,
    # }
    
    # return render(request, 'index.html', context)
   return render(request, 'login_student.html')
def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('email_login_student')
        password = request.POST.get('pass_login_student')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if TeacherProfile.objects.filter(user=user).exists():
                usering = TeacherProfile.objects.get(user=user)
                courseslist = usering.assgined_course.split(",")  # Update this line with the correct attribute name
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
     try:
        if request.method == "GET":
            # Fetch all course names
            names = Course.objects.values_list('course_category', flat=True).distinct()

            if not names:
                logging.error('No course names found')
                return render(request, 'course_category.html', {'error': 'No course names found'})
            
            names_json = json.dumps(list(names), cls=DjangoJSONEncoder)
            
        else:
            names_json = json.dumps([])  # Default empty list for non-GET requests
            
     except Exception as e:
        logging.error(f'Error fetching course names: {str(e)}')
        return render(request, 'course_category.html', {'error': 'An error occurred while fetching course names'})

     return render(request, 'course_category.html', {'course_names': names_json})

@csrf_exempt
def submit_category(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        category = data.get('category')

        print(category)
        return JsonResponse({'redirect_url': f'/course_listing/?category={category}'})
        #yesle course description ma janxa aaahile ko laagi yo change garera course listing ma pathairako ho 
        #return JsonResponse({'redirect_url': f'/course_desc/?category={category}'})
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
    # sample_assignments = {
    #     "Python": [
    #         ["Assignment 1", "Learn the basics of Python programming.", "2024-08-01"],
    #         ["Assignment 2", "Practice Python loops and conditions.", "2024-08-10"]
    #     ],
    #     "Django": [
    #         ["Assignment 3", "Build a simple Django application.", "2024-08-15"]
    #     ],
    #     "JavaScript": [
    #         ["Assignment 4", "Create a dynamic web page using JavaScript.", "2024-08-20"]
    #     ]
    # }
    # context = {
    #     'assignments': json.dumps(sample_assignments)
    # }
    # return render(request, 'courses.html', context)
        username = request.user.username
        try:
            StdProfile = StudentProfile.objects.get(username=username)
        except StudentProfile.DoesNotExist:
            return redirect('login_student')  # Redirect if student profile does not exist

        courses = StdProfile.course_taken.split(",")
        AssignmentHaruBhako = {}
        assessments = {}
        for course in courses:
            try:
                course_obj = Course.objects.get(course_name=course)
            except Course.DoesNotExist:
                print(f"Course does not exist: {course}")
                continue

            assignments = Assignment.objects.filter(course_name=course_obj)
            AssignmentHaruBhako[course] = [
            [
                assignment.assignment_name,
                assignment.assignment_description,
                assignment.due_date.strftime('%Y-%m-%d'),
                assignment.submitted,
                assignment.remarks,

            ]
            for assignment in assignments
        ]
            assessments[course] = AssignmentHaruBhako[course]
    
    # Convert the dictionary to a JSON string
        assignments_json = json.dumps(AssignmentHaruBhako)
    
        return render(request, 'courses.html', {
        'name': StdProfile.Studentname,
        'courses': courses,
        'assignments': assignments_json,
        'assessments': assessments
    })
 
def course_listing(request, category):
    try:
        # Fetch courses that match the given category
        courses = Course.objects.filter(course_category=category)

        # Extract the course names
        course_names = list(courses.values_list('course_name', flat=True))
        names_json = json.dumps(list(course_names), cls=DjangoJSONEncoder)

        if not course_names:
            logging.error(f'No courses found for category: {category}')
            return render(request, 'course_listing.html', {'error': 'No courses found for the given category'})

    except Exception as e:
        logging.error(f'Error fetching courses for category {category}: {str(e)}')
        return render(request, 'course_listing.html', {'error': 'An error occurred while fetching courses'})
    return render(request, 'course_listing.html', {
        'category': category,
        'course_names': names_json
    })

def edit_profile(request):
    name = ""
    email = ""
    role = ""
    initials = ""

    if request.method == 'POST':
        username = request.user.username
        user = User.objects.get(username=username)

        try:
            student = StudentProfile.objects.get(user=user)
            name = student.Studentname
            email = student.StudentEmail
            role = "Student"
            print(f"Student Profile: {name}, {email}, {role}")
        except StudentProfile.DoesNotExist:
            try:
                teacher = TeacherProfile.objects.get(user=user)
                name = teacher.Teachername
                email = teacher.TeacherEmail
                role = "Teacher"
                print(f"Teacher Profile: {name}, {email}, {role}")
            except TeacherProfile.DoesNotExist:
                print("No profile found for user.")
        
        initials = get_initials(name) if name else ""
        return render(request, 'edit_profile.html', {'name': name, 'email': email, 'role': role, 'initials': initials})

    return render(request, 'edit_profile.html', {'name': name, 'email': email, 'role': role, 'initials': initials})

def get_initials(name):
    components = name.split()
    initials = ''.join([component[0] for component in components])
    return initials


@login_required
def changeDetail(request):
    if request.method == 'POST':
        username = request.user.username
        user = User.objects.get(username=username)

        # Change name and email logic
        try:
            student = StudentProfile.objects.get(user=user)
            fname = request.POST.get('fname')
            email = request.POST.get('email')
            if fname:
                student.Studentname = fname
            if email:
                student.StudentEmail = email
            student.save()
        except StudentProfile.DoesNotExist:
            try:
                teacher = TeacherProfile.objects.get(user=user)
                name = request.POST.get('name')
                email = request.POST.get('email')
                if name:
                    teacher.Teachername = name
                if email:
                    teacher.TeacherEmail = email
                teacher.save()
            except TeacherProfile.DoesNotExist:
                messages.error(request, "No profile found for user.")
                return redirect('changeDetail')

        # Change password logic
        opassword = request.POST.get('opassword')
        npassword1 = request.POST.get('npassword1')
        npassword2 = request.POST.get('npassword2')

        if opassword and npassword1 and npassword2:
            if user.check_password(opassword):
                if npassword1 == npassword2:
                    user.set_password(npassword1)
                    user.save()
                    update_session_auth_hash(request, user)  # Keep the user logged in after password change
                    messages.success(request, "Password changed successfully.")
                else:
                    messages.error(request, "New passwords do not match.")
            else:
                messages.error(request, "Current password is incorrect.")
        
        return redirect('changeDetail')
    else:
        return render(request, 'login_student.html')
    
def logout(request):
    auth.logout(request)
    return redirect ("/")


def teacher_assignment(request):
    studentlist = [    ]
    username = request.user.username
    Tusers = TeacherProfile.objects.get(username=username)
    
    return render (request, 'teacher_assignment.html', {'studentlist': studentlist})
