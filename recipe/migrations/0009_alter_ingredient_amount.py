# Generated by Django 4.0.5 on 2022-06-07 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0008_alter_recipe_author_alter_recipe_cook_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]
