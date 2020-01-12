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
        # print(user.username)
        title = request.POST.get('title')
        des = request.POST.get('description')
        tags = request.POST.get('all_emails')
        print(tags)
        list_tags = tags.split(",")
        # for tag in list_tags:
        #     if User.objects.filter(email=tag).exists():
        #         temp_obj
        # image = request.FILES['image']
        # fs = FileSystemStorage()
        # filename = fs.save(image.name, image)
        # url = fs.url(filename)
        # print(user.username)
        # print(url)
        student_img = student.objects.filter(user=request.user)
        complain = Complaint(user=user, title=title, description=des, tags=tags,  # image=url,
                             url=student_img[0].profile_picture)
        complain.save()
        list_tags = tags.split(",")
        if "" in list_tags:
            list_tags.remove("")
        for tag in list_tags:
            if User.objects.filter(email=tag).exists():
                temp_user =  User.objects.get(email=tag)
                if student.objects.filter(user=temp_user).exists():
                    temp_obj = student.objects.get(user=temp_user)
                    print('===start===')
                    print(temp_obj)
                    print('===end===')
                    all_user_tags =  temp_obj.requested_tag
                    all_user_tags = all_user_tags.split(",")
                    all_user_tags.append(str(complain.id))
                    temp_obj.requested_tag = ",".join(all_user_tags)
                    temp_obj.save()
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
        print(userdata)
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


def allow(request):
    if request.user.is_authenticated:
        print("kam karne aaya")
        id = request.GET.get('id')
        allow = request.GET.get('allow')
        if student.objects.filter(user=request.user).exists:
            temp_student = student.objects.get(user=request.user)
            requested_tag = temp_student.requested_tag
            requested_approved_tag = temp_student.requested_approved_tag
            requested_tag = requested_tag.split(",")
            requested_approved_tag = requested_approved_tag.split(",")
            if "" in requested_tag:
                requested_tag.remove("")
            if id in requested_tag:
                print(requested_tag)
                requested_tag.remove(id)
                print(requested_tag)
                if "" in requested_tag:
                    requested_tag.remove("")
                temp_student.requested_tag = ",".join(requested_tag)
                temp_student.save()
                if Complaint.objects.filter(id=id).exists():
                    temp_comp = Complaint.objects.get(id=id)
                    pending = temp_comp.tags
                    approved = temp_comp.approved_tags
                    pending = pending.split(",")
                    approved = approved.split(",")
                    if request.user.email in pending:
                        pending.remove(request.user.email)
                        if request.user.email not in approved and allow == "1":
                            print("trying to add " + id)
                            print("trying to add " + id)
                            approved.append(request.user.email)
                            if id not in requested_approved_tag:
                                requested_approved_tag.append(id)
                                if "" in requested_approved_tag:
                                    requested_approved_tag.remove("")
                                temp_student.requested_approved_tag = ",".join(requested_approved_tag)
                                print("----------------")
                                print(requested_approved_tag)
                                temp_student.save()
                                print("Mil gai success.")
                    temp_comp.tags = ",".join(pending)
                    temp_comp.approved_tags = ",".join(approved)
                    temp_comp.save()
    return redirect('/users_student/profile?requesteddata=requested_tag')
#  http://127.0.0.1:8000/users_student/profile/?username=abhishek.varde@gmail.com&requesteddata=requested_tag