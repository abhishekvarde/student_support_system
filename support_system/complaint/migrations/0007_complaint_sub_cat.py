# Generated by Django 3.0 on 2019-12-25 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0006_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='sub_cat',
            field=models.CharField(default='other', max_length=30),
        ),
    ]