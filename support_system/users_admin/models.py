from django.contrib.auth.models import User
from django.db import models


class CommitteeMember(models.Model):
    user = models.OneToOneField(User,models.CASCADE)
    #college_id = models.CharField(max_length=100, default="")
    #year = models.CharField(max_length=20, default=0)
    committee = models.CharField(max_length=100, default="")
    teacher_id = models.CharField(max_length=100, default="")
    college = models.CharField(max_length=100,default="")
    is_approved = models.BooleanField(default="False")
    phone_no = models.CharField(max_length=10, default="")
    pending_request = models.CharField(max_length=1000,default="")

