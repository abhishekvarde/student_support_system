from django.contrib.auth import logout
from django.shortcuts import render, redirect
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
    userdata = []
    if request.user.is_authenticated:
        if student.objects.filter(user=request.user).exists():
            userdata = student.objects.get(user=request.user)
        else:
            return redirect('/login')
    else:
        return redirect('/login')
    if category is not None:
        complaints = Complaint.objects.all().filter(sub_cat=category)
        return render(request, 'support_system/home_single.html', {'complaints': complaints})
    cats = cat.objects.all()
    # if request.user.is_authenticated:
    #     like_obj = student.objects.get(user=request.user)
    #     liked_post = like_obj.liked_complaint
    #     liked_post = liked_post.split(",")
    for c in cats:
        if Complaint.objects.filter(sub_cat=c.name).exists():
            complaint_objs = Complaint.objects.filter(sub_cat=c.name)
            qset = append_likes(request, complaint_objs)
            complaint.append([c.name, qset[:10]])
            print(complaint)
            print("----------------------------------------------------------")
    return render(request, 'support_system/home.html', {'complaints': complaint, 'userdata': userdata})


def append_likes(request, complaint_objs):
    qset = []
    if request.user.is_authenticated:
        like_obj = student.objects.get(user=request.user)
        liked_post = like_obj.liked_complaint
        liked_post = liked_post.split(",")
        for i in complaint_objs:
            if str(i.id) in liked_post:
                qset.append([i, '1'])  # for every liked post
            else:
                qset.append([i, '0'])
        print(qset)
    else:
        for i in complaint_objs:
            qset.append([i, '0'])
    return qset


def registeration(request):
    logout(request)
    return render(request, 'support_system/registration_form.html')


def login(request):
    logout(request)
    return render(request, 'support_system/login.html')
