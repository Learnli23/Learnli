from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import create_classForm ,create_subjectForm,create_lessonForm
#from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from . models import Lessons,Classes,Subjects
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .import forms
from .utils import send_email_notification
import uuid
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
 


# sending email when a course is created

@login_required
def create_course(request):
    if not hasattr(request.user, 'teacher'):
        return redirect('home')

    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save()
            # Send email notification
            subject = 'New Marks Awarded'
            message = f'Dear {result.student.user.username},\n\nYou have been awarded {result.marks} marks for the {result.test or result.exam}.\n\nBest regards,\nYour School'
            recipient_list = [result.student.user.email]
            send_email_notification(subject, message, recipient_list)
            return redirect('teacher_results')
    else:
        form = ResultForm()
    return render(request, 'results/award_marks.html', {'form': form})



 
# create class view
def create_class(request): 
    submitted = False
    if request.method == 'POST':
        form = create_classForm(request.POST, request.FILES,user=request.user)
        if form.is_valid():
            classes=form.save(commit=False)
            classes.created_by = request.user
            classes.save()
            form.save() 
            # Send email notification
            #subject = 'New Course created'
            #message = f'Dear {classes.created_by.username},\n\n A new course {classes.title} has been created.\n\n you can sign into your learnli account and check for it. Good luck '
            #recipient_list = [classes.created_by.email]
            #send_email_notification(subject, message, recipient_list)
            return HttpResponseRedirect('/classes?submitted = True')

    else:
         form = create_classForm(user=request.user)
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'create_class.html' ,{'form':form, 'submitted':submitted})


# create subject view
def create_subject(request): 
    submitted = False
    if request.method == 'POST':
        form = create_subjectForm(request.POST, request.FILES,user=request.user)
        if form.is_valid():
            subject=form.save(commit=False)
            subject.taught_by = request.user
            subject.save()
            form.save() 
            return HttpResponseRedirect('/subjects?submitted = True')

    else:
         form = create_subjectForm(user=request.user)
         if 'submitted' in request.GET:
             submitted = True
    return render(request,'create_subject.html' ,{'form':form, 'submitted':submitted})




#Enroll into a course

def Enrolling(request, pk) :
     if request.user.is_authenticated:
        course = get_object_or_404(Classes, id = pk)
        is_enrolled = course.Enroll.filter(id=request.user.id).exists()
        course_content_type = ContentType.objects.get_for_model(Classes)  # Get ContentType for course mode
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
def my_courses(request):
    my_courses = Classes.objects.all()
    return render(request,'my_courses.html',{
            'my_courses':my_courses,})
    

   
# create lessons view
def create_lesson(request): 
    submitted = False
    if request.method == 'POST':
        form = create_lessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson=form.save(commit=False)
            lesson.taught_by = request.user
            lesson.position = request.user.id
            lesson.save()
            form.save() 
            return HttpResponseRedirect('/lessons?submitted = True')

    else:
         form = create_lessonForm
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'create_lesson.html' ,{'form':form, 'submitted':submitted}) 

#**** CREATING  VIEWS FOR CLASSES, SUBJECTS AND LESSONS***
# class view
def classes(request):
    classes = Classes.objects.all()
    return render(request,'classes.html',
    {
        'classes':classes
    })

# subject view
def subjects(request):
    subjects = Subjects.objects.filter(taught_by = request.user).order_by('-created_on')
    return render(request,'subjects.html',
    {
        'subjects':subjects
    })    

# lessons view
def lessons(request):
    lessons = Lessons.objects.filter(taught_by = request.user).order_by('-created_on')
    return render(request,'lessons.html',
    {
        'lessons':lessons
    }) 
#getsubjects for aparticular corse
def class_subjects(request,class_id):
    classes =get_object_or_404(Classes,id=class_id)
    has_paid = classes.paid_users.filter(id=request.user.id).exists()
    if has_paid or request.user == classes.created_by:
        subjects_for_class =classes.with_subjects.all()
        return render(request,'class_subjects.html',
        {
            'subjects_for_class':subjects_for_class
        
        })
    else:
     # Redirect to payment page
        messages.info(request, "You need to pay for this course to access its content.")
        return redirect('course_payment_page', course_id = class_id) 




# course payment page.
@login_required
@csrf_exempt
def course_payment_page(request, course_id):
    course = Classes.objects.get(id=course_id)
    user_profile=request.user
    course_id = course_id
     
    if request.method == "POST":
        # Extract currency from the form
        currency = request.POST.get('currency')
        price = course.price
        tx_ref = f"course_{course_id}_txref--{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Flutterwave API request
        
        headers = {
                'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',  # API Key from settings
                'Content-Type': 'application/json',
            }


       
        payload = {
                "tx_ref":tx_ref,  # Transaction reference
                "amount":float(price),  # Amount to be charged
                "currency":currency,  # Currency
                "payment_options": "card, mobilemoneyuganda, ussd,banktransfer",
                "redirect_url": "http://54.198.251.116/course_payment_success",  # Redirect URL after payment
                "customer": {
                    "email": user_profile.email,  # User's email for payment receipt
                    "phonenumber": user_profile.contact,  # User's phone number
                    "name": user_profile.username  # User's name
                },
                "customizations": {
                    "title": "Learnli book Payment",  # Title of the payment
                    "description": f"{user_profile.username.capitalize()} course payment",  # Description of the payment
                    #"logo":book.display_image
                }
            }

                    # Make the API request to Flutterwave

        try:      
                    
                    response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)

                    # Check if the request was successful
                    if response.status_code == 200:
                        messages.success(request, 'payment successful!')
                        # if a success, flatterwavw will return a json data structure containg the satatus, link and some other info.
                        payment_link = response.json().get('data',{}).get('link')# collect the link to the flatterwave checkout page and store it into payment_link varriable
                        
                        return redirect(payment_link)  # Redirect to the payment page(the flatterwave checkout page)
                        
                    else:
                        # Log the error and render an error page with the message from Flutterwave
                        messages.error(request, 'payment failed!')
                        error_message = response.json().get('message')
                        return render(request, 'payment_error.html', {'error': error_message})

        except Exception as e:
                    # Handle exceptions such as network issues
                    return render(request, 'payment_error.html', {'error': f"An error occurred: {str(e)}"})    
    return render(request,'course_payment_page.html', {'course': course})        



