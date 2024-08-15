from django.urls import path
from . import views

urlpatterns = [
    path('blog_list', views.blog_list, name='blog_list'),
    path('post/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('create_blog',views.create_blog,name='create_blog'),
    path('delete_post/<post_id>',views.delete_post, name='delete_post'),
    path('edit_post/<post_id>',views.edit_post, name='edit_post'),
]
 