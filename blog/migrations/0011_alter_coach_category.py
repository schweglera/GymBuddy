# Generated by Django 5.1.2 on 2025-01-25 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_coach_category_alter_coach_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='category',
            field=models.CharField(max_length=50),
        ),
    ]
