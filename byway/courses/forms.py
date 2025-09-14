# courses/forms.py
from django import forms
from .models import Course , Category

class CourseForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100, 
        required=False, 
        label="Create a New Category",
        help_text="If your category isn't in the list, add it here."
    )
    
    class Meta:
        model = Course
        exclude = ('instructor', 'created_at', 'updated_at', 'is_deleted')
        widgets = {
            # ... all your other widgets ...
            'category': forms.Select(attrs={'class': 'input-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the original category field not required
        self.fields['category'].required = False

    
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category_name = cleaned_data.get('new_category')

        if new_category_name:
            # get_or_create prevents creating duplicates
            new_cat, created = Category.objects.get_or_create(name=new_category_name)
            # Set the form's category to this new one
            cleaned_data['category'] = new_cat
        elif not category:
            raise forms.ValidationError(
                "You must either select an existing category or create a new one."
            )
        
        return cleaned_data