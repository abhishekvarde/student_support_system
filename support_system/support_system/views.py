from django.shortcuts import render

from complaint.models import Complaint


def wall(request):
    compiles = Complaint.objects.get()
    return render(request, 'wall.html', {'compiles': compiles})
