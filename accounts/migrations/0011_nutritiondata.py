# Generated by Django 5.1.7 on 2025-03-19 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_dailymeal_delete_meal'),
    ]

    operations = [
        migrations.CreateModel(
            name='NutritionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.TextField()),
                ('calories', models.FloatField()),
                ('protein', models.FloatField()),
                ('carbs', models.FloatField()),
                ('fat', models.FloatField()),
            ],
            options={
                'db_table': 'nutrition_data',
            },
        ),
    ]
