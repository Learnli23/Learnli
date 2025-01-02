from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exam,Answer,Test,Test_answer,RegisterforExam,Test_answer_response,Exam_answer_response
from .forms import AnswerForm ,ExamForm,TestForm,Test_answerForm,Test_answer_responseForm,Exam_answer_responseForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from users.models import user_Profile


# Create your views here.
 # creating an exam
@login_required
def exam(request): 
    submitted = False
    if request.method == 'POST':
        form =ExamForm(request.POST, request.FILES)
        if form.is_valid():
            exam=form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            form.save() 
            return HttpResponseRedirect('/exams?submitted = True')

    else:
         form = ExamForm()
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'Exam.html' ,{'form':form, 'submitted':submitted})


# reistering for the xam view
@login_required
def register(request): 
    candidate_profile = request.user #created_by in  request.user.follows.all
   
    # Filter exams where the creator is in the 'follows' list
    follows = candidate_profile.follows.all()
    exams = Exam.objects.filter(created_by__in=follows).exclude(candidates=candidate_profile)

    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        exam = get_object_or_404(Exam, id=exam_id)
        exam.candidates.add(candidate_profile)
        messages.success(request,('you have successfully registered for this examination'))
        return redirect('home')

    return render(request, 'RegisterforExamForm.html', {'exams': exams})

 

#All students who registered for exams created by the logged-in teacher.
@login_required
def examRegister(request):
    teacher_profile = request.user
   
    # Fetch all exams created by this teacher
    teacher_exams = Exam.objects.filter(created_by=teacher_profile,candidates__isnull =False).distinct()
    # Collect all students registered for those exams
    candidates =user_Profile.objects.filter(exam_registered__created_by=teacher_profile).distinct()

    return render(request, 'Examregistration.html', {'candidates': candidates})

 

#deleting a canndidate
@login_required
def delete_candidate(request, exam_id,candidate_id):
        exam = get_object_or_404(Exam, id=exam_id)
        exam.candidates.remove(candidate_id)
        messages.success(request,('candidate Deleted!'))
        return redirect('examRegister')


@login_required
def answer(request,exam_id): 
    exam =Exam.objects.get( pk = exam_id)
    submitted = False
    if request.method == 'POST':
        form =AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.Answered_by = request.user
            answer.Answered_to = exam.created_by
            answer.Examination_name = exam
            answer.Cours_name =exam.Cours_name
            answer.semester = exam.semester
            answer.save()
            form.save() 
            return HttpResponseRedirect('/answers?submitted = True')

    else:
         form = AnswerForm()
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'Answer.html' ,{'form':form, 'submitted':submitted,'exam':exam})    




# for inbox
@login_required
def answers(request):
    answers = Answer.objects.all().order_by('-Date')
    return render(request, 'Answers.html',{
        'answers':answers
    })
    


# for out box
@login_required
def exams(request):
    exams = Exam.objects.filter(release = True).order_by('-Date')
    candidates = RegisterforExam.objects.all()
    return render(request, 'exams.html',{
        'exams':exams,'candidates':candidates,
    })

# my exams
@login_required
def my_exams(request):
    exams = Exam.objects.filter(created_by = request.user).order_by('-Date')
    candidates = RegisterforExam.objects.all()
    return render(request, 'my_exams.html',{
        'exams':exams,'candidates':candidates,
    })





@login_required
def delete_exam(request, exam_id):
        exam= Exam.objects.get(pk = exam_id)
        exam.delete()
        messages.success(request,('Exam Deleted!!'))
        return redirect('exams')    



@login_required
def edit_exam(request, exam_id):
    exams = Exam.objects.get( pk = exam_id)
    form = ExamForm( request.POST or None, request.FILES or None, instance=exams)
    if form.is_valid():
           form.save()
           return redirect('exams')
    

    return render(request, 'edit_exam.html', {
        "exams":exams,
        'form':form,
    })


@login_required
def test(request): 
    submitted = False
    if request.method == 'POST':
        form =TestForm(request.POST, request.FILES)
        if form.is_valid():
            test=form.save(commit=False)
            test.created_by = request.user
            test.save()
            form.save() 
            return HttpResponseRedirect('/tests?submitted = True')

    else:
         form = TestForm()
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'Test.html' ,{'form':form, 'submitted':submitted})





@login_required
def test_answer(request,test_id): 
    test = Test.objects.get( pk = test_id)
    submitted = False
    if request.method == 'POST':
        form =Test_answerForm(request.POST, request.FILES)
        if form.is_valid():
            test_answer=form.save(commit=False)
            test_answer.Answered_by = request.user
            test_answer.Answered_to =test.created_by
            test_answer.semester = test.semester
            test_answer.Subject_name = test.Subject_name
            test_answer.save()
            form.save() 
            return HttpResponseRedirect('/test_answers?submitted = True')

    else:
         form = Test_answerForm()
         if 'submitted' in request.GET:
            submitted = True

    return render(request,'Test_answer.html' ,{'form':form, 'submitted':submitted,'test':test})    



