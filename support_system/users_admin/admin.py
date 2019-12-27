from django.contrib import admin

# Register your models here.
from .models import CommitteeMember

admin.site.register(CommitteeMember)