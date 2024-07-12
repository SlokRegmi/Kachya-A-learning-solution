from django.shortcuts import render

from KachyaApp.models import Course

# Create your views here.
def index(request):

    return render (request, "database.html")

def course_database(request):

    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_description = request.POST.get('course_description')
        course_live = request.POST.get('course_live')
        course_picture = request.FILES.get('course_picture')
        course_price = request.POST.get('course_price')
        no_of_assignment = request.POST.get('no_of_assignment')
        course_category = request.POST.get('course_category')
        

        course = Course.objects.create(course_name=course_name, course_description=course_description, course_live=course_live, course_picture=course_picture, course_price=course_price, no_of_assignment=no_of_assignment,course_category=course_category)
        

        return render (request, "database.html")