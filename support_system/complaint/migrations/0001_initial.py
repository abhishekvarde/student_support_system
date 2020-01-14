# Generated by Django 3.0.1 on 2020-01-14 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users_student', '0015_auto_20200113_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='cat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('total', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
                ('liked', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('level', models.CharField(default='department', max_length=20)),
                ('satisfied', models.BooleanField(default=False)),
                ('sub_cat', models.CharField(default='other', max_length=30)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('tags', models.CharField(max_length=200)),
                ('approved_tags', models.CharField(default='', max_length=200)),
                ('image', models.ImageField(upload_to='complaint_image/')),
                ('solution', models.TextField(default='', max_length=300)),
                ('student', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='users_student.student')),
            ],
        ),
    ]
