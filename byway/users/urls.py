
from django.urls import path , include
from users import views

app_name = "users"

urlpatterns = [
    path('login/', views.login, name="login" ),
    path('logout/',views.logout, name="logout"),
    path('signup/',views.signup, name="signup"),
    path('become-instructor/',views.become_instructor, name="become_instructor"),
    path('leave-instructor/',views.leave_instructor_role, name="leave_instructor_role"),
    path('review-platform/',views.review_platform_view, name="review_platform"),

]
