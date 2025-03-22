import google.generativeai as genai
import re
from datetime import date
from accounts.models import DailyMeal
import os
# Configure the Gemini API with your API key
genai.configure(api_key=os.environ.get('GENERATIVE_AI_API_KEY'))

def ask_gemini(question):
    try:
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(question)
        if response and hasattr(response, 'text'):
            # Debug: print the raw response from Gemini
            print("Gemini raw response:", response.text)
            return response.text.strip()
        else:
            print("Gemini returned unexpected format.")
            return "Unexpected API response format."
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

def get_recommended_intakes(age, gender, height, weight, goal):
    """
    For a user with the provided age, gender, height, weight, and goal, ask Gemini
    to return recommended daily calories, protein, carbs, and fat in grams.
    Expect Gemini to return 4 numbers separated by commas.
    """
    question = (
        f"For a {age}-year-old {gender} with height {height} cm and weight {weight} kg "
        f"who wants to {goal}, how many daily calories, protein, carbs, and fats are needed? "
        "Just provide 4 numbers separated by commas (calories, protein, carbs, fat)."
    )
    response_text = ask_gemini(question)
    # Debug: print the response for recommended intakes
    print("Gemini response for recommended intakes:", response_text)
    if not response_text:
        return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    numbers = re.findall(r"(\d+\.?\d*)", response_text)
    if len(numbers) >= 4:
        return {
            "calories": float(numbers[0]),
            "protein": float(numbers[1]),
            "carbs": float(numbers[2]),
            "fat": float(numbers[3]),
        }
    else:
        print("Unexpected format from Gemini:", response_text)
        return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

# You may also have additional functions for processing daily meals
def process_daily_meals(user):
    """
    Process today's DailyMeal(s) for the given user:
      - Retrieve today's meals.
      - For each meal section (breakfast, lunch, snack, dinner), split the food items.
      - For each food item, call get_food_nutrition to get its macros.
      - Sum up all nutritional values and update the DailyMeal records in bulk.
    """
    total_cal = 0
    total_prot = 0
    total_carb = 0
    total_fat = 0

    meals = DailyMeal.objects.filter(user=user, date=date.today())
    meal_sections = ["breakfast", "lunch", "snack", "dinner"]

    for meal in meals:
        for section in meal_sections:
            food_data = getattr(meal, section, None)
            if food_data:
                food_items = [item.strip() for item in food_data.split(",") if item.strip()]
                for item in food_items:
                    nutrition = get_food_nutrition(item)
                    total_cal  += nutrition.get("calories", 0)
                    total_prot += nutrition.get("protein", 0)
                    total_carb += nutrition.get("carbs", 0)
                    total_fat  += nutrition.get("fat", 0)

    meals.update(
        calintake=total_cal,
        prtointake=total_prot,
        carbintake=total_carb,
        fatintake=total_fat
    )

    return total_cal, total_prot, total_carb, total_fat

def get_food_nutrition(food_item):
    """
    Use the Gemini API to retrieve nutritional information for a given food item.
    The query should be tailored so that Gemini returns 4 numbers representing the
    number of calories, protein (g), carbs (g), and fat (g) separated by commas.
    """
    query = f"Provide the nutritional values in calories, protein (g), carbs (g), and fat (g) for {food_item}. Just return 4 numbers separated by commas."
    response_text = ask_gemini(query)
    # Debug: print Gemini response for this food item
    print(f"Gemini response for '{food_item}':", response_text)
    if not response_text:
        return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    numbers = re.findall(r"(\d+\.?\d*)", response_text)
    if len(numbers) >= 4:
        return {
            "calories": float(numbers[0]),
            "protein": float(numbers[1]),
            "carbs": float(numbers[2]),
            "fat": float(numbers[3]),
        }
    else:
        print("Unexpected Gemini response for food item:", food_item, response_text)
        return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