#course payment success hundling
@login_required
@csrf_exempt
def course_payment_success(request): 
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')
    
    course_id, rest_of_tx_ref = extract_course_and_rest_of_tx_ref_from_tx_ref(tx_ref)
  
    # Verify the payment
    
    flutterwave_url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
    }

    try:
            # Call the Flutterwave API to verify the transaction
            response = requests.get(flutterwave_url, headers=headers)
            print(' this the response status code:',response.status_code)
            response.raise_for_status()  # Check if request was successful
            payment_data = response.json()

            # Check if transaction was successful
            if payment_data.get('status') == 'success':# and payment_data.get('payment_data', {}).get('status') == 'successful':
                # Ensure the user is authenticated before updating profile
                if request.user.is_authenticated:
                    user_profile = request.user
                     # Record the payment
                    course = Classes.objects.get(id = course_id)
                    # Create payment record
                    #Book_Payment.objects.create(user=user_profile, book=book, transaction_id=transaction_id)
                    # Add user to paid_users for the book
                    course.paid_users.add(user_profile)

                    messages.success(request, "Payment successful! You now have access to the course.")
                    return redirect('class_subjects',course.id)
                    
                else:
                    messages.error(request, "User is not authenticated.")
                    return redirect('login')
            else:
                # Handle unsuccessful transaction
                messages.error(request, "Payment verification failed. Please try again.")
                return redirect('home')
    except requests.exceptions.RequestException as e:
            # Handle request exceptions (network issues, invalid response, etc.)
            print(f"Error during transaction verification: {e}")
            messages.error(request, "Error verifying payment. Please try again.")
            return redirect('home')

# extract the book id and user id rom tx_ref number
def extract_course_and_rest_of_tx_ref_from_tx_ref(tx_ref):
    # Assuming tx_ref format is 'book_{book_id}_user_{user_id}'
     _,course_id, rest_of_tx_ref= tx_ref.split('_',2)
     return int(course_id), str(rest_of_tx_ref)

# get lessons for aparticular subject
def subject_lessons(request,subject_id):
    subjects =get_object_or_404(Subjects,id=subject_id)
    lessons_for_subject =subjects.with_lessons.all()
    return render(request,'subject_lessons.html',
    {
        'lessons_for_subject':lessons_for_subject,
        'subjects':subjects,
    }) 

#**** EDITING CLASS, SUBJECTS AND LESSON CONTENT*****    
# Edit the class content

def edit_class(request, klass_id):
    klass = Classes.objects.get( pk = klass_id)
    form = create_classForm( request.POST or None, request.FILES,request.user or None, instance=klass)
    if form.is_valid():
           form.save()
           return redirect('classes')
    

    return render(request, 'edit_class.html', {
        "klass":klass,
        'form':form,
    })


# Edit the subject content
def edit_subject(request, subject_id):
    subject = Subjects.objects.get( pk = subject_id)
    form = create_subjectForm( request.POST or None, request.FILES,request.user or None, instance=subject)
    if form.is_valid():
           form.save()
           return redirect('subjects')
    

    return render(request, 'edit_subject.html', {
        "klass":subject,
        'form':form,
    })   


# Edit the lesson content
def edit_lesson(request, lesson_id):
    lesson = Lessons.objects.get( pk = lesson_id)
    form = create_lessonForm( request.POST or None, request.FILES or None, instance=lesson)
    if form.is_valid():
           form.save()
           return redirect('lessons')
    

    return render(request, 'edit_lesson.html', {
        "klass":lesson,
        'form':form,
    })  

 #*** DELETING A CLASS, LESSON OR SUBJECT***
 # Deleting a clas
def delete_class(request, klass_id):
    klass = Classes.objects.get( pk = klass_id)
    #if request.user == Classes. created_by:
    klass.delete()
    messages.success(request,('class Deleted!!'))
    return redirect('classes')
    #else:
         #messages.success(request,('you can not delete this class'))
         #return redirect('classes')

 #Deleting a subject
def delete_subject(request, subject_id):
    subject= Subjects.objects.get( pk = subject_id)
    #if request.user.user == Subjects.taught_by:
    subject.delete()
    messages.success(request,('subject Deleted!!'))
    return redirect('subjects')
    #else:
        # messages.success(request,('you can not delete this subject'))
        # return redirect('subjects')

 #Deleting a lesson
def delete_lesson(request, lesson_id):
    lesson= Lessons.objects.get( pk = lesson_id)
    #if request.user.user == Lessons. taught_by:
    lesson.delete()
    messages.success(request,('lesson Deleted!!'))
    return redirect('lessons')
    #else:
         #messages.success(request,('you can not delete this subject'))
         #return redirect('subjects')
