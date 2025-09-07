from django.contrib import admin
from courses.models import Course,Category,Lecture,Review,Section,LectureComment,StudyMaterial
# Register your models here.

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Lecture)
admin.site.register(Review)
admin.site.register(Section)
admin.site.register(LectureComment)
admin.site.register(StudyMaterial)
