# Generated by Django 5.2.2 on 2025-06-21 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_review_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
    ]
