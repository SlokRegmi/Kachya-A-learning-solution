from django.urls import path

from . import views
urlpatterns = [
    path ("",views.index,name = "index"),
    path ("login_student",views.login_student,name = "login_student"),
    path ("SignUpStudent",views.SignUpStudent,name = "SignUpStudent"),
    path ("SignUpTeacher",views.SignUpTeacher,name = "SignUpTeacher"),
        path('chat/', views.chat, name='chat'),

   # path ("login_teacher",views.login_teacher,name = "login_teacher"),
  #  path ("dashboard_student/<str:username>",views.dashboard_student,name = "dashboard_student"),
  path ("dashboard_teacher/<str:username>",views.dashboard_teacher,name = "dashboard_teacher"),
    path ("course_category",views.course_category,name = "course_category"),
    path ("cccc",views.cccc,name = "cccc"),

  path('submit-category/', views.submit_category, name='submit_category'),
    path('course-desc/<str:category>/', views.course_desc, name='course_desc'),
    ]
