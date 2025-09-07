from django import forms 
from django.contrib.auth.models import User
from users.models import PlatformReview

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password"]
        widgets = {
            "password": forms.widgets.PasswordInput()
        }


class PlatformReviewForm(forms.ModelForm):
    class Meta:
        model = PlatformReview
        fields = ['rating','review_text']
        widgets = {
            'review_text':forms.Textarea(attrs={'rows':4}),
        }