from django.shortcuts import render

# Create your views here.
def index(request):
    def teacher_assignment(request):
        sample_assignments = {
            "Python": [
                ["Assignment 1", "Learn the basics of Python programming.", "2024-08-01", "yes", "hello my name is this "]

            ],
            "Django": [
                ["Assignment 2",
                "Build a simple Django application.",
                "2024-08-15"]
            ],
            "JavaScript": [
                ["Assignment 3",
                "Create a dynamic web page using JavaScript.",
                "2024-08-20"]
            ]}
    return render (request, "dashboard_teacher.html")
def about(request):

    return render (request, "about.html")  
 