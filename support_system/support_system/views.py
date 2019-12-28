from django.shortcuts import render
from complaint.models import Complaint, cat
from users_student.models import student


def wall(request):
    category = request.GET.get("category")
    print('category :')
    print(category)
    print('category :')
    qset = []
    liked_post = []
    complaint = []
    if category is not None:
        complaints = Complaint.objects.all().filter(sub_cat=category)
        return render(request, 'support_system/home_single.html', {'complaints': complaints, 'category': category})
    cats = cat.objects.all()
    if request.user.is_authenticated:
        like_obj = student.objects.get(user=request.user)
        liked_post = like_obj.liked_complaint
        liked_post = liked_post.split(",")
    for c in cats:
        if Complaint.objects.filter(sub_cat=c.name).exists():
            complaint_objs = Complaint.objects.filter(sub_cat=c.name)
            for i in complaint_objs:
                print("checking:")
                print(i.id)
                print(liked_post)
                print("-----------")
                if str(i.id) in liked_post:
                    qset.append([i, '1'])  # for every liked post
                else:
                    qset.append([i, '0'])
            complaint.append([c.name, qset[:]])
            print(complaint)
            print("----------------------------------------------------------")
    return render(request, 'support_system/home.html', {'complaints': complaint})
