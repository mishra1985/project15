from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    pass

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "The new passwords do not match")
        return cleaned_data

# accounts/forms.py
from django import forms

class OnboardingForm(forms.Form):
    name = forms.CharField(max_length=100)
    goal = forms.ChoiceField(choices=[
        ('Weight Loss', 'Weight Loss'),
        ('Weight Gain', 'Weight Gain'),
        ('Maintain Weight', 'Maintain Weight'),
        ('Build Muscle', 'Build Muscle'),
        ('Improve Health', 'Improve Health'),
    ])
    diet = forms.ChoiceField(choices=[
        ('No Restrictions', 'No Restrictions'),
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan'),
        ('Paleo', 'Paleo'),
        ('Keto', 'Keto'),
        ('Mediterranean', 'Mediterranean'),
        ('Gluten-Free', 'Gluten-Free'),
    ])
    age = forms.IntegerField(min_value=18, max_value=100)
    gender = forms.ChoiceField(choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-binary', 'Non-binary'),
        ('Prefer not to say', 'Prefer not to say'),
    ])
    height = forms.FloatField(min_value=100, max_value=250)
    weight = forms.FloatField(min_value=30, max_value=300)
    activity = forms.ChoiceField(choices=[
        ('Sedentary', 'Sedentary (little or no exercise)'),
        ('Light', 'Light (exercise 1-3 days/week)'),
        ('Moderate', 'Moderate (exercise 3-5 days/week)'),
        ('Active', 'Active (exercise 6-7 days/week)'),
        ('Very Active', 'Very Active (hard exercise daily)'),
    ])
    # Using a MultipleChoiceField for checkboxes; Django will collect these as a list.
    allergies = forms.MultipleChoiceField(
        choices=[
            ('Dairy', 'Dairy'),
            ('Eggs', 'Eggs'),
            ('Nuts', 'Nuts'),
            ('Gluten', 'Gluten'),
            ('Soy', 'Soy'),
            ('Shellfish', 'Shellfish'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    avoid = forms.CharField(max_length=255, required=False)
    meals = forms.ChoiceField(choices=[
        ('3', '3 meals per day'),
        ('4', '4 meals per day'),
        ('5', '5 meals per day'),
        ('6', '6 meals per day'),
    ])

# accounts/forms.py

from django import forms
from .models import ExtraData

# forms.py
from django import forms
from .models import ExtraData
# forms.py
from django import forms
from .models import ExtraData

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = ExtraData
        fields = [
            'name',
            'goal',
            'diet',
            'age',
            'gender',
            'height',
            'weight',
            'activity',
            'allergies',
            'avoid',
            'meals',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Name'
            }),
            'goal': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Goal'
            }),
            'diet': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Diet'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Age'
            }),
            'gender': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Gender'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Height (cm)'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Weight (kg)'
            }),
            'activity': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Activity'
            }),
            'allergies': forms.Textarea(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Allergies (comma separated, e.g. Nuts, Soy)',
                'rows': 2
            }),
            'avoid': forms.Textarea(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Foods to avoid',
                'rows': 2
            }),
            'meals': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-slate-700 text-white border border-slate-600',
                'placeholder': 'Meals per day'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make them not strictly required if your model allows blank=True
        for field in self.fields:
            self.fields[field].required = False

