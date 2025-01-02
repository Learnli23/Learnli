from django.contrib import admin
from django.urls import path
from . import views

# create your urls here 
urlpatterns = [ 
    #path('inbox',views.inbox,name='inbox'),
    #path('outbox',views.outbox,name='outbox'),examRegister
    path('exam',views.exam,name='exam'),
    path('my_exams',views.my_exams,name='my_exams'),
    path('my_tests',views.my_tests,name='my_tests'),
    path('answer/<exam_id>',views.answer,name='answer'),
    path('answers',views.answers,name='answers'),
    path('exams',views.exams,name='exams'),
    path('test',views.test,name='test'),
   # path('test_answer',views.test_answer,name='test_answer'),
    path('tests',views.tests,name='tests'),
    path('test_answers',views.test_answers,name='test_answers'),
    path('RegisterforExam',views.register,name='RegisterforExam'),
    path('examRegister',views.examRegister,name='examRegister'),
    path('delete_exam/<exam_id>',views.delete_exam, name='delete_exam'),
    path('edit_exam/<exam_id>',views.edit_exam, name='edit_exam'),
    path('delete_test/<test_id>',views.delete_test, name='delete_test'),
    path('edit_test/<test_id>',views.edit_test, name='edit_test'),
    path('exam/<int:exam_id>/remove_candiate/<int:candidate_id>/',views.remove_candidate, name='remove_candidate'),
    path('test_answer_response/<int:pk>/',views.test_answer_response,name='test_answer_response'),
    path('test_answer_responses',views.test_answer_responses,name='test_answer_responses'),
    path('exam_answer_response/<int:pk>/',views.exam_answer_response,name='exam_answer_response'),
    path('exam_answer_responses',views.exam_answer_responses,name='exam_answer_responses'),
    path('edit_test_answer_response/<response_id>',views.edit_test_asnswer_response, name='edit_test_answer_response'),
    path('delete_test_answer_response/<response_id>',views.delete_test_answer_response, name='delete_test_answer_response'),
    path('edit_exam_answer_response/<response_id>',views.edit_exam_asnswer_response, name='edit_exam_answer_response'),
    path('delete_exam_answer_response/<response_id>',views.delete_exam_answer_response, name='delete_exam_answer_response'),
    path('exam_results',views.Exam_results,name='exam_results'),
    path('test_results',views.test_results,name='test_results'),
    path('test_answer/<test_id>',views.test_answer, name='test_answer'),
    #path('answer/<exam_id>',views.answer, name='answer'),


 ]