# Generated by Django 3.0.1 on 2019-12-28 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(default='', max_length=10)),
                ('otp_phone_no', models.CharField(default='', max_length=6)),
                ('email', models.CharField(default='', max_length=100)),
                ('otp_email', models.CharField(default='', max_length=6)),
            ],
        ),
    ]
