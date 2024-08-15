from django.urls import path
from . import views

urlpatterns = [
    path('upload_content', views.upload_content, name='upload_content'),
    path('content_detail/<int:pk>/', views.content_detail, name='content_detail'),
    path('edit_content/<content_id>',views.edit_content, name='edit_content'),
    path('delete_content/<content_id>',views.delete_content, name='delete_content'),
    #path('content/<int:pk>/purchase/', views.purchase_content, name='purchase_content'),
    path('content_list', views.content_list, name='content_list'),
    path('profile_library/<int:pk>/', views.profile_library, name='profile_library'),
    path('profile_books/<int:pk>/', views.profile_books, name='profile_books'),
    #Ebook urls
    path('book_list', views.book_list, name='book_list'),
    path('edit_ebook/<ebook_id>',views.edit_ebook, name='edit_ebook'),
    path('book/<int:pk>/', views.book_details, name='book_details'),
    path('delete_ebook/<ebook_id>',views.delete_ebook, name='delete_ebook'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:book_pk>/add-section/', views.add_section, name='add_section'),
    path('section/<int:section_pk>/add-sub_section/', views.add_sub_section, name='add_sub_section'),
    path('section/<int:pk>/', views.section_details, name='section_details'),
]