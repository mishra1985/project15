# Generated by Django 5.1.7 on 2025-03-19 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_delete_nutritiondata_remove_dailymeal_calintake_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailymeal',
            name='calintake',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='dailymeal',
            name='carbintake',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='dailymeal',
            name='fatintake',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='dailymeal',
            name='prtointake',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='extradata',
            name='recommended_calories',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='extradata',
            name='recommended_carbs',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='extradata',
            name='recommended_fat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='extradata',
            name='recommended_protein',
            field=models.FloatField(default=0),
        ),
    ]
