# courses/urls.py
from django.urls import path
from courses import views

app_name = 'courses'

urlpatterns = [
    path('buy/<int:course_id>/',views.buy_course_view,name="buy_course"),
    path('my-courses/',views.my_courses_view,name="my_courses"),
    path('create/',views.create_course,name="create_course"),
    path('my_courses/',views.my_courses,name="my_courses"),
]