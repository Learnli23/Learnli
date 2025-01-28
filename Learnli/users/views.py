from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import  student_SignupForm,teacher_SignupForm,institution_SignupForm,SubscriptionForm
from django.contrib.auth import authenticate,login,logout
#from django.contrib.auth.models import User
from . models import user_Profile,User
from django.http import HttpResponseRedirect
from .import forms
from Works.models import Classes
from my_library.models import Ebook,Content
from Examination.models import Exam,RegisterforExam,Test
from blogs.models import BlogPost
from Works.recommendations import get_course_recommendations, get_book_recommendations, get_teacher_recommendations
from datetime import timedelta
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
import requests  
from django.conf import settings
import uuid
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_datetime
from django.db.models import Q
#moderation tool
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from.forms import ReportContentForm
from.models import FlaggedContent
import openai


# Set up the OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

#Assistant view

@csrf_exempt
def chat(request):
    if request.method == "POST":
        user_input = request.POST.get("message")

        if user_input:
            # Interact with OpenAI API
            try:
                response = openai.Completion.create(
                    engine="GTP-3.5",  # You can use other engines like GPT-4 if needed
                    prompt=user_input,
                    max_tokens=150
                )

                # Extract the assistant's response from the API result
                bot_response = response.choices[0].text.strip()

                return JsonResponse({"message": bot_response})

            except Exception as e:
                return JsonResponse({"message": f"Error: {str(e)}"})

    return JsonResponse({"message": "Invalid request method."})





# content moderation tool views
 
