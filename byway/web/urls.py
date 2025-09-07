from django.urls import path , include
from web import views


app_name = "web"

urlpatterns = [
    path('',views.index,name="index"),
    path('cources/',views.cources,name="cources"),
    path('instructors/',views.instructors,name="instructors"),
    path('courcesingle/<int:course_id>/',views.courcesingle,name="courcesingle"),
    path('categories/',views.categories,name="categories"),
    path('categories/<int:category_id>/',views.categoriescourses,name="categoriescourses"),
]
