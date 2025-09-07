from django.shortcuts import render , get_object_or_404 , reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course , Enrollment


@login_required
def buy_course_view(request,course_id):
    if request.method == "POST":
        course = get_object_or_404(Course,id=course_id)
        student = request.user

        if Enrollment.objects.filter(student=student , course=course).exists():
            messages.info(request,"You are already enrolled this course")
        else:
            Enrollment.objects.create(student=student,course=course)
            messages.success(request,f'Success! You can now access"{course.title}".')
        
    return HttpResponseRedirect(reverse('courses:my_courses'))


@login_required
def my_courses_view(request):
    enrollments = Enrollment.objects.filter(student=request.user)

    context = {
        'title':'My Courses',
        'enrollments':enrollments,
    }
    return render(request,'courses/my_courses.html',context)