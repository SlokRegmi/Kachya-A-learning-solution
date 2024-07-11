from django.shortcuts import render

# Create your views here.
def index(request):

    return render (request, "dashboard_student.html")
def about(request):

    return render (request, "about.html")  
 