from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from . models import Lessons,Course,course_unit,FreeSub_Section,FreeSection,FreeContent,FreeEbook
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .import forms
from .forms import FreeContentForm,FreeEbookForm,Freesub_SectionForm,FreeSectionForm,create_course_unitForm,create_courseForm,create_lessonForm
import uuid
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from users.models import  user_Profile
from django.forms import modelformset_factory
from django.contrib import messages
import json
import uuid
from django.conf import settings
from datetime import datetime
 
 



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
def free_course_details(request, pk):
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
                return redirect('free_course_details', pk = pk)
            
        return render(request,'free_course_details.html',{
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
    course_units_for_courses =courses.with_course_units.all()
    return render(request,'course_course_units.html',
        {
            'course_units_for_courses':course_units_for_courses
        
        })
     

# get lessons for aparticular course unit
@login_required
def course_unit_lessons(request,course_unit_id):
    course_units =get_object_or_404(course_unit,id=course_unit_id)
    lessons_for_course_unit =course_units.with_lessons.all()
    return render(request,'course_unit_lessons.html',
    {
        'lessons_for_course_unit':lessons_for_course_unit,
        'course_units':course_units,
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
    

    return render(request, 'edit_course.html', {
        "courses":courses,
        'form':form,
    })


# Edit the subject content
@login_required
def edit_course_units(request, course_unit_id):
    course_units = course_unit.objects.get( pk = course_unit_id)
    form = create_course_unitForm( request.POST or None, request.FILES,request.user or None, instance=course_units)
    if form.is_valid():
           form.save()
           return redirect('course_units')
    return render(request, 'edit_course_unit.html', {
        "course_units":course_units,
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
    

# Free library views

@login_required
def upload_Freecontent(request):
    submitted = False
    if request.method == 'POST':
        form = FreeContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.save()
            return redirect('Freecontent_list')
    else:
        form = FreeContentForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'upload_Freecontent.html', {'form': form})

# editing content
@login_required
def edit_Freecontent(request, content_id):
    content = FreeContent.objects.get(pk = content_id)
    form = FreeContentForm( request.POST or None, request.FILES or None, instance=content)
    if form.is_valid():
           form.save()
           return redirect('Freecontent_list')
    return render(request, 'edit_Freecontent.html', {
        "content":content,
        'form':form,
    })

# delete ebook
@login_required
def delete_Freecontent(request, content_id):
        content= FreeContent.objects.get(pk = content_id)
        content.delete()
        messages.success(request,('Content Deleted!!'))
        return redirect('Freecontent_list')    

# content details view
@login_required
def Freecontent_detail(request, pk):
    content = get_object_or_404(FreeContent, pk=pk)
    book_content_type = ContentType.objects.get_for_model(FreeContent)  # Get ContentType for ebook mode 
    return render(request, 'Freecontent_detail.html', {
        'content': content,
        'book_content_type':book_content_type,
    })

 

@login_required
def Freecontent_list(request):
    contents = FreeContent.objects.filter(is_hiden = False).order_by('-upload_date')
    return render(request, 'Freecontent_list.html', {'contents': contents})

@login_required
def profile_Freelibrary(request,pk):
    profile = get_object_or_404(user_Profile, pk=pk)
    contents = FreeContent.objects.all().order_by('-upload_date')
    return render(request, 'profile_Freelibrary.html', {'contents': contents, 'profile':profile})    



#Ebook views
@login_required
def Freebook_list(request):
    books = FreeEbook.objects.filter(is_hiden = False)
    return render(request, 'Freebook_list.html', {'books': books})

  


#Profile Ebook views
@login_required
def profile_Freebooks(request,pk):
    profile = get_object_or_404(user_Profile, pk=pk)
    books = FreeEbook.objects.all().order_by('-date_updated')
    return render(request, 'profile_Freebooks.html', {'books': books, 'profile':profile})  


# editing ebook
@login_required
def edit_Freeebook(request, ebook_id):
    ebooks =  FreeEbook.objects.get(pk = ebook_id)
    form = FreeEbookForm( request.POST or None, request.FILES or None, instance=ebooks)
    if form.is_valid():
           form.save()
           return redirect('Freebook_list')
    

    return render(request, 'edit_Freeebook.html', {
        "ebooks":ebooks,
        'form':form,
    })

# delete ebook
@login_required
def delete_Freeebook(request, ebook_id): 
        ebook= FreeEbook.objects.get(pk = ebook_id)
        ebook.delete()
        messages.success(request,('Ebook Deleted!!'))
        return redirect('Freebook_list')    
    
    

def Freebook_details(request, pk):
    book = get_object_or_404(FreeEbook, pk=pk)
    ebook_content_type = ContentType.objects.get_for_model(FreeEbook)  # Get ContentType for ebook mode
    sections = book.sections.all()
    return render(request, 'book_details.html', {
            'book': book,
            'sections': sections,
            'ebook_content_type':ebook_content_type
            })

# adding abook
@login_required
def add_Freebook(request):
    if request.method == 'POST':
        form = FreeEbookForm(request.POST,request.FILES )
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.save()

            return redirect('Freebook_list')
    else:
        form = FreeEbookForm()
    return render(request, 'add_Freebook.html', {'form': form})

def add_Freesection(request, book_pk):
    book = get_object_or_404(FreeEbook, pk=book_pk)
    SectionFormSet = modelformset_factory(FreeSection, form=FreeSectionForm, extra=1, can_delete=True)
    if request.method == 'POST':
        formset = SectionFormSet(request.POST, request.FILES, queryset=book.sections.all())
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.ebook = book
                instance.section_author = request.user
                instance.save()
            return redirect('Freebook_details', pk=book.pk)
    else:
        formset = SectionFormSet(queryset=book.sections.all())

    return render(request, 'add_Freesection.html', {'book': book, 'formset': formset}) 


def add_Freesub_section(request, section_pk):
    section = get_object_or_404(FreeSection, pk=section_pk)
    sub_SectionFormSet = modelformset_factory(FreeSub_Section, form=Freesub_SectionForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = sub_SectionFormSet(request.POST, request.FILES, queryset=section.sub_sections.all())
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.section = section
                instance.subsection_author = request.user
                instance.save()
            return redirect('Freesection_details', pk=section.pk)
    else:
        formset = sub_SectionFormSet(queryset=section.sub_sections.all())

    return render(request, 'add_Freesub_section.html', {'section': section, 'formset': formset})       

def Freesection_details(request, pk):
    section = get_object_or_404(FreeSection, pk=pk)
    sub_sections = section.sub_sections.all()
    return render(request, 'Freesection_details.html', {'section': section, 'sub_sections': sub_sections})  