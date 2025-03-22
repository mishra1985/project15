# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import (
    RegistrationForm, 
    LoginForm, 
    ForgotPasswordForm, 
    OnboardingForm, 
    UserSettingsForm
)
from .models import ExtraData, DailyMeal

# Import the Gemini API helper that calculates recommended macros.
from .nutrition import get_recommended_intakes

# --- Triple Forms (login, register, forgot password) ---
def triple_forms_view(request):
    login_form = LoginForm()
    reg_form = RegistrationForm()
    forgot_form = ForgotPasswordForm()
    return render(request, 'accounts/tripleforms.html', {
        'login_form': login_form,
        'reg_form': reg_form,
        'forgot_form': forgot_form,
    })

def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            reg_form = RegistrationForm()
            forgot_form = ForgotPasswordForm()
            return render(request, 'accounts/tripleforms.html', {
                'login_form': login_form,
                'reg_form': reg_form,
                'forgot_form': forgot_form,
            })
    return redirect('triple_forms')

def register_view(request):
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            print(f"User {user.username} created successfully.")
            login(request, user)
            if request.user.is_authenticated:
                print(f"User {request.user.username} is now logged in.")
            else:
                print("Login failed after registration.")
            return redirect('extra_data')
        else:
            print("Registration form errors:", reg_form.errors)
            login_form = LoginForm()
            forgot_form = ForgotPasswordForm()
            return render(request, 'accounts/tripleforms.html', {
                'login_form': login_form,
                'reg_form': reg_form,
                'forgot_form': forgot_form,
            })
    return redirect('triple_forms')

