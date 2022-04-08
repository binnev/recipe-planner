# Generated by Django 4.0.3 on 2022-04-08 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_alter_recipe_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='preparation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
