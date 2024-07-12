from django.urls import path

from . import views
urlpatterns = [
    path ("",views.index,name = "index"),
    path ("course_database",views.course_database,name = "course_database"),
    ]