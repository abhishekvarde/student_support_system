from django.http import HttpResponse
from django.shortcuts import render
from complaint.models import Complaint, cat
from users_student.models import student
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import JsonResponse


def post(request):
    return render(request, 'complaint/post.html')


# dont call this function.

def like(request):
    if request.user.is_authenticated:
        post_id = request.GET.get('post_id')
        print("-----------------------------------------")
        print(post_id)
        data = {
            "success": 'False'
        }
        if Complaint.objects.filter(id=int(post_id)).exists():
            user_obj = student.objects.get(user=request.user)
            liked_post = user_obj.liked_complaint
            liked_list = liked_post.split(",")
            if "" in liked_list:
                liked_list.remove("")
            if post_id not in liked_list:
                compile_obj = Complaint.objects.get(id=post_id)
                compile_obj.liked += 1
                compile_obj.save()
                liked_list.append(post_id)
                liked_post = ",".join(liked_list)
                user_obj.liked_complaint = liked_post
                user_obj.save()
                response = 'True'
                print("At the end")
                data = {
                    "success": 'True'
                }
            else:
                print("--------------------------------sending false")
                data = {
                    "success": 'False'
                }
        return JsonResponse(data)


def dislike(request):
    if request.user.is_authenticated:
        post_id = request.GET.get('post_id')
        print("-----------------------------------------")
        print(post_id)
        data = {
            "success": 'False'
        }
        if Complaint.objects.filter(id=int(post_id)).exists():
            user_obj = student.objects.get(user=request.user)
            liked_post = user_obj.liked_complaint
            liked_list = liked_post.split(",")
            if "" in liked_list:
                liked_list.remove("")
            if post_id in liked_list:
                compile_obj = Complaint.objects.get(id=post_id)
                compile_obj.liked -= 1
                compile_obj.save()
                liked_list.remove(post_id)
                liked_post = ",".join(liked_list)
                user_obj.liked_complaint = liked_post
                user_obj.save()
                print("At the end")
                data = {
                    "success": 'True'
                }
            else:
                print("--------------------------------sending false")
                data = {
                    "success": 'False'
                }
        return JsonResponse(data)


def post(request):
    if not request.user.is_authenticated:
        return redirect('/users_student/login/')

    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        print(user.username)
        title = request.POST.get('title')
        des = request.POST.get('description')
        tags = request.POST.get('tags')
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        url = fs.url(filename)
        print(user.username)
        print(url)
        student_img = student.objects.filter(user=request.user)
        complain = Complaint(user=user, title=title, description=des, tags=tags, image=url,
                             url=student_img[0].profile_picture)
        complain.save()
        student_obj = student.objects.get(user=user)
        ids = student_obj.post_ids
        ids = ids.split(",")
        ids.append(str(complain.id))
        if "" in ids:
            ids.remove("")
        student_obj.post_ids = ",".join(ids)
        student_obj.save()
        return redirect("/users_student/profile/")
    else:
        level = request.GET.get('level')
        student_img = student.objects.filter(user=request.user)
        # print(student_img)
        print("---------------------------------------------------------------------")
        print(student_img[0].profile_picture)
        for i in student_img:
            print(i.profile_picture)
        if level is None or level == "":
            level = "department"
        userdata = student.objects.get(user=request.user)
        print (userdata)
        return render(request, 'complaint/add_complaint.html', {'level': level, 'userdata': userdata})


# def display(request):


# tracker is used to track post and shown in different page which is to be designed

def tracker(request):
    userdata = []
    post_id = request.GET.get('track_id')
    if post_id is not None:
        if post_id != "":
            complaints = Complaint.objects.filter(id=post_id)
            if request.user.is_authenticated:
                userdata = student.objects.get(user=request.user)
            return render(request, 'support_system/home_single.html', {'complaints': complaints, 'userdata': userdata})
        return redirect("/")
    return redirect("/")
