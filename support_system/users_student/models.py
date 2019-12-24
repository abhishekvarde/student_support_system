from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class student(models.Model):
    user = models.OneToOneField(User,models.CASCADE)
    college_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    year = models.CharField(max_length=20)
    college_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10)




