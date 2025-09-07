from django.shortcuts import render , reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate , login as auth_login , logout as auth_logout
from users.forms import UserForm , PlatformReviewForm
from django.contrib.auth.models import User
from users.models import Profile , PlatformReview 
from web.functions import generate_form_errors
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request,username=username,password=password)

            if user is not None:
                auth_login(request,user)

                return HttpResponseRedirect("/")

        context = {
            "title":"Login",
            "error":True,
            "message":"invalid username or password"
        }
        return render(request,'users/login.html',context=context)
    else:
        context={
            'title':'Login'
        }
        return render(request,'users/login.html',context=context)

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            Profile.objects.create(user=new_user)
        
           
            auth_login(request,new_user)
            messages.success(request,f"Welcome, {new_user.username}! Your account have been created.")

            return HttpResponseRedirect(reverse("web:index"))
           
        else:
           
            form = UserForm()
            context = {
                'title':'Signup',
                "form":form,
            }
            return render(request,"users/signup.html",context=context)
    else:
        form = UserForm()
        context={
            "title":"signup",
            "form":form,
        }
        return render(request,"users/signup.html",context=context)


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("web:index"))

@login_required
def become_instructor(request):
    if request.method == "POST":
        try:
            profile = request.user.profile

            profile.role = Profile.Role.INSTRUCTOR
            profile.save()
            

            messages.success(request,'Congragulations! You are now registered as an instructor')
        
        except Profile.DoesNotExist:
            messages.error(request, 'Your profile could not be found. Please contact support.')
        return HttpResponseRedirect(reverse("web:index"))
    
    return HttpResponseRedirect(reverse("web:index"))

@login_required
def leave_instructor_role(request):
    if request.method == "POST":
        try:
            profile = request.user.profile
            profile.role = Profile.Role.LEARNER
            profile.save()
            messages.success(request, 'You have left your instructor role and are now a learner.')
        except Profile.DoesNotExist:
            messages.error(request, 'Your profile could not be found. Please contact support.')


    return HttpResponseRedirect(reverse("web:index"))

@login_required
def review_platform_view(request):
    if PlatformReview.objects.filter(student=request.user).exists():
        messages.info(request,"you have already submitted a review for our platform")
        return HttpResponseRedirect(reverse('web:index'))
    
    if request.method == "POST":
        form = PlatformReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.student = request.user
            review.save()
            messages.success(request, "Thank you for your feedback!")
            return HttpResponseRedirect(reverse('web:index'))
    else:
        form = PlatformReviewForm()

    context = {
        'title': 'Review Our Platform',
        'form': form
    }
    return render(request, 'users/platform_review.html', context)