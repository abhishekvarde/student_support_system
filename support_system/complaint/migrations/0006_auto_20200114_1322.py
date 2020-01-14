# Generated by Django 3.0.1 on 2020-01-14 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_student', '0015_auto_20200113_2129'),
        ('complaint', '0005_auto_20200114_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='cats',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='complaint.cat'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='complaint',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users_student.student'),
        ),
    ]
