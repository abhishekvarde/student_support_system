from django.db import models
from django.contrib.auth.models import User
from users_student.models import student


# from complaint.models import cat


class Complaint(models.Model):
    student = models.OneToOneField(student, on_delete=models.CASCADE, default=None)
    url = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    liked = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    # solved = models.BooleanField(default=False)
    level = models.CharField(max_length=20, default="department")
    satisfied = models.BooleanField(default=False)
    sub_cat = models.CharField(max_length=30, default="other")
    status = models.CharField(max_length=20, default="pending")  # pending, ongoing, solved, rejected
    tags = models.CharField(max_length=200)
    approved_tags = models.CharField(max_length=200, default="")
    image = models.ImageField(upload_to="complaint_image/")
    solution = models.TextField(max_length=300, default="")

    def __str__(self):
        return self.title


class cat(models.Model):
    name = models.CharField(max_length=20)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.name
