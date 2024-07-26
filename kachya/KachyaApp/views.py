from django.shortcuts import render

# Create your views here.
def index(request):
    return render (request, "edit_profile.html")
def about(request):

    return render (request, "about.html")  
 