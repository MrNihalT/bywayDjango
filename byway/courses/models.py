from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator , MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    caategory_img = models.FileField(upload_to="categoryimage/",default="profile_pics/user.png",null=True,blank=True)
    def __str__(self):
        return self.name
    
    @property
    def total_courses(self):
        return self.courses.count()


class Course(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER = 'BEGINNER' , 'Beginner'
        INTERMEDIATE = "INTERMEDIATE" , "Intermediate"
        ADVANCED = "ADVANCED" , "Advanced"
    
    
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.SET_NULL, null=True)
    instructor = models.ForeignKey(User,related_name="courses_created",on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    offer_percentage = models.PositiveBigIntegerField(
        default=0,
        help_text = "Discount percentage (e.g., 20 for 20%)"
    )
    course_image = models.ImageField(upload_to="course_images/")
    total_time = models.CharField(max_length=20)
    total_lecture = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)
    difficulty = models.CharField(choices=Difficulty.choices,max_length=100,null=False)

    @property
    def final_price(self):
        if self.offer_percentage > 0 and self.offer_percentage < 100:
            discount = (self.price * Decimal(self.offer_percentage)) / 100
            return (self.price - discount).quantize(Decimal('0.01'))
        return self.price
    
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)
        return 0

    @property
    def total_reviews(self):
        return self.reviews.count()

    @property
    def instructor_profile(self):
        return self.instructor.profile
    

    def __str__(self):
        return self.title


class Section(models.Model):
    course = models.ForeignKey(Course,related_name="sections",on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()
    hour = models.IntegerField(default=1,null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} - Section {self.order}: {self.title}'
    

class Lecture(models.Model):
    section = models.ForeignKey(Section,related_name="lectures",on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    order = models.PositiveIntegerField()

    video_file = models.FileField(upload_to="lecture_videos/",blank=True,null=True,help_text="Upload a video file")
    youtub_url = models.URLField(blank=True,null=True,help_text="Or Provide a Youtube video URL")

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title
    

class Review(models.Model):
    course = models.ForeignKey(Course,related_name="reviews",on_delete=models.CASCADE)
    student = models.ForeignKey(User,related_name="reviews",on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f'Rating: {self.rating} by {self.student.username} for {self.course.title}'
    

class StudyMaterial(models.Model):
    lecture = models.ForeignKey(Lecture,related_name="materials",on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='study_materials/')

    def __str__(self):
        return f"{self.title} for {self.lecture.title}"
    

class LectureComment(models.Model):
    lecture = models.ForeignKey(Lecture,related_name="comments",on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',null=True,blank=True,related_name="replies",on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment  by {self.user.username} on {self.lecture.title}"
    

class Enrollment(models.Model):
    student = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course') 

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

