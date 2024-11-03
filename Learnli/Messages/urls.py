from django.urls import path
from . import views
 

urlpatterns =[
    path('inbox',views.inbox,name='inbox'),
    path('outbox',views.outbox,name='outbox'),
    path('compose',views.compose,name='compose'),
    path('delete_message/<message_id>',views.delete_message, name='delete_message'),
    path('contact-message/', views.contact_message, name='contact_message'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/add/', views.add_event, name='add_event'),
    path('delete_event/<event_id>',views.delete_event, name='delete_event'),
    path('edit_event/<event_id>',views.edit_event, name='edit_event'),
]
