from django.shortcuts import render,get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .models import Content,Reaction,Ebook,Section,Sub_Section,Reviews,Book_Payment
from users.models import  user_Profile
from .forms import ContentForm, CommentForm,EbookForm,sub_SectionForm,SectionForm,ReviewForm
from django.forms import modelformset_factory
from django.contrib import messages
import json
import uuid
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
 
# Create your views here.


@login_required

def upload_content(request):
    submitted = False
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.save()
            return redirect('content_list')



    else:
        form = ContentForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'upload_content.html', {'form': form})

# editing content
@login_required
def edit_content(request, content_id):
    content = Content.objects.get(pk = content_id)
    form = ContentForm( request.POST or None, request.FILES or None, instance=content)
    if form.is_valid():
           form.save()
           return redirect('content_list')
    return render(request, 'edit_content.html', {
        "content":content,
        'form':form,
    })

# delete ebook
@login_required
def delete_content(request, content_id):
        content= Content.objects.get(pk = content_id)
        content.delete()
        messages.success(request,('Content Deleted!!'))
        return redirect('content_list')    

# content details view
@login_required
def content_detail(request, pk):
    content = get_object_or_404(Content, pk=pk)
    book_content_type = ContentType.objects.get_for_model(Content)  # Get ContentType for ebook mode
    has_paid = content.paid_users.filter(id=request.user.id).exists()
    if has_paid or request.user == content.author:
            comments = content.comments.all()
            if request.method == 'POST':
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.Commenter = request.user
                    comment.content = comment
                    comment.save()
                    return redirect('content_detail', pk=content.pk)        
                
    else:
        # Redirect to payment page
        messages.info(request, "You need to purchase this book to access its content.")
        return redirect('content_payment_page', content_id = content.id) 
    comment_form = CommentForm()    
    return render(request, 'content_detail.html', {
        'content': content,
        'comments': comments,
        'comment_form': comment_form,
        'book_content_type':book_content_type,
    })

