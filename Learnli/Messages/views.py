from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import composeForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages

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