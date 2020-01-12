from django.contrib import admin

# Register your models here.
from .models import CommitteeMember, Otp

admin.site.register(CommitteeMember)
admin.site.register(Otp)