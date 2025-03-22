from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

class ExtraData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userextradata')
    name = models.CharField(max_length=100, default='', blank=True)
    goal = models.CharField(max_length=50, default='Maintain Weight', blank=True)
    diet = models.CharField(max_length=50, default='No Restrictions', blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=20, default='Prefer not to say', blank=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    activity = models.CharField(max_length=50, default='Sedentary', blank=True)
    allergies = models.CharField(max_length=255, blank=True, default='')
    avoid = models.CharField(max_length=255, blank=True, default='')
    meals = models.CharField(max_length=10, default='3', blank=True)
    
    # Fields to store recommended nutritional values from Gemini API
    recommended_calories = models.FloatField(default=0)
    recommended_protein = models.FloatField(default=0)
    recommended_carbs = models.FloatField(default=0)
    recommended_fat = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username}'s extra data"

'''
class ExtraData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userextradata')
    name = models.CharField(max_length=100, default='', blank=True)
    goal = models.CharField(max_length=50, default='Maintain Weight', blank=True)
    diet = models.CharField(max_length=50, default='No Restrictions', blank=True)
    age = models.IntegerField(blank=True, null=True)   # allow null if you want to skip
    gender = models.CharField(max_length=20, default='Prefer not to say', blank=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    activity = models.CharField(max_length=50, default='Sedentary', blank=True)
    allergies = models.CharField(max_length=255, blank=True, default='')
    avoid = models.CharField(max_length=255, blank=True, default='')
    meals = models.CharField(max_length=10, default='3', blank=True)
    
    # Fields to store recommended nutritional values calculated by Gemini API
    recommended_calories = models.FloatField(default=0)
    recommended_protein = models.FloatField(default=0)
    recommended_carbs = models.FloatField(default=0)
    recommended_fat = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username}'s extra data"
'''


class DailyMeal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    breakfast = models.TextField(blank=True, null=True)
    lunch = models.TextField(blank=True, null=True)
    snack = models.TextField(blank=True, null=True)
    dinner = models.TextField(blank=True, null=True)
    
    # These fields will store the actual nutritional intake for the day,
    # computed from the food items using the Gemini API.
    calintake = models.FloatField(default=0)
    prtointake = models.FloatField(default=0)
    carbintake = models.FloatField(default=0)
    fatintake = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'date')  # ensures one record per user per day

    def __str__(self):
        return f"{self.user.username} - {self.date}"


from django.db import models

class ChatMessage(models.Model):
    # You can add a conversation field if you wish to support multiple conversation threads.
    username = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # Time taken (in seconds) for Gemini's reply (optional – only set for Gemini messages)
    time_taken = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} @ {self.timestamp:%Y-%m-%d %H:%M:%S}: {self.message[:50]}"


