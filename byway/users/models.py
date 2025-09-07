from django.db import models
from django.contrib.auth.models import User
from courses.models import Enrollment, Review
from django.core.validators import MinValueValidator , MaxValueValidator

# Create your models here.

class Profile(models.Model):
    class Role(models.TextChoices):
        LEARNER = 'LEARNER' , 'Learner'
        INSTRUCTOR = 'INSTRUCTOR' , 'Instructor'
        ADMIN = 'ADMIN','Admin'
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=50,choices=Role.choices, default=Role.LEARNER)
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',default='profile_pics/default.png')
    title = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Senior UI/UX Designer")


    @property
    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR
    
    @property
    def total_students(self):
       
        if self.is_instructor:
            # Filter enrollments where the course's instructor is this user
            return Enrollment.objects.filter(course__instructor=self.user).count()
        return 0
    
    
    @property
    def total_courses(self):
        if self.is_instructor:
            return self.user.courses_created.count()
        return 0
    
    @property
    def total_reviews(self):
        
        if self.is_instructor:
            return Review.objects.filter(course__instructor=self.user).count()
        return 0
    
    def __str__(self):
        return f'{self.user.username} Profile'

    
class PlatformReview(models.Model):
    student = models.OneToOneField(User,on_delete=models.CASCADE)
    review_text = models.TextField(max_length=250)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"Platform review by {self.student.username}"