def tests(request):
    tests = Test.objects.filter(release = True).order_by('-Date').order_by('-Date')
    return render(request, 'tests.html',{
        'tests':tests
    })


# my tests
@login_required
def my_tests(request):
    tests = Test.objects.filter(created_by = request.user).order_by('-Date')
    candidates = RegisterforExam.objects.all()
    return render(request, 'my_tests.html',{
        'tests':tests,'candidates':candidates,
    })



def test_answers(request):
    test_answers = Test_answer.objects.all().order_by('-Date')
    return render(request, 'test_answers.html',{
        'test_answers':test_answers
    })    



@login_required
def delete_test(request, test_id):
        test= Test.objects.get(pk = test_id)
        test.delete()
        messages.success(request,('Test Deleted!!'))
        return redirect('tests')    



@login_required
def edit_test(request, test_id):
    tests = Test.objects.get( pk = test_id)
    form = TestForm( request.POST or None, request.FILES or None, instance=tests)
    if form.is_valid():
           form.save()
           return redirect('tests')
    

    return render(request, 'edit_test.html', {
        "tests":tests,
        'form':form,
    })



 
@login_required
def test_answer_response(request,pk):
     submitted = False
     if request.method == 'POST':
           test_answer =get_object_or_404( Test_answer, pk=pk)
           form = Test_answer_responseForm(request.POST,request.FILES)
           if form.is_valid():
               test_response = form.save(commit=False)
               test_response.Subject= test_answer.Subject_name
               test_response.answer = test_answer
               test_response.semester = test_answer.semester
               test_response.response_by = request.user
               test_response.response_to = test_answer.Answered_by
               test_response.save()
               form.save()
               return HttpResponseRedirect('/test_answers?submitted = True')
     else:
          form = Test_answer_responseForm()
          if 'submitted' in request.GET:
            submitted = True

     return render(request,'test_answer_response.html' ,{'form':form , 'submitted':submitted,}) 



@login_required
def test_answer_responses(request):
    test_answer_responses= Test_answer_response.objects.all().order_by('-submitted_at')
 
    return render(request, 'test_answer_responses.html',{
        'exams':exams,'test_answer_responses':test_answer_responses,
    })
   

@login_required
def exam_answer_response(request,pk):
     submitted = False
     if request.method == 'POST':
           exam_answer =get_object_or_404( Answer, pk=pk)
           form = Exam_answer_responseForm(request.POST,request.FILES)
           if form.is_valid():
               exam_response = form.save(commit=False)
               exam_response.Course= exam_answer.Cours_name
               exam_response.Examination = exam_answer.Examination_name
               exam_response.semester = exam_answer.semester
               exam_response.responseby = request.user
               exam_response.responseto = exam_answer.Answered_by
               exam_response.save()
               form.save()
               return HttpResponseRedirect('/answers?submitted = True')
     else:
          form = Exam_answer_responseForm()
          if 'submitted' in request.GET:
            submitted = True

     return render(request,'exam_answer_response.html' ,{'form':form , 'submitted':submitted,}) 


@login_required
def exam_answer_responses(request):
    exam_answer_responses= Exam_answer_response.objects.all().order_by('-submittedat')
 
    return render(request, 'exam_answer_responses.html',{
        'exams':exams,'exam_answer_responses':exam_answer_responses,
    })


@login_required
def edit_test_asnswer_response(request, response_id):
    tests  = Test_answer_response.objects.get( pk = response_id)
    form = Test_answer_responseForm( request.POST or None, request.FILES or None, instance=tests)
    if form.is_valid():
           form.save()
           return redirect('test_answer_responses')
    

    return render(request, 'edit_test_answer_response.html', {
        "tests":tests,
        'form':form,
    })




@login_required
def delete_test_answer_response(request, response_id):
        test= Test_answer_response.objects.get(pk = response_id)
        test.delete()
        messages.success(request,('Response Deleted!!'))
        return redirect('test_answer_responses')  



@login_required
def edit_exam_asnswer_response(request, response_id):
    exam  = Exam_answer_response.objects.get( pk = response_id)
    form = Exam_answer_responseForm( request.POST or None, request.FILES or None, instance=exam)
    if form.is_valid():
           form.save()
           return redirect('exam_answer_responses')
    

    return render(request, 'edit_exam_answer_response.html', {
        "texam":exam,
        'form':form,
    })


@login_required
def delete_exam_answer_response(request, response_id):
        exam= Exam_answer_response.objects.get(pk = response_id)
        exam.delete()
        messages.success(request,('Response Deleted!!'))
        return redirect('exam_answer_responses')   


@login_required
def Exam_results(request):
    exam_results = Exam_answer_response.objects.all().order_by('-submittedat')
    return render(request, 'exam_results.html', {
        'exams':exams, 'exam_results': exam_results,
         
    })

 
@login_required
def test_results(request):
    test_results= Test_answer_response.objects.all().order_by('-submitted_at')
 
    return render(request, 'test_results.html',{
        'exams':exams,'test_results':test_results,
    })