def forgot_password_view(request):
    if request.method == 'POST':
        forgot_form = ForgotPasswordForm(request.POST)
        if forgot_form.is_valid():
            username = forgot_form.cleaned_data['username']
            email = forgot_form.cleaned_data['email']
            new_password = forgot_form.cleaned_data['new_password1']
            try:
                user = User.objects.get(username=username, email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated successfully. Please log in with your new password.")
                return redirect('login')
            except User.DoesNotExist:
                forgot_form.add_error(None, "No user found with the provided username and email.")
    else:
        forgot_form = ForgotPasswordForm()
    login_form = LoginForm()
    reg_form = RegistrationForm()
    return render(request, 'accounts/tripleforms.html', {
         'login_form': login_form,
         'reg_form': reg_form,
         'forgot_form': forgot_form,
    })

# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ExtraData
from .forms import OnboardingForm, UserSettingsForm
from .nutrition import get_recommended_intakes

# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ExtraData
from .forms import OnboardingForm
from .nutrition import get_recommended_intakes

@login_required
def extra_data_view(request):
    # If ExtraData already exists, redirect to dashboard.
    if hasattr(request.user, 'userextradata'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = OnboardingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            extra_data = ExtraData.objects.create(
                user=request.user,
                name=data['name'],
                goal=data['goal'],
                diet=data['diet'],
                age=data['age'],
                gender=data['gender'],
                height=data['height'],
                weight=data['weight'],
                activity=data['activity'],
                allergies=",".join(data['allergies']),
                avoid=data['avoid'],
                meals=data['meals'],
            )
            # Call Gemini API to get recommended nutritional values
            recommended = get_recommended_intakes(
                age=extra_data.age,
                gender=extra_data.gender,
                height=extra_data.height,
                weight=extra_data.weight,
                goal=extra_data.goal,
            )
            print("Gemini recommended:", recommended)  # Debug print
            extra_data.recommended_calories = recommended.get("calories", 0)
            extra_data.recommended_protein = recommended.get("protein", 0)
            extra_data.recommended_carbs = recommended.get("carbs", 0)
            extra_data.recommended_fat = recommended.get("fat", 0)
            extra_data.save()
            return redirect('dashboard')
    else:
        form = OnboardingForm()
    return render(request, 'accounts/extra_data_form.html', {'form': form})

    return render(request, 'accounts/extra_data_form.html', {'form': form})

'''
# --- Onboarding / Extra Data ---
def extra_data_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # If the user has already provided extra data, redirect to dashboard.
    if hasattr(request.user, 'userextradata'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = OnboardingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            extra_data = ExtraData.objects.create(
                user=request.user,
                name=data['name'],
                goal=data['goal'],
                diet=data['diet'],
                age=data['age'],
                gender=data['gender'],
                height=data['height'],
                weight=data['weight'],
                activity=data['activity'],
                allergies=",".join(data['allergies']),
                avoid=data['avoid'],
                meals=data['meals'],
            )
            # Get recommended nutrition values from Gemini API using the user's data.
            recommended = get_recommended_intakes(
                age=extra_data.age,
                gender=extra_data.gender,
                height=extra_data.height,
                weight=extra_data.weight,
                goal=extra_data.goal,
            )
            extra_data.recommended_calories = recommended['calories']
            extra_data.recommended_protein = recommended['protein']
            extra_data.recommended_carbs = recommended['carbs']
            extra_data.recommended_fat = recommended['fat']
            extra_data.save()
            return redirect('dashboard')
    else:
        form = OnboardingForm()
    
    return render(request, 'accounts/extra_data_form.html', {'form': form})
'''

# --- Dashboard & User Settings ---
@login_required
def dashboard_view(request):
    # Get or create the user's extra data
    try:
        user_extra_data = request.user.userextradata
    except ExtraData.DoesNotExist:
        user_extra_data = ExtraData.objects.create(user=request.user)
    
    today = timezone.now().date()
    try:
        daily_meal = DailyMeal.objects.get(user=request.user, date=today)
    except DailyMeal.DoesNotExist:
        daily_meal = None

    # Calculate actual consumed macros from DailyMeal (if available)
    if daily_meal:
        consumed_cal = daily_meal.calintake
        consumed_pro = daily_meal.prtointake
        consumed_carbs = daily_meal.carbintake
        consumed_fat = daily_meal.fatintake
    else:
        consumed_cal = consumed_pro = consumed_carbs = consumed_fat = 0

    # Recommended values from ExtraData (set during onboarding/profile update)
    recommended_cal = user_extra_data.recommended_calories
    recommended_pro = user_extra_data.recommended_protein
    recommended_carbs = user_extra_data.recommended_carbs
    recommended_fat = user_extra_data.recommended_fat

    # Calculate percentages for display (avoiding division by zero)
    cal_percent = (consumed_cal / recommended_cal * 100) if recommended_cal else 0
    pro_percent = (consumed_pro / recommended_pro * 100) if recommended_pro else 0
    carbs_percent = (consumed_carbs / recommended_carbs * 100) if recommended_carbs else 0
    fat_percent = (consumed_fat / recommended_fat * 100) if recommended_fat else 0

    form = UserSettingsForm(instance=user_extra_data)
    context = {
        'form': form,
        'daily_meal': daily_meal,
        'user_extra_data': user_extra_data,
        'consumed_cal': consumed_cal,
        'consumed_pro': consumed_pro,
        'consumed_carbs': consumed_carbs,
        'consumed_fat': consumed_fat,
        'recommended_cal': recommended_cal,
        'recommended_pro': recommended_pro,
        'recommended_carbs': recommended_carbs,
        'recommended_fat': recommended_fat,
        'cal_percent': cal_percent,
        'pro_percent': pro_percent,
        'carbs_percent': carbs_percent,
        'fat_percent': fat_percent,
    }
    return render(request, 'accounts/dashboard.html', context)



def update_settings(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        user_extra_data = request.user.userextradata
    except ExtraData.DoesNotExist:
        user_extra_data = ExtraData.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_extra_data)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(request, 'accounts/dashboard.html', {'form': form})
    else:
        return redirect('dashboard')

def logout_view(request):
    logout(request)
    return redirect('triple_forms')

def home_view(request):
    return render(request, 'accounts/tripleforms.html')

def barcode_scanner_view(request):
    return render(request, 'accounts/barcode_scanner.html')

def chat_view(request):
    return render(request, 'accounts/chat.html')

# --- Meal Logging ---
@login_required
def log_meal_view(request):
    today = timezone.now().date()
    daily_meal, created = DailyMeal.objects.get_or_create(user=request.user, date=today)

    if request.method == 'POST':
        meal_type = request.POST.get('meal_type', '').lower()  # expecting 'breakfast', 'lunch', etc.
        food_items = request.POST.get('food_items', '').strip()
        
        if meal_type not in ['breakfast', 'lunch', 'snack', 'dinner']:
            messages.error(request, "Invalid meal type.")
            return redirect('dashboard')
        
        # Check if this meal has already been logged.
        if getattr(daily_meal, meal_type):
            messages.error(request, f"{meal_type.capitalize()} has already been logged for today.")
        else:
            setattr(daily_meal, meal_type, food_items)
            daily_meal.save()
            messages.success(request, f"{meal_type.capitalize()} logged successfully.")
        
        return redirect('dashboard')
    else:
        return redirect('dashboard')
    

# accounts/views.py
from .nutrition import get_recommended_intakes
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ExtraData
from .forms import UserSettingsForm
from .nutrition import get_recommended_intakes
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ExtraData
from .forms import UserSettingsForm
from .nutrition import get_recommended_intakes

@login_required
def update_profile(request):
    try:
        profile = request.user.userextradata
    except ExtraData.DoesNotExist:
        profile = ExtraData.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()  # Saves any changes to age, gender, etc.
            # Now update recommended values using Gemini
            recommended = get_recommended_intakes(
                age=profile.age,
                gender=profile.gender,
                height=profile.height,
                weight=profile.weight,
                goal=profile.goal,
            )
            print("Gemini recommended:", recommended)  # Debug print (remove in production)
            profile.recommended_calories = recommended.get("calories", 0)
            profile.recommended_protein = recommended.get("protein", 0)
            profile.recommended_carbs = recommended.get("carbs", 0)
            profile.recommended_fat = recommended.get("fat", 0)
            profile.save()
            return redirect('dashboard')
    else:
        form = UserSettingsForm(instance=profile)
    
    return render(request, 'accounts/update_profile.html', {'form': form})


from django.shortcuts import render

def chat_view(request):
    return render(request, 'accounts/chat.html')
