# Generated by Django 4.2.6 on 2023-12-17 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_recipe_classification_recipe_n_main_ingredients_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredient',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
