from django.shortcuts import render
from complaint.models import Complaint, cat


def wall(request):
    category = request.GET.get("category")
    print('category :')
    print(category)
    print('category :')
    if category is not None:
        complaints = Complaint.objects.all().filter(sub_cat=category).filter(sub_cat=category)
        return render(request, 'support_system/home_single.html', {'complaints': complaints, 'category': category} )
    cats = cat.objects.all()
    complaint = []
    for c in cats:
        if Complaint.objects.filter(sub_cat=c.name).exists():
            complaint.append([c.name, Complaint.objects.all().filter(sub_cat=c.name)[:]])
    return render(request, 'support_system/home.html', {'compiles': complaint})
