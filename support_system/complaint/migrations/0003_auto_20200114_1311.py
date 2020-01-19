# Generated by Django 3.0.1 on 2020-01-14 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_student', '0015_auto_20200113_2129'),
        ('complaint', '0002_auto_20200114_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='student_id',
        ),
        migrations.AddField(
            model_name='complaint',
            name='student',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='users_student.student'),
            preserve_default=False,
        ),
    ]