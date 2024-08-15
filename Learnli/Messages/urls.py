from django.urls import path
from . import views
 

urlpatterns =[
    path('inbox',views.inbox,name='inbox'),
    path('outbox',views.outbox,name='outbox'),
    path('compose',views.compose,name='compose'),
    path('delete_message/<message_id>',views.delete_message, name='delete_message'),
]