# reporting an item
@login_required
def report_content(request,content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    content_object = content_type.get_object_for_this_type(id=object_id)
    if request.method == "POST":
        form = ReportContentForm(request.POST)
        if form.is_valid():
            FlaggedContent.objects.create(
                content_type=content_type,
                object_id=object_id,
                reported_by=request.user,
                reason=form.cleaned_data['reason'],
            )
            messages.success(request,('your report has been submited ,Learnli will review the report and take an appropriet action. thank you for your concern to maintain integrity on the platiform'))
            return redirect("home") 
            
    else:
        form = ReportContentForm()

    return render(request, "report.html", {"form": form, "content_object": content_object})

#loading the content moderation dash board
@login_required
def moderation_tool(request):
    flagged_items = FlaggedContent.objects.filter(reviewed=False, escalated=False )
    return render(request, "moderation_tool.html", {"flagged_items": flagged_items})

# moderation actions
#1.approving a flag
@login_required
def approve_flag(request, flag_id):
    flagged_item = FlaggedContent.objects.get(id=flag_id)
    flagged_item.reviewed = True
    flagged_item.approved = True
    content_object=flagged_item.content_object
    content_object.reported =True
    content_object.is_hiden =True
    content_object.save()
    flagged_item.save()
    return redirect("moderation_tool")
#1.approving a flag
@login_required
def reject_flag(request, flag_id):
    flagged_item = FlaggedContent.objects.get(id=flag_id)
    flagged_item.reviewed = True
    content_object=flagged_item.content_object
    content_object.reported =False
    content_object.is_hiden =False
    content_object.save()
    flagged_item.delete()
    return redirect("moderation_tool")
#3.escaleting a flag
@login_required
def escaleting_flag(request, flag_id):
    flagged_item = FlaggedContent.objects.get(id=flag_id)
    flagged_item.reviewed = True
    flagged_item.escalated = True
    flagged_item.save()
    return redirect("moderation_tool")

#reported Blogposts
@login_required
def reported_blogs(request):
    flagged_blogs = FlaggedContent.objects.filter(reviewed=False, escalated=False ,)
    return render(request, "reported_blogs.html", {"flagged_blogs": flagged_blogs})

#reported Ebooks
@login_required
def reported_ebooks(request):
    flagged_ebooks = FlaggedContent.objects.filter(reviewed=False, escalated=False ,)
    return render(request, "reported_ebooks.html", {"flagged_ebooks": flagged_ebooks})


#reported uploaded books
@login_required
def reported_content(request):
    flagged_content = FlaggedContent.objects.filter(reviewed=False, escalated=False ,)
    return render(request, "reported_content.html", {"flagged_content": flagged_content})

#reported courses
@login_required
def reported_courses(request):
    flagged_courses = FlaggedContent.objects.filter(reviewed=False, escalated=False ,)
    return render(request, "reported_courses.html", {"flagged_courses": flagged_courses})

#reported courses
@login_required
def reported_lessons(request):
    flagged_lessons = FlaggedContent.objects.filter(reviewed=False, escalated=False ,)
    return render(request, "reported_lessons.html", {"flagged_lessons": flagged_lessons})

# moderation guides
# course moderation guide
def course_guide(request):
    return render(request, "course_guide.html", { })

#BlogPost moderation guide
def blogs_guide(request):
    return render(request, "blogposts_guide.html", { })

#lesson moderation guide
def lessons_guide(request):
    return render(request, "lessons_guide.html", { })    

#ebook moderation guide
def ebook_guide(request):
    return render(request, "ebook_guide.html", { })  

#uploaded books moderation guide
def content_guide(request):
    return render(request, "content_guide.html", { })    


# recommendation views
@login_required
def user_profile(request, user_id):
    user = user_Profile.objects.get(id=user_id)
    recommended_courses = get_course_recommendations(user)
    recommended_books = get_book_recommendations(user)
    recommended_teachers = get_teacher_recommendations(user)
   
    context = {
        'user': user,
        'recommended_courses': recommended_courses,
        'recommended_books': recommended_books,
        'recommended_teachers': recommended_teachers,
    }
   
    return render(request, 'profile.html', context)

#  views here

def home(request):
    # Fetch counts
    book_count = Ebook.objects.count
    course_count = Classes.objects.count
    user_count = user_Profile.objects.count
    teacher_count = user_Profile.objects.filter(is_teacher = True).count
    institution_count = user_Profile.objects.filter(is_institution = True).count
    student_count =user_Profile.objects.filter(is_student = True).count

    # Pass counts to the template
    context = {
        'book_count': book_count,
        'course_count': course_count,
        'user_count': user_count,
        'teacher_count': teacher_count,
        'institution_count': institution_count,
        'student_count': student_count,
    }
    return render(request, 'home.html', context)
 

#copyright page
def copyright(request):
     return render(request,'copyright.html',{
              })

#FAQs

def FAQs(request):
     return render(request,'FAQs.html',{
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
    
      })
    else:
        messages.success(request,('you must be loged in to view this page'))
        return redirect("home") 

#  user profile
def profile(request, pk) :
     if request.user.is_authenticated:
        profile = user_Profile.objects.get(id = pk)
        courses = Classes.objects.filter(created_by = request.user).count
        ebooks = Ebook.objects.filter(author = request.user).count
        uploaded_books = Content.objects.filter(author = request.user).count
        Exams_created = Exam.objects.filter(created_by = request.user).count
        Registered_exams = RegisterforExam.objects.filter(name = request.user).count
        Tests_created = Test.objects.filter(created_by = request.user).count
        Blogs = BlogPost.objects.filter(author = request.user).count
        # caprturing paid courses
        paid_courses =Classes.objects.filter(created_by = request.user)
        courses_data =[]
        total_revenue = 0
        for course in paid_courses:
            paid_users_count = course.paid_users.count()
            if paid_users_count > 0:
                course_title = course.title
                price = course.price
                revenue = price*paid_users_count
                total_revenue += revenue

            
                courses_data.append({
                                    'course_title':course_title,
                                    'courses':courses,
                                    'price':price,
                                    'paid_users_count':paid_users_count,
                                    'revenue':revenue
                                    
                                    })
       

# caprturing paid ebooks
        paid_ebooks =Ebook.objects.filter(author = request.user)
        ebooks_data =[]
        ebook_total_revenue= 0
        for ebook in paid_ebooks:
            ebook_paid_users_count = ebook.paid_users.count()
            if ebook_paid_users_count > 0:
                ebook_title = ebook.title
                ebook_price = ebook.price
                ebook_revenue = ebook_price*ebook_paid_users_count
                ebook_total_revenue += ebook_revenue

            
                ebooks_data.append({
                                    'ebook_title': ebook_title,
                                    'ebooks':ebooks,
                                    'ebook_price':ebook_price,
                                    'ebook_paid_users_count':ebook_paid_users_count,
                                    'ebook_revenue':ebook_revenue
                                    
                                    })
         
        #caprturing paid uploded books
        paid_books =Content.objects.filter(author = request.user)
        books_data =[]
        book_total_revenue= 0
        for book in paid_books:
            book_paid_users_count = book.paid_users.count()
            if book_paid_users_count > 0:
                book_title = book.title
                book_price = book.price
                book_revenue = book_price*book_paid_users_count
                book_total_revenue += book_revenue

            
                books_data.append({
                                    'book_title': book_title,
                                    'uploaded_books ':uploaded_books ,
                                    'book_price':book_price,
                                    'book_paid_users_count':book_paid_users_count,
                                    'book_revenue':book_revenue
                                    
                                    })

#course recommendations
        user_profile = request.user
        # Get users whom the user follows or who follow the user
        related_users = user_profile.follows.all() | user_profile.followed_by.all()

        # Filter courses that have been paid for or enrolled in by any related user
        recommended_courses = Classes.objects.filter(
            Q(paid_users__in=related_users) or Q(Enroll__in=related_users)
        ).distinct()

#ebook recommendations
        user_profile = request.user
        # Get users whom the user follows or who follow the user
        related_users = user_profile.follows.all() or user_profile.followed_by.all()

        # Filter ebooks that have been paid for by any related user
        recommended_ebooks = Ebook.objects.filter(Q(paid_users__in=related_users)).distinct()

#book recommendations
        user_profile = request.user
        # Get users whom the user follows or who follow the user
        related_users = user_profile.follows.all() or user_profile.followed_by.all()

        # Filter ebooks that have been paid for by any related user
        recommended_books = Content.objects.filter(Q(paid_users__in=related_users)).distinct()        


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
            'courses':courses,
            'ebooks':ebooks,
            'uploaded_books':uploaded_books,
            'Exams_created':Exams_created,
            'Registered_exams': Registered_exams,
            'Tests_created':Tests_created,
            'Blogs':Blogs,
            'courses_data':courses_data,
            'total_revenue':total_revenue,
            'ebooks_data':ebooks_data,
            'ebook_total_revenue':ebook_total_revenue,
            'books_data':books_data,
            'book_total_revenue':book_total_revenue,
            'recommended_courses': recommended_courses,
            'recommended_ebooks':recommended_ebooks,
            'recommended_books':recommended_books

             
             
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
                messages.success(request,('you are reqistered successfully, WELCOME'
                                           'We are glad to give you 30 days of free SubscriptionForm'
                                          'please enjoy LearnLi'))
               
               
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
                messages.success(request,('you are reqistered successfully, WELCOME'
                                           'We are glad to give you 30 days of free SubscriptionForm'
                                          'please enjoy LearnLi'))
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
                messages.success(request,('you are reqistered successfully, WELCOME.'
                                           'We are glad to give you 30 days of free Subscription'
                                           'please enjoy LearnLi'))
                return redirect("home")
     return render(request,'register_institution.html',{
            'form': form, })             



#*** hanadling user authentication, login and logout***
 
def login_user(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
       
        user = authenticate(request,username=username, password=password)
        if user is  not None:
            
            login(request,user)
           
            user_profile = request.user
            # check if the subscription expiry date reached
            if not user_profile.check_subscription():
                messages.error(request, 'Your subscription has expired. Please subscribe to continue.')
                return redirect('subscription_page')
            # Check if subscription is active
            if user_profile.subscription_active == True :
                #login(request,user)
                messages.success(request,('you are successfuly loged in'))
                return redirect('home')  
            else:
                #logout(request)
                messages.error(request, 'Your subscription has expired. Please subscribe to continue.')
                return redirect('subscription_page')    
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



 

# Handle subscription page and payment initiation
def subscription_page(request):
    user_profile = request.user #user_Profile.objects.get(user=request.user)
    form = SubscriptionForm(request.POST)
    if request.method == 'POST':
        
        if form.is_valid():  # If the form is valid
            subscription_type = request.POST.get('subscription_type')# Get the subscription type
            currency = form.cleaned_data['currency']  # Get the selected currency
            months = request.POST.get('subscription_type')# get the subscription duration
            subscription_type = subscription_type
            subscription_start_date = timezone.now()
            # Set subscription end date based on the chosen subscription type
            duration = int(months)  # e.g., 1 month, 3 months, etc.
            subscription_end_date = timezone.now() + timedelta(days=30 * duration)
            
            # Calculate amount based on user type and subscription duration
            if user_profile.is_student:
               amount = 1000 * int(months)  # $1 per month for students
            elif user_profile.is_teacher:
               amount = 2500* int(months)  # $5 per month for teachers
            elif user_profile.is_institution:
               amount =  5000 * int(months)  # $10 per month for institutions
            user_profile.subscription_amount = amount

            # store the calculated varriables in sessions to be retrieved in the payment success view
            request.session['subscription_type'] = subscription_type
            request.session['currency'] = currency
            request.session['amount'] = amount
            request.session['subscription_start_date'] = subscription_start_date.isoformat()
            request.session['subscription_end_date'] = subscription_end_date.isoformat()
            request.session['duration'] = duration
            request.session['months'] = months

            
        
            # Process payment via Flutterwave
            tx_ref = f"txref-{uuid.uuid4()}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    # Store user information and tx_ref in session for later use
           
            headers = {
                'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',  # API Key from settings
                'Content-Type': 'application/json',
            }
        
            # Data to be sent to Flutterwave for payment processing
            payload = {
                "tx_ref":tx_ref,  # Transaction reference
                "amount":amount,  # Amount to be charged https://461b-197-239
                "currency": currency,  # Currency
                "payment_options": "card, mobilemoneyuganda,mobilemoneykenya, ussd,banktransfer",
                "redirect_url": "https://learnli-production.up.railway.app/payment_success",  # Redirect URL after payment
                "customer": {
                    "email": user_profile.email,  # User's email for payment receipt
                    "phonenumber": user_profile.contact,  # User's phone number
                    "name": user_profile.username  # User's name
                },
                "customizations": {
                    "title": "Learnli Subscription Payment",  # Title of the payment
                    "description": f"{user_profile.username.capitalize()} subscription",  # Description of the payment
                    # "logo": "http://yourlogo.com/logo.png"
                }
            }
            # Make the API request to Flutterwave
            try:
                    response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)

                    # Check if the request was successful
                    if response.status_code == 200:
                        messages.success(request, 'Subscription successful!')
                        # if a success, flatterwavw will return a json data structure containg the satatus, link and some other info.
                        payment_link = response.json().get('data').get('link')# collect the link to the flatterwave checkout page and store it into payment_link varriable
                        
                        return redirect(payment_link)  # Redirect to the payment page(the flatterwave checkout page)
                    else:
                        # Log the error and render an error page with the message from Flutterwave
                        messages.error(request, 'Subscription failed!')
                        error_message = response.json().get('message')
                        return render(request, 'payment_error.html', {'error': error_message})

            except Exception as e:
                    # Handle exceptions such as network issues
                    return render(request, 'payment_error.html', {'error': f"An error occurred: {str(e)}"})

        
    form = SubscriptionForm()  # Initialize an empty form
    return render(request, 'subscription_page.html', {'form':form,'user_profile': user_profile,})
'''
def payment_success(request):
    # Retrieve transaction reference
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')

    # Retrieve values from the session
    subscription_type = request.session.get('subscription_type')
    currency = request.session.get('currency')
    amount = request.session.get('amount')
    subscription_start_date_str = request.session.get('subscription_start_date')
    subscription_expiry_date_str = request.session.get('subscription_end_date')
    duration = request.session.get('duration')
    months = request.session.get('months')

    # Parse dates safely
    subscription_start_date = None
    subscription_expiry_date = None

    try:
        if subscription_start_date_str:
            subscription_start_date = parse_datetime(subscription_start_date_str)
        if subscription_expiry_date_str:
            subscription_expiry_date = parse_datetime(subscription_expiry_date_str)
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        messages.error(request, "Invalid subscription dates.")
        return redirect('home')

    # Check if transaction reference is missing
    if not tx_ref:
        messages.error(request, "Transaction reference not found.")
        return redirect('home')

    # Construct the Flutterwave API URL for transaction verification
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
    }

    try:
        # Call the Flutterwave API to verify the transaction
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if request was successful
        data = response.json()

        # Debugging: Output the entire response for checking
        print("Response from Flutterwave:", data)

        # Check if transaction was successful
        if data.get('status') == 'success' and data.get('data', {}).get('status') == 'successful':
            # Ensure the user is authenticated before updating profile
            if request.user.is_authenticated:
                user_profile = request.user
                user_profile.subscription_active = True
                user_profile.subscription_amount = amount
                user_profile.currency_choice = currency
                user_profile.subscription_type = months
                user_profile.subscription_end_date = subscription_expiry_date
                user_profile.subscription_start_date = subscription_start_date
                user_profile.save()

                messages.success(request, "Subscription activated successfully.")
                return redirect('home')
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
'''
def payment_success(request):
    # Retrieve transaction reference
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')
    # Retrieve values from the session
    subscription_type = request.session.get('subscription_type')
    currency = request.session.get('currency')
    amount = request.session.get('amount')
    subscription_start_date = parse_datetime(request.session.get('subscription_start_date'))
    subscription_expiry_date = parse_datetime(request.session.get('subscription_end_date'))
    duration = request.session.get('duration')
    months = request.session.get('months')
    
     
    if  subscription_expiry_date:
        #subscription_expiry_date =datetime.fromisoformat(subscription_end_date)
        #print('this subscription will expire on:',subscription_expiry_date)
        if not tx_ref:
            messages.error(request, "Transaction reference not found.")
            return redirect('home')

    # Construct the Flutterwave API URL for transaction verification
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
    }
    
    try:
        # Call the Flutterwave API to verify the transaction
        response = requests.get(url, headers=headers)
        print(response.status_code)
        response.raise_for_status()  # Check if request was successful
        data = response.json()

        # Debugging: Output the entire response for checking
        print("Response from Flutterwave:", data)

        # Check if transaction was successful
        if data.get('status') == 'success' and data.get('data', {}).get('status') == 'successful':
            # Ensure the user is authenticated before updating profile
            if request.user.is_authenticated:
                user_profile = request.user
                user_profile.subscription_active = True
                user_profile.subscription_amount = amount
                user_profile.currency_choice = currency 
                user_profile.subscription_type = months
                user_profile.subscription_end_date = subscription_expiry_date
                user_profile.subscription_start_date = subscription_start_date

                #user_Profile.subscription_end_date = subscription_expiry_date
                 
                user_profile.save()
                messages.success(request, "Subscription activated successfully.")
                return redirect('home')
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
     
#Notification System:
def send_subscription_reminders():
    users = user_Profile.objects.filter(subscription_active=True)
    for profile in users:
        days_left = (profile.subscription_end_date - now()).days
        if days_left == 7 or days_left == 2 or days_left == 0:
            send_mail(
                'Subscription Expiration Reminder',
                f' dear{profile.user.username},Your subscription will expire in {days_left} days. Please renew.',
                ' learnli759@gmail.com',
                [profile.user.email],
                fail_silently=False,
            ) 
