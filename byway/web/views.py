from django.shortcuts import render , get_object_or_404
from django.http.response import HttpResponse
from courses.models import Course,Category,Lecture,LectureComment,Review,StudyMaterial,Section
from django.db.models import Count,Avg
from users.models import Profile, PlatformReview

# Create your views here.

def index(request):
    cources = Course.objects.filter(is_deleted = False,is_draft=False)[:4]
    categories = Category.objects.annotate(course_count=Count('courses'))[:4]
    instructor = Profile.objects.filter(role="INSTRUCTOR")
    platform_reviews = PlatformReview.objects.order_by('-created_at')
    context = {
        "title":"homepage",
        "cources":cources,
        "categories":categories,
        "instructor":instructor,
        "platform_reviews":platform_reviews,
    }
    return render(request, 'web/index.html',context=context)


def cources(request):
    cources = Course.objects.filter(is_deleted = False,is_draft=False)
    return render(request,'courses/cources.html',context={"cources":cources})

def categories(request):
    categories = Category.objects.annotate(course_count=Count('courses'))
    return render(request,'courses/categories.html',context={"categories":categories})

def instructors(request):
    instructors = Profile.objects.filter(role="INSTRUCTOR")
    return render(request,'courses/instroctors.html',context={"instructors":instructors})
def courcesingle(request,course_id):
    course_obj = get_object_or_404(Course, id=course_id)
    review_count = course_obj.reviews.count()
    avg_rating = course_obj.reviews.aggregate(average=Avg('rating'))['average'] or 0
    rating_breakdown = []
    platform_reviews = PlatformReview.objects.order_by('-created_at')[:4]

    if review_count > 0:
        rating_counts = course_obj.reviews.values('rating').annotate(count=Count('id'))
        counts_dict = {item['rating']: item['count'] for item in rating_counts}


        for star in range(5, 0, -1):
            count = counts_dict.get(star, 0)
            percentage = (count / review_count) * 100
            rating_breakdown.append({
                'star': star,
                'count': count,
                'percentage': percentage,
            })
    else:
        # If there are no reviews, create a default empty breakdown
        for star in range(5, 0, -1):
            rating_breakdown.append({'star': star, 'count': 0, 'percentage': 0})

    
    related_courses = Course.objects.filter(
        category = course_obj.category,is_draft=False
    ).exclude(
        id=course_id
    )[:4]
    context = {
        "course":course_obj,
        'related_courses': related_courses,
        'avg_rating':avg_rating,
        'review_count': review_count,
        'rating_breakdown': rating_breakdown,
        "platform_reviews": platform_reviews,
        
    }
    return render(request,'courses/singlepage.html',context)

def categoriescourses(request,category_id):
    course_obj = Course.objects.filter(category__id=category_id)
    context = {
        "cources":course_obj,
    }
    return render(request,'courses/categoriesingle.html',context)
