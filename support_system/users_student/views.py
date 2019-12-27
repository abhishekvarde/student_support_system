from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from complaint.models import Complaint

from .models import student


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
            #
            # if user is not None:
            #     login(request, user)
            #     print("Auth")
            # else:
            #     print("NOT")

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
            return redirect('/complaint/post/')

    return render(request, 'users_student/login_student.html')


def student_profile(request):
    requested_data = request.GET.get('requesteddata')
    print(requested_data)
    posts = []
    if request.user.is_authenticated:

        userdata = student.objects.get(user=request.user)

        if requested_data is None or requested_data == "all":
            postsobj = Complaint.objects.filter(user=request.user)
            for post in postsobj:
                posts.append(post)
            print(posts)
        if requested_data == "pending":
            posts = Complaint.objects.filter(user=request.user).filter(status="pending")
        if requested_data == "ongoing":
            posts = Complaint.objects.filter(user=request.user).filter(status="ongoing")
        if requested_data == "upvoted":
            posts = []
            likedpostids = userdata.liked_complaint
            likedpostids = likedpostids.split(",")
            likedpostids.remove("")
            for likedpostid in likedpostids:
                if Complaint.objects.filter(id=likedpostid).exists():
                    print(Complaint.objects.get(id=likedpostid))
                    # print((Complaint.objects.get(id=likedpostid))[0])
                    posts.append((Complaint.objects.get(id=likedpostid)))
                else:
                    likedpostids.remove(likedpostid)
        if requested_data == "rejected":
            posts = Complaint.objects.filter(user=request.user).filter(status="rejected")
        return render(request, 'users_student/student_profile.html', {"userdata": userdata, "posts": posts,
                                                                      'requested_data': requested_data})


    else:
        #display a separate page for visitors
        return render(request, 'users_student/login.html')