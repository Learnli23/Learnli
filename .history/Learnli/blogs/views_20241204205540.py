from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment
from .forms import CommentForm,BlogForm
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType



# Create your views here.


@login_required
def create_blog(request): 
    submitted = False
    if request.method == 'POST':
        form =BlogForm(request.POST, request.FILES)
        if form.is_valid():
              BlogPost = form.save(commit=False)
              BlogPost.author = request.user 
              BlogPost.save()
              form.save() 
              return redirect('blog_list')
               

    else:
         form = BlogForm()
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'create_blog.html' ,{'form':form, 'submitted':submitted})



def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'posts': posts})

@login_required
def blog_detail(request, post_id):
       post = get_object_or_404(BlogPost, id=post_id)
       comments = post.comments.all()
       if request.method == 'POST':
           form = CommentForm(request.POST)
           if form.is_valid():
               comment = form.save(commit=False)
               comment.author = request.user
               comment.post = post
               comment.save()
               return redirect('blog_detail', post_id=post.id)
       else:
           form = CommentForm()
       return render(request, 'blog_detail.html', {'post': post, 'comments': comments, 'form': form})  


@login_required
def edit_post(request,  post_id):
    post = BlogPost.objects.get(pk = post_id)
    form = BlogForm( request.POST or None, request.FILES or None, instance= post)
    if form.is_valid():
           form.save()
           return redirect('blog_list')
    

    return render(request, 'edit_post.html', {
        "post": post,
        'form':form,
    })




@login_required
def delete_post(request, post_id):
        post = BlogPost.objects.get(pk = post_id)
        post.delete()
        messages.success(request,('post deleted!!'))
        return redirect('blog_list')        

 
@login_required
def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('blog_detail', post_id=post.id)

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    return redirect('blog_detail', post_id=post.id)