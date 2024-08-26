from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import composeForm, ContactMessageForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from .models import CalendarEvent
from .forms import CalendarEventForm
from django.utils import timezone

#Reminder views


@login_required
def calendar_view(request):
    events = CalendarEvent.objects.filter(user=request.user, event_date__gte=timezone.now()).order_by('event_date')
    return render(request, 'calendar.html', {'events': events})

@login_required
def add_event(request):
    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('calendar')
    else:
        form = CalendarEventForm()
    return render(request, 'add_event.html', {'form': form})


# contact message view
def contact_message(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.name = request.user
            message.email =request.user.email
            form.save()
            messages.success(request, 'Your message has been sent!')
            return redirect('home')  # or redirect to 'about' if you prefer
    else:
        form = ContactMessageForm()
    return render(request, 'contact_form.html', {'form': form})


def delete_message(request, message_id):
    message= Message.objects.get(pk = message_id)
    message.delete()
    messages.success(request,('message Deleted!!'))
    return redirect('outbox')

@login_required
def compose(request): 
    submitted = False
    if request.method == 'POST':
        form =composeForm(request.POST, request.FILES)
        if form.is_valid():
            message=form.save(commit=False)
            message.sender = request.user
            message.save()
            form.save() 
            return HttpResponseRedirect('/outbox?submitted = True')

    else:
         form = composeForm()
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'compose.html' ,{'form':form, 'submitted':submitted})

# for inbox
@login_required
def inbox(request):
    messages = Message.objects.filter(reciepient = request.user).order_by('-timestamp')
    return render(request, 'inbox.html',{
        'messages':messages
    })
# for out box
@login_required
def outbox(request):
    outmsg = Message.objects.filter(sender = request.user).order_by('-timestamp')
    return render(request, 'outbox.html',{
        'outmsg':outmsg
    })