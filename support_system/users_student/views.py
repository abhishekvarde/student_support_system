from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse
from complaint.models import Complaint
from support_system.views import append_likes
from .models import student
import os
from support_system.settings import BASE_DIR as project_path
from django.core.files.storage import FileSystemStorage


def validator(college_id, first_name, last_name, year, college_name, email, phone_no):
    error_code = "0000000"
    return error_code


def username_avaliable(request):
    username = request.GET.get('username', None)
    print(username)
    data = {
        "is_valid": User.objects.filter(email=username).exists()
    }
    return JsonResponse(data)


def register_student(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name_student')
        last_name = request.POST.get('last_name_student')
        college_id = request.POST.get('college_id_student')
        gender = request.POST.get('gender_student')
        dob = request.POST.get('dob_student')
        branch = request.POST.get('branch_student')
        college_name = request.POST.get('collage_student')
        email = request.POST.get('email_student')
        phone_no = request.POST.get('phone_no_student')
        address = request.POST.get('address_student')
        password = request.POST.get('password_student')
        cnf_password = request.POST.get('re_password_student')

        # request['email'] = email

        if not User.objects.filter(username=email).exists():
            user_obj = User.objects.create_user(username=email, password=password, email=email)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.save()

            user = authenticate(request, username=email, password=password)

            student_details = student(user=user, college_id=college_id, dob=dob, gender=gender,
                                      college_name=college_name,
                                      phone_no=phone_no, address=address)
            student_details.save()

        return redirect('/login')


def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('username_student')
        password = request.POST.get('password_student')

        print("--------------------")
        print(username)
        print(password)
        print("--------------------")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return redirect('/login')
    return redirect('/login')


def student_profile(request):
    if request.method == "GET":
        requested_data = request.GET.get('requesteddata')
        user_name = request.GET.get('user_name')
        print(requested_data)
        print(user_name)

        if user_name is None:
            user_name = request.user.username
        print(user_name)

        if request.user.is_authenticated and user_name == request.user.username:
            print("---------------------------utkarsh---------------------------------------")
            posts = []
            if not student.objects.filter(user=request.user):
                return redirect("/login")
            userdata = student.objects.get(user=request.user)

            if requested_data is None:
                requested_data = "all"

            if requested_data == "all":
                postsobj = Complaint.objects.filter(student=userdata)
                for post in postsobj:
                    posts.append(post)
            elif requested_data == "pending":
                posts = Complaint.objects.filter(student=userdata).filter(status="pending")
            elif requested_data == "ongoing":
                posts = Complaint.objects.filter(student=userdata).filter(status="ongoing")
            elif requested_data == "solved":
                posts = Complaint.objects.filter(student=userdata).filter(status="solved")
            elif requested_data == "approved_tags":
                appoved_ids = userdata.requested_approved_tag
                appoved_ids = appoved_ids.split(",")
                for a_i in appoved_ids:
                    if a_i is not "" and " ":
                        if Complaint.objects.filter(id=a_i).exists():
                            posts.append(Complaint.objects.filter(id=a_i)[0])
            elif requested_data == "requested_tag":
                # temp_user = request.user
                # if student.objects.filter(user=request.user):
                #     temp_student = student.objects.get(user=request.user)
                print('successful')
                print('successful')
                print('successful')
                print('successful')
                reqested_tags = userdata.requested_tag
                reqested_tags = reqested_tags.split(",")
                if "" in reqested_tags:
                    reqested_tags.remove("")
                for tag_ids in reqested_tags:
                    if Complaint.objects.filter(id=tag_ids).exists:
                        posts.append(Complaint.objects.filter(id=tag_ids)[0])
            elif requested_data == "upvoted":
                posts = []
                likedpostids = userdata.liked_complaint
                likedpostids = likedpostids.split(",")
                if "" in likedpostids:
                    likedpostids.remove("")
                for likedpostid in likedpostids:
                    if Complaint.objects.filter(id=likedpostid).exists():
                        posts.append((Complaint.objects.get(id=likedpostid)))
                    else:
                        likedpostids.remove(likedpostid)
            elif requested_data == "rejected":
                posts = Complaint.objects.filter(student=userdata).filter(status="rejected")
            print(posts)
            posts = append_likes(request, posts)
            return render(request, 'users_student/student_profile2.html',
                          {"usernmae": request.user.username, "userdata": userdata, "posts": posts,
                           'requesteddata': requested_data})
        else:
            if User.objects.filter(username=user_name).exists():
                user = User.objects.get(username=user_name)
                userdata = student.objects.get(user=user)
                posts = Complaint.objects.filter(student=userdata)
                return render(request, 'users_student/student_profile_another.html',
                              {"usernmae": request.user.username, "userdata": userdata, "posts": posts})
            print("user doesn't exists")
            return redirect('/users_student/login/')
    else:
        print("================================")
        print(request.user.username)
        postsobj = Complaint.objects.filter(user=request.user)
        posts = []
        userdata = student.objects.get(user=request.user)
        for post in postsobj:
            posts.append(post)
        print("================================140")

        return render(request, 'users_student/student_profile2.html',
                      {"usernmae": request.user.username, "posts": posts, "userdata": userdata})


def update_profile(request):
    print(request.user.username)
    if request.method == "GET":
        password = request.GET.get('password')
        studentdata = student.objects.get(user=request.user)

        print("---------" + password)

        user = authenticate(request, username=request.user.email, password=password)
        if user is None:
            data = {"is_updated": "False"}
            return JsonResponse(data)
        if User.objects.filter(email=request.GET.get('email')).exists() and request.GET.get(
                'email') != request.user.email:
            data = {"is_updated": "False"}
            return JsonResponse(data)
        if student.objects.filter(phone_no=request.GET.get('phone_no')).exists() and request.GET.get(
                'phone_no') != studentdata.phone_no:
            data = {"is_updated": "False"}
            return JsonResponse(data)

        data = {"is_updated": "True"}
        return JsonResponse(data)

    if request.user.is_authenticated:
        email = request.POST.get('updated_email')
        phone_no = request.POST.get('updated_phone_no')
        college_id = request.POST.get('updated_college_id')
        college_name = request.POST.get('updated_college_name')
        password = request.POST.get('updated_password')

        print("||||||||||||||||||||||||||||||||||")

        print(email)
        print(phone_no)
        print(college_id)
        print(college_name)
        print(password)
        user = authenticate(request, username=request.user.email, password=password)
        if user is None:
            print("--------------------------------------")
            return render(request, "users_student/student_profile2.html")

        if student.objects.filter(user=request.user).exists():
            userobj = student.objects.get(user=request.user)
            userobj.phone_no = phone_no
            userobj.college_id = college_id
            userobj.college_name = "SKN"
            print("****************************")
            print(userobj.profile_picture.name)
            print(project_path)
            if request.FILES.get('updated_image'):
                os.remove(project_path + "/media/" + userobj.profile_picture.name)
                userobj.profile_picture = request.FILES.get('updated_image')

            user.email = email
            user.username = email
            user.save()
            userobj.save()
            logout(request)
            user_auth = authenticate(request, username=email, password=password)
            login(request, user_auth)

            return redirect('/users_student/profile')
    else:
        return render(request, "users_student/student_profile2.html")


def search_user(request):
    username = request.GET.get('username')
    already_taged = request.GET.get('already_taged')
    already_taged = already_taged.split(",")
    if "" in already_taged:
        already_taged.remove("")
    lists = []
    list_remove = []
    if username is None:
        username = '-'
    if request.user.is_authenticated:
        lists = []
        if User.objects.filter(email__contains=username).exists():
            lists = User.objects.filter(email__contains=username)
            lists1 = [i.email for i in lists]
            lists = lists1
            for l in lists:
                if l in already_taged:
                    list_remove.append(l)
    for l_r in list_remove:
        if l_r in lists:
            lists.remove(l_r)
    if request.user.email in lists:
        lists.remove(request.user.email)
    return JsonResponse({'data': lists})
