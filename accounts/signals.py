# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import DailyMeal
from accounts.nutrition import process_daily_meals

@receiver(post_save, sender=DailyMeal)
def update_nutrition_totals(sender, instance, created, **kwargs):
    # Temporarily disconnect this signal
    post_save.disconnect(update_nutrition_totals, sender=DailyMeal)
    try:
        process_daily_meals(instance.user)
    finally:
        # Reconnect the signal
        post_save.connect(update_nutrition_totals, sender=DailyMeal)
