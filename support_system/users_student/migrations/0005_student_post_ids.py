# Generated by Django 3.0 on 2019-12-25 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_student', '0004_auto_20191225_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='post_ids',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
