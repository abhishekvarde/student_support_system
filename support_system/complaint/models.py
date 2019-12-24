from django.db import models
from django.contrib.auth.models import User


class Complaint(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    solved = models.BooleanField(default=False)
    satisfied = models.BooleanField(default=False)
    status = models.CharField(max_length=20)
    tags = models.CharField(max_length=200)
    image = models.ImageField(upload_to="complaint_image/")

    def __str__(self):
        return self.title
