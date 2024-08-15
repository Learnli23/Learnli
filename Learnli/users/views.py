from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import  student_SignupForm,teacher_SignupForm,institution_SignupForm
from django.contrib.auth import authenticate,login,logout
#from django.contrib.auth.models import User
from . models import user_Profile,User
from django.http import HttpResponseRedirect
from .import forms

# Create your views here

def home(request):
     return render(request,'home.html',{
              })


# about us view 
def about(request):
     return render(request,'about.html',{
              })
              
# **** working on profiles***
 
#update user profile
def update_profile(request):
    if request.user.is_authenticated:
        current_user =user_Profile.objects.get(id=request.user.id)
        user_form = student_SignupForm(request.POST or None,  request.FILES or None ,instance = current_user)
        #profile_form = profilePicForm(request.POST or None,  request.FILES or None ,instance = profile_user)
        if user_form.is_valid(): #and profile_form.is_valid():
            user_form.save()
           # profile_form.save()
            login(request,current_user)
            messages.success(request,('your profile has been updated'))
            return redirect("home")  
        return render(request,'update_profile.html',{"user_form":user_form, 
     #"profile_form":profile_form,
      })
    else:
        messages.success(request,('you must be loged in to view this page'))
        return redirect("home") 

#  user profile
def profile(request, pk) :
     if request.user.is_authenticated:
        profile = user_Profile.objects.get(id = pk)
        #post form logic
        if request.method=='POST':
            #get current user
            current_user_profile = request.user
            #get form data
            action = request.POST['follow']
            #decide to follow or unfollow
            if action =='unfollow':
            # act on the current users follow attribute
                current_user_profile.follows.remove(profile)
            elif  action =='follow':  
                 current_user_profile.follows.add(profile)
            current_user_profile.save()
            
        return render(request,'profile.html',{
            'profile':profile,
             
            })   
     else: 
         messages.success(request,('you must be loged in to view this page'))
         return render(request, 'home.html')

 # all registered users profiles
def profiles(request):
    if request.user.is_authenticated:
        profiles =user_Profile.objects.exclude(username=request.user)
        if request.method=='POST':
            #get current user
            current_user_profile = request.user
            #get form data
            action = request.POST['follow']
            #decide to follow or unfollow
            if action =='unfollow':
            # act on the current users follow attribute
                current_user_profile.follows.remove()
            elif  action =='follow':  
                 current_user_profile.follows.add()
            current_user_profile.save()
        
        return render(request,'profiles.html',{
            'profiles': profiles,
        })    
    else:
        messages.success(request,('you must be loged in to view this page'))
        return render(request, 'home.html')
        

#students  profiles
def students(request):
    if request.user.is_authenticated:
        students = user_Profile.objects.all()
        if request.method=='POST':
            #get current user
            current_user_profile = request.user
            #get form data
            action = request.POST['follow']
            #decide to follow or unfollow
            if action =='unfollow':
            # act on the current users follow attribute
                current_user_profile.follows.remove()
            elif  action =='follow':  
                 current_user_profile.follows.add()
            current_user_profile.save()
        return render(request,'students.html',{
            'students': students,

        })    
    else:
        messages.success(request,('you must be loged in to view this page'))
        return render(request, 'home.html') 
    
#teachers profiles
def teachers(request):
    if request.user.is_authenticated:
        teachers = user_Profile.objects.all()
        if request.method=='POST':
            #get current user
            current_user_profile = request.user
            #get form data
            action = request.POST['follow']
            #decide to follow or unfollow
            if action =='unfollow':
            # act on the current users follow attribute
                current_user_profile.follows.remove()
            elif  action =='follow':  
                 current_user_profile.follows.add()
            current_user_profile.save()
        return render(request,'teachers.html',{
            'teachers': teachers,

        })    
    else:
        messages.success(request,('you must be loged in to view this page'))
        return render(request, 'home.html') 

#institution profiles
def institutions(request):
    if request.user.is_authenticated:
        institutions = user_Profile.objects.all()
        return render(request,'institutions.html',{
            'institutions':institutions,

        })    
    else:
        messages.success(request,('you must be loged in to view this page'))
        return render(request, 'home.html')      



 # ***creating the three different users***      
# student registratioon form
def register_student(request):  
     form = student_SignupForm()
     if request.method =='POST':
         form = student_SignupForm(request.POST,request.FILES)
         if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user =authenticate(username = username, password  = password)
                login(request, user)
                messages.success(request,('you are reqistered successfully, WELCOME'))
                return redirect("home")
     return render(request,'register_student.html',{
            'form': form, }) 
            
 # teacher registration form  
def register_teacher(request):  
     form = teacher_SignupForm()
     if request.method =='POST':
         form = teacher_SignupForm(request.POST,request.FILES)
         if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user =authenticate(username = username, password  = password)
                login(request, user)
                messages.success(request,('you are reqistered successfully, WELCOME'))
                return redirect("home")
     return render(request,'register_teacher.html',{
            'form': form, }) 

# institution registratioon form
def register_institution(request):  
     form = institution_SignupForm()
     if request.method =='POST':
         form = institution_SignupForm(request.POST,request.FILES)
         if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user =authenticate(username = username, password  = password)
                login(request, user)
                messages.success(request,('you are reqistered successfully, WELCOME'))
                return redirect("home")
     return render(request,'register_institution.html',{
            'form': form, })             


#*** hanadling user authentication, login and logout***

def login_user(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is  not None:
            login(request,user)
            messages.success(request,('you are successfuly loged in'))
            return redirect('about') 
        else:
            
            messages.success(request,('there was an error loging in, please try again'))   
            return redirect('login')
                    
    else:   
        return render(request,'login_user.html',{})

# logout user view
def logout_user(request):
    logout(request)
    messages.success(request,('you are loged out, thanks for spending some time on the page'))   
    return redirect("about")     
