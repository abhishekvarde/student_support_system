# Generated by Django 3.0.1 on 2020-01-11 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0009_complaint_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='solution',
            field=models.TextField(default='', max_length=300),
        ),
    ]
