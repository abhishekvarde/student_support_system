from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class student(models.Model):
    user = models.OneToOneField(User,models.CASCADE)
    college_id = models.CharField(max_length=100, default="")
    year = models.CharField(max_length=20, default=0)
    college_name = models.CharField(max_length=100, default="")
    phone_no = models.CharField(max_length=10, default="")
    liked_complaint = models.CharField(max_length=1000, default="")




