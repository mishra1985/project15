# Generated by Django 5.1.7 on 2025-03-19 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_extradata_activity_alter_extradata_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='food_items',
            field=models.TextField(),
        ),
    ]
