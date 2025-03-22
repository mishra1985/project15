from django.core.management.base import BaseCommand
import pdfplumber
import pandas as pd
from accounts.models import NutritionData

class Command(BaseCommand):
    help = "Import nutrition data from PDF into the nutrition_data table"

    def handle(self, *args, **kwargs):
        # Update this path to the actual location of your PDF file
        pdf_path = r"C:\Users\rithi\OneDrive\Documents\HTML Programs\projectdata\dinner_nutrition1.pdf"
        
        data = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    # Assuming the first row is the header
                    for row in table[1:]:
                        try:
                            data.append({
                                "item": row[0],
                                "calories": float(row[1]),
                                "protein": float(row[2]),
                                "carbs": float(row[3]),
                                "fat": float(row[4]),
                            })
                        except (ValueError, IndexError) as e:
                            self.stdout.write(f"Skipping row due to error: {e}")

        df = pd.DataFrame(data)
        
        # Optionally, if you want to avoid duplicates, use get_or_create
        for _, row in df.iterrows():
            obj, created = NutritionData.objects.get_or_create(
                item=row["item"],
                defaults={
                    "calories": row["calories"],
                    "protein": row["protein"],
                    "carbs": row["carbs"],
                    "fat": row["fat"]
                }
            )
            if created:
                self.stdout.write(f"Added {row['item']}")
            else:
                self.stdout.write(f"{row['item']} already exists")

        self.stdout.write("Data import completed!")
