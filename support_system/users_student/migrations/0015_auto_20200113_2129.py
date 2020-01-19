# Generated by Django 2.2.5 on 2020-01-13 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_student', '0014_student_requested_approved_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='dob',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(default='', max_length=20),
        ),
    ]