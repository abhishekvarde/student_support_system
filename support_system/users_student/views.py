from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse
from complaint.models import Complaint
from support_system.views import append_likes
from .models import student
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
        print(request)
        college_id = request.POST.get('college_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        year = request.POST.get('year')
        college_name = request.POST.get('college_name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        cnf_password = request.POST.get('cnf_password')

        year = 2000
        phone_no = "9999999999"

        # request['email'] = email

        if not User.objects.filter(username=email).exists():
            user_obj = User.objects.create_user(username=email, password=password, email=email)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.save()

            user = authenticate(request, username=email, password=password)

            student_details = student(user=user, college_id=college_id, year=year, college_name=college_name,
                                      phone_no=phone_no)
            student_details.save()
        return redirect('/users_student/login')
    else:
        return render(request, 'users_student/regestration.html')


def login_student(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        print("i am in loogin")
        if user is not None:
            login(request, user)
            return redirect('/')
    logout(request)
    return render(request, 'users_student/login_student.html')


def student_profile(request):
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
        userdata = student.objects.get(user=request.user)

        if requested_data is None:
            requested_data = "all"

        if requested_data == "all":
            postsobj = Complaint.objects.filter(user=request.user)
            for post in postsobj:
                posts.append(post)
        elif requested_data == "pending":
            posts = Complaint.objects.filter(user=request.user).filter(status="pending")
        elif requested_data == "ongoing":
            posts = Complaint.objects.filter(user=request.user).filter(status="ongoing")
        elif requested_data == "solved":
            posts = Complaint.objects.filter(user=request.user).filter(status="solved")
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
            posts = Complaint.objects.filter(user=request.user).filter(status="rejected")
        print(posts)
        posts = append_likes(request, posts)
        return render(request, 'users_student/student_profile2.html',
                      {"usernmae": request.user.username, "userdata": userdata, "posts": posts,
                       'requesteddata': requested_data})
    else:
        if User.objects.filter(username=user_name).exists():
            user = User.objects.get(username=user_name)
            userdata = student.objects.get(user=user)
            posts = Complaint.objects.filter(user=User.objects.get(username=user_name))
            return render(request, 'users_student/student_profile_another.html',
                          {"usernmae": request.user.username, "userdata": userdata, "posts": posts})
        print("user doesn't exists")
        return redirect('/users_student/login/')


def update_profile(request):
    if request.user.is_authenticated:
        email = request.GET.get('email')
        phone_no = request.GET.get('phone_no')
        college_id = request.GET.get('college_id ')
        college_name = request.GET.get('college_name')
        password = request.GET.get('password')
        profile_pic = request.GET.get('profile_pic')

        image = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        print("Profile picture")
        print(profile_pic)
        print("Profile picture")

        user = authenticate(request, username=request.user.email, password=password)
        if user is None:
            data = {
                "is_updated": "false"
            }
            return JsonResponse(data)

        if student.objects.filter(user=request.user).exists():
            userobj = student.objects.get(user=request.user)
            userobj.phone_no = phone_no
            userobj.college_id = college_id
            userobj.college_name = college_name
            userobj.profile_pics = profile_pic
            userobj.url = uploaded_file_url
            user = User.objects.get(email=request.user.email)
            user.email = email
            user.username = email

            if not User.objects.filter(email=request.user.email).exists():
                data = {
                    "is_updated": "false"
                }
                return JsonResponse(data)

            if User.objects.filter(email=email).exists() and request.user.email != email:
                data = {
                    "is_updated": "false"
                }
                return JsonResponse(data)

            if user.username == email and user.email == email and userobj.college_name == college_name and \
                    userobj.college_id == college_id and userobj.phone_no == phone_no and \
                    userobj.url == uploaded_file_url:
                data = {
                    "is_updated": "false"
                }
                return JsonResponse(data)

            user.save()
            userobj.save()
            logout(request)
            user_auth = authenticate(request, username=email, password=password)
            login(request, user_auth)
            data = {
                "is_updated": "true"
            }
            return JsonResponse(data)
    else:
        data = {
            "is_updated": "false"
        }
        return JsonResponse(data)


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