# content payment page.
@login_required
@csrf_exempt
def content_payment_page(request, content_id):
    content = Content.objects.get(id=content_id)
    user_profile=request.user
    content_id = content.id
     
    if request.method == "POST":
        # Extract currency from the form
        currency = request.POST.get('currency')
        price = content.price
        tx_ref = f"book_{content_id}_txref--{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
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
                "redirect_url": "YOUR REDIRCT URL",  # Redirect URL after payment
                "customer": {
                    "email": user_profile.email,  # User's email for payment receipt
                    "phonenumber": user_profile.contact,  # User's phone number
                    "name": user_profile.username  # User's name
                },
                "customizations": {
                    "title": "Learnli book Payment",  # Title of the payment
                    "description": f"{user_profile.username.capitalize()} book payment",  # Description of the payment
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
    return render(request,'content_payment_page.html', {'content': content})        

#content payment success hundling
@login_required
@csrf_exempt
def content_payment_success(request): 
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')
    #book_id = request.session.get('book_id')
    content_id, rest_of_tx_ref = extract_content_and_rest_of_tx_ref_from_tx_ref(tx_ref)
    print('transaction_id:',transaction_id)
    print('tx_ref is:',tx_ref)
    print('the content id is:',content_id)
    # Verify the payment
    #flutterwave_url = f"https://api.flutterwave.com/v3/transactiools/{transaction_id}/verify"
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

            # Debugging: Output the entire response for checking
            print("Response from Flutterwave:", payment_data)

            # Check if transaction was successful
            if payment_data.get('status') == 'success':# and payment_data.get('payment_data', {}).get('status') == 'successful':
                # Ensure the user is authenticated before updating profile
                if request.user.is_authenticated:
                    user_profile = request.user
                     # Record the payment
                    content = Content.objects.get(id = content_id)
                    print('this is the content id:',content_id)
                    # Create payment record
                    #Book_Payment.objects.create(user=user_profile, book=book, transaction_id=transaction_id)
                    # Add user to paid_users for the book
                    content.paid_users.add(user_profile)

                    messages.success(request, "Payment successful! You now have access to the book.")
                    return redirect('content_detail',content.id)
                    
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
def extract_content_and_rest_of_tx_ref_from_tx_ref(tx_ref):
    # Assuming tx_ref format is 'book_{book_id}_user_{user_id}'
     _,content_id, rest_of_tx_ref= tx_ref.split('_',2)
     return int(content_id), str(rest_of_tx_ref)

@login_required
def content_list(request):
    contents = Content.objects.filter(is_hiden = False).order_by('-upload_date')
    return render(request, 'content_list.html', {'contents': contents})

@login_required
def profile_library(request,pk):
    profile = get_object_or_404(user_Profile, pk=pk)
    contents = Content.objects.all().order_by('-upload_date')
    return render(request, 'profile_library.html', {'contents': contents, 'profile':profile})    

#Ebook views
@login_required
def book_list(request):
    books = Ebook.objects.filter(is_hiden = False)
    return render(request, 'book_list.html', {'books': books})

#Profile Ebook views
@login_required
def profile_books(request,pk):
    profile = get_object_or_404(user_Profile, pk=pk)
    books = Ebook.objects.all().order_by('-date_updated')
    return render(request, 'profile_books.html', {'books': books, 'profile':profile})  


# editing ebook
@login_required
def edit_ebook(request, ebook_id):
    ebooks =  Ebook.objects.get(pk = ebook_id)
    form = EbookForm( request.POST or None, request.FILES or None, instance=ebooks)
    if form.is_valid():
           form.save()
           return redirect('book_list')
    

    return render(request, 'edit_ebook.html', {
        "ebooks":ebooks,
        'form':form,
    })

# delete ebook
@login_required
def delete_ebook(request, ebook_id): 
        ebook= Ebook.objects.get(pk = ebook_id)
        ebook.delete()
        messages.success(request,('Ebook Deleted!!'))
        return redirect('book_list')    
        
def book_details(request, pk):
    book = get_object_or_404(Ebook, pk=pk)
    ebook_content_type = ContentType.objects.get_for_model(Ebook)  # Get ContentType for ebook mode
    has_paid = book.paid_users.filter(id=request.user.id).exists()
    
    if has_paid or request.user == book.author:
        sections = book.sections.all()
        reactions = book.reviews.all()
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                reaction = form.save(commit=False)
                reaction.reviewer = request.user
                reaction.book = book
                reaction.save()
                return redirect('book_detail', pk=book.pk)
    else:
        # Redirect to payment page
        messages.info(request, "You need to purchase this book to access its content.")
        return redirect('book_payment_page', book_id=book.id) 
    form = ReviewForm()
    return render(request, 'book_details.html', {
            'book': book,
            'sections': sections,
            'reactions': reactions,
            'form': form,
            'ebook_content_type':ebook_content_type
            })


@login_required
@csrf_exempt
def book_payment_page(request, book_id):
    book = Ebook.objects.get(id=book_id)
    user_profile=request.user
    book_id = book.id
     
    if request.method == "POST":
        # Extract currency from the form
        currency = request.POST.get('currency')
        price = book.price
        tx_ref = f"book_{book_id}_txref--{datetime.now().strftime('%Y%m%d%H%M%S')}"
        #tx_ref = f"txref--{datetime.now().strftime('%Y%m%d%H%M%S')}"
        #request.session['book_id'] = book_id
        
        # Sample Flutterwave API request
        
        headers = {
                'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',  # API Key from settings
                'Content-Type': 'application/json',
            }


       
        payload = {
                "tx_ref":tx_ref,  # Transaction reference
                "amount":float(price),  # Amount to be charged
                "currency":currency,  # Currency
                "payment_options": "card, mobilemoneyuganda, ussd,banktransfer",
                "redirect_url": "YOUR REDIRECT URL",  # Redirect URL after payment
                "customer": {
                    "email": user_profile.email,  # User's email for payment receipt
                    "phonenumber": user_profile.contact,  # User's phone number
                    "name": user_profile.username  # User's name
                },
                "customizations": {
                    "title": "Learnli book Payment",  # Title of the payment
                    "description": f"{user_profile.username.capitalize()} ebook payment",  # Description of the payment
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
    return render(request,'ebook_payment_page.html', {'book': book})        



@login_required
@csrf_exempt
def book_payment_success(request): 
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')
    #book_id = request.session.get('book_id')
    book_id, rest_of_tx_ref = extract_book_and_user_from_tx_ref(tx_ref)
 
    #flutterwave_url = f"https://api.flutterwave.com/v3/transactiools/{transaction_id}/verify"
    flutterwave_url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
    }

    try:
            # Call the Flutterwave API to verify the transaction
            response = requests.get(flutterwave_url, headers=headers)
          
            response.raise_for_status()  # Check if request was successful
            payment_data = response.json()


            # Check if transaction was successful
            if payment_data.get('status') == 'success':# and payment_data.get('payment_data', {}).get('status') == 'successful':
                # Ensure the user is authenticated before updating profile
                if request.user.is_authenticated:
                    user_profile = request.user
                     # Record the payment
                    book = Ebook.objects.get(id = book_id)
                   
                
                    # Add user to paid_users for the book
                    book.paid_users.add(user_profile)

                    messages.success(request, "Payment successful! You now have access to the book.")
                    return redirect('book_details',book.id)
                    
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
def extract_book_and_user_from_tx_ref(tx_ref):
    # Assuming tx_ref format is 'book_{book_id}_user_{user_id}'
     _,book_id, rest_of_tx_ref= tx_ref.split('_',2)
     return int(book_id), str(rest_of_tx_ref)

# adding abook
@login_required
def add_book(request):
    if request.method == 'POST':
        form = EbookForm(request.POST,request.FILES )
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.save()

            return redirect('book_list')
    else:
        form = EbookForm()
    return render(request, 'add_book.html', {'form': form})



def add_section(request, book_pk):
    book = get_object_or_404(Ebook, pk=book_pk)
    SectionFormSet = modelformset_factory(Section, form=SectionForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = SectionFormSet(request.POST, request.FILES, queryset=book.sections.all())
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.ebook = book
                instance.section_author = request.user
                instance.save()
            return redirect('book_details', pk=book.pk)
    else:
        formset = SectionFormSet(queryset=book.sections.all())

    return render(request, 'add_section.html', {'book': book, 'formset': formset}) 


def add_sub_section(request, section_pk):
    section = get_object_or_404(Section, pk=section_pk)
    sub_SectionFormSet = modelformset_factory(Sub_Section, form=sub_SectionForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = sub_SectionFormSet(request.POST, request.FILES, queryset=section.sub_sections.all())
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.section = section
                instance.subsection_author = request.user
                instance.save()
            return redirect('section_details', pk=section.pk)
    else:
        formset = sub_SectionFormSet(queryset=section.sub_sections.all())

    return render(request, 'add_sub_section.html', {'section': section, 'formset': formset})       

def section_details(request, pk):
    section = get_object_or_404(Section, pk=pk)
    sub_sections = section.sub_sections.all()
    return render(request, 'section_details.html', {'section': section, 'sub_sections': sub_sections})    
