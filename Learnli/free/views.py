from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import create_course_unitForm, create_courseForm, create_lessonForm
#from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from . models import Lessons,Course, course_unit
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .import forms
import uuid
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
 



# create course view
@login_required
def create_free_course(request): 
    submitted = False
    if request.method == 'POST':
        form = create_courseForm(request.POST, request.FILES,user=request.user)
        if form.is_valid():
            courses=form.save(commit=False)
            courses.teacher = request.user
            courses.save()
            form.save() 
            return HttpResponseRedirect('/courses?submitted = True')

    else:
         form = create_courseForm(user=request.user)
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'create_free_course.html' ,{'form':form, 'submitted':submitted})


# create subject view
@login_required
def create_course_unit(request): 
    submitted = False
    if request.method == 'POST':
        form = create_course_unitForm(request.POST, request.FILES,user=request.user)
        if form.is_valid():
            course_unit=form.save(commit=False)
            course_unit. unit_teacher = request.user
            course_unit.save()
            form.save() 
            return HttpResponseRedirect('/course_units?submitted = True')

    else:
         form = create_course_unitForm(user=request.user)
         if 'submitted' in request.GET:
             submitted = True
    return render(request,'create_course_unit.html' ,{'form':form, 'submitted':submitted})




#Enroll into a course
@login_required
def Enrolling(request, pk) :
     if request.user.is_authenticated:
        course = get_object_or_404(Course, id = pk)
        is_enrolled = course.Enroll.filter(id=request.user.id).exists()
        course_content_type = ContentType.objects.get_for_model(Course)  # Get ContentType for course mode
        #post form logic
        if request.method=='POST':
            if 'enroll' in request.POST and not is_enrolled:
                course.Enroll.add(request.user)
            if 'enroll' in request.POST and  is_enrolled:
                course.Enroll.remove(request.user)    
                return redirect('enroll', pk = pk)
            
        return render(request,'course_details.html',{
            'course':course,
            'course_content_type':course_content_type,
             
            })   
     else: 
         messages.success(request,('you must be loged in to view this page'))
         return render(request, 'home.html')

# enrolled courses/ my_courses
@login_required
def myfree_courses(request):
    myfree_courses = Course.objects.all()
    return render(request,'my_courses.html',{
            'myfree_courses':myfree_courses,})
    

   
# create lessons view
@login_required
def create_free_lesson(request): 
    submitted = False
    if request.method == 'POST':
        form = create_lessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson=form.save(commit=False)
            lesson.lesson_teacher = request.user
            lesson.position = request.user.id
            lesson.save()
            form.save() 
            return HttpResponseRedirect('/free_lessons?submitted = True')

    else:
         form = create_lessonForm
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'create_free_lesson.html' ,{'form':form, 'submitted':submitted}) 

#**** CREATING  VIEWS FOR CLASSES, SUBJECTS AND LESSONS***
# class view
@login_required
def courses(request):
    courses = Course.objects.filter(is_hiden = False)
    return render(request,'courses.html',
    {
        'courses':courses
    })

# subject view
@login_required
def course_units(request):
    course_units = course_unit.objects.filter( unit_teacher = request.user).order_by('-created_on')
    return render(request,'course_units.html',
    {
        'course_units':course_units
    })    

# lessons view
@login_required
def free_lessons(request):
    lessons = Lessons.objects.filter(lesson_teacher = request.user).order_by('-created_on')
    return render(request,'free_lessons.html',
    {
        'lessons':lessons
    }) 
#getsubjects for aparticular corse
@login_required
def course_course_units(request,course_id):
    courses =get_object_or_404(Course,id=course_id)
    course_units_for_courses =courses.with_subjects.all()
    return render(request,'course_course_units.html',
        {
            'course_units_for_courses':course_units_for_courses
        
        })
     

# get lessons for aparticular course unit
@login_required
def course_units_lessons(request,course_unit_id):
    course_unit =get_object_or_404(course_unit,id=course_unit_id)
    lessons_for_course_unit =course_unit.with_lessons.all()
    return render(request,'course_unit_lessons.html',
    {
        'lessons_for_course_unit':lessons_for_course_unit,
        'course_unit':course_unit,
    })      

#**** EDITING CLASS, SUBJECTS AND LESSON CONTENT*****    
# Edit the class content
@login_required
def edit_course(request, course_id):
    course = Course.objects.get( pk = course_id)
    form = create_courseForm( request.POST or None, request.FILES,request.user or None, instance=course)
    if form.is_valid():
           form.save()
           return redirect('courses')
    

    return render(request, 'edit_courses.html', {
        "courses":courses,
        'form':form,
    })


# Edit the subject content
@login_required
def edit_course_units(request, course_unit_id):
    course_unit = course_unit.objects.get( pk = course_unit_id)
    form = create_course_unitForm( request.POST or None, request.FILES,request.user or None, instance=course_unit)
    if form.is_valid():
           form.save()
           return redirect('course_units')
    

    return render(request, 'edit_course_unit.html', {
        "course_unit":course_unit,
        'form':form,
    })   


# Edit the lesson content
@login_required
def edit_lesson(request, lesson_id):
    lesson = Lessons.objects.get( pk = lesson_id)
    form = create_lessonForm( request.POST or None, request.FILES or None, instance=lesson)
    if form.is_valid():
           form.save()
           return redirect('lessons')
    

    return render(request, 'edit_lesson.html', {
        "lesson":lesson,
        'form':form,
    })  

 #*** DELETING A CLASS, LESSON OR SUBJECT***
 # Deleting a clas
@login_required
def delete_course(request, course_id):
    course = Course.objects.get( pk = course_id)
    course.delete()
    messages.success(request,('course Deleted!!'))
    return redirect('courses')
    

 #Deleting a subject
@login_required
def delete_course_units(request, course_unit_id):
    course_unit= course_unit.objects.get( pk = course_unit_id)
    course_unit.delete()
    messages.success(request,('course unit Deleted!!'))
    return redirect('course_units')
     
 #Deleting a lesson
def delete_lesson(request, lesson_id):
    lesson= Lessons.objects.get( pk = lesson_id)
    lesson.delete()
    messages.success(request,('lesson Deleted!!'))
    return redirect('lessons')
    
