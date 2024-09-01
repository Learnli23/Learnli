from django.db.models import Count
from .models import UserCourseActivity, UserBookActivity, UserTeacherActivity,user_Profile
from .models import Classes
from my_library.models import Ebook

def get_course_recommendations(user):
    # Find courses liked by similar users
    similar_users = UserCourseActivity.objects.filter(
        course__in=UserCourseActivity.objects.filter(user=user, activity_type='liked').values('course')
    ).exclude(user=user).values('user').annotate(count=Count('user')).order_by('-count')
   
    # Get the most common courses liked by similar users
    recommended_courses = Classes.objects.filter(
        id__in=UserCourseActivity.objects.filter(user__in=[u['user'] for u in similar_users], activity_type='liked')
        .values('course').annotate(count=Count('course')).order_by('-count').values('course')
    )
   
    return recommended_courses

def get_book_recommendations(user):
    # Similar process for books
    similar_users = UserBookActivity.objects.filter(
        book__in=UserBookActivity.objects.filter(user=user, activity_type='liked').values('book')
    ).exclude(user=user).values('user').annotate(count=Count('user')).order_by('-count')

    recommended_books = Ebook.objects.filter(
        id__in=UserBookActivity.objects.filter(user__in=[u['user'] for u in similar_users], activity_type='liked')
        .values('book').annotate(count=Count('book')).order_by('-count').values('book')
    )
   
    return recommended_books

def get_teacher_recommendations(user):
    # Similar process for teachers
    similar_users = UserTeacherActivity.objects.filter(
        teacher__in=UserTeacherActivity.objects.filter(user=user, activity_type='followed').values('teacher')
    ).exclude(user=user).values('user').annotate(count=Count('user')).order_by('-count')

    recommended_teachers = user_Profile.objects.filter(
        id__in=UserTeacherActivity.objects.filter(user__in=[u['user'] for u in similar_users], activity_type='followed')
        .values('teacher').annotate(count=Count('teacher')).order_by('-count').values('teacher')
    )
   
    return recommended_teachers