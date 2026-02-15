# forms.py (place this in same directory as views.py)
from django import forms
from django.core.validators import RegexValidator

class UserRegistrationForm(forms.Form):
    """
    Note: This form is not currently used in the signup flow.
    User registration is handled via AJAX in signup.html with first_name, last_name, and age fields.
    Face embeddings are stored in MongoDB (face_services.py)
    """
    first_name = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s\'-]+$',
                message='First name can only contain letters, spaces, hyphens, and apostrophes'
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your first name',
            'class': 'form-input',
            'autocomplete': 'name'
        })
    )
    
    last_name = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s\'-]+$',
                message='Last name can only contain letters, spaces, hyphens, and apostrophes'
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your last name',
            'class': 'form-input',
            'autocomplete': 'name'
        })
    )
   
