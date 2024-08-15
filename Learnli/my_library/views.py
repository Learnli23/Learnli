from django.shortcuts import render,get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from .models import Content,Reaction,Ebook,Section,Sub_Section,Reviews
from users.models import  user_Profile
from .forms import ContentForm, CommentForm,EbookForm,sub_SectionForm,SectionForm,ReviewForm
from django.forms import modelformset_factory
from django.contrib import messages
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






@login_required
def content_detail(request, pk):
    content = get_object_or_404(Content, pk=pk)
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
        comment_form = CommentForm()
    return render(request, 'content_detail.html', {
        'content': content,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def content_list(request):
    contents = Content.objects.all().order_by('-upload_date')
    return render(request, 'content_list.html', {'contents': contents})

@login_required
def profile_library(request,pk):
    profile = get_object_or_404(user_Profile, pk=pk)
    contents = Content.objects.all().order_by('-upload_date')
    return render(request, 'profile_library.html', {'contents': contents, 'profile':profile})    



#Ebook views
@login_required
def book_list(request):
    books = Ebook.objects.all()
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
        form = ReviewForm()
    return render(request, 'book_details.html', {
        'book': book,
        'sections': sections,
         'reactions': reactions,
        'form': form,
        
        })





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