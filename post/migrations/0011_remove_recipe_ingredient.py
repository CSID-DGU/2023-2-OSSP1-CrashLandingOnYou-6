# Generated by Django 4.0.5 on 2023-12-18 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_rename_author_recipe_author_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredient',
        ),
    ]
