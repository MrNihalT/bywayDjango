import datetime
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course, Enrollment, Section
# Import the form and the new formset
from courses.forms import CourseForm


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


@login_required()
def create_course(request):
    if not request.user.profile.is_instructor:
        messages.error(request, "You are not authorized to create a course.")
        return HttpResponseRedirect(reverse("web:index"))

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, "Course created successfully!")
            return HttpResponseRedirect(reverse("web:index"))
    else:
        form = CourseForm()
        
    context = {
        "title": "Create New Course",
        "form": form,
    }
    return render(request, "courses/creat.html", context)

@login_required()
def edit_courses(request,id):
    if not request.user.profile.is_instructor:
        messages.error(request, "You are not authorized to Edit a course.")
        return HttpResponseRedirect(reverse("web:index"))
    
    instance = get_object_or_404(Course,id=yuid)
    if instance.instructor != request.user:
        messages.error(request,"you can only edit your own courses")
        return HttpResponseRedirect(reverse("courses:my_courses"))
    
    if request.method == "POST":
        form = CourseForm(request.POST,request.FILES,instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request,"course updated")
            return HttpResponseRedirect(reverse("courses:my_courses"))
    else:
        form = CourseForm(instance=instance)
        
    context = {
        "title":f'Edit Courses : {instance.title}',
        'form':form,
    }
    return render(request,"courses/creat.html",context=context)




@login_required()
def my_courses(request):
    if not request.user.profile.is_instructor:
       messages.error(request,"You are not authorized to view this page")
       return HttpResponseRedirect(reverse("web:index"))


    cources = Course.objects.filter(instructor=request.user)
    context = {
        "title":"My Courses",
        "cources":cources
    }
    return render(request,'courses/instructor_courses.html',context=context)




