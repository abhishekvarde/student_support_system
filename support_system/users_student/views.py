from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from .models import student


def validator(college_id, first_name, last_name, year, college_name, email, phone_no):
    error_code = "0000000"
    return error_code


def register_student(request):
    if request.method == 'POST':
        college_id = request.POST.get('college_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        year = request.POST.get('year')
        college_name = request.POST.get('college_name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        cnf_password = request.POST.get('cnf_password')

        #request['email'] = email

        error_code = validator(college_id, first_name, last_name, year, college_name, email, phone_no, password,
                               cnf_password)

        if error_code != "0000000":
            return render(request, 'register_student.html', {"college_id": college_id, "first_name": first_name,
                                                             "last_name": last_name, "year": year,
                                                             "college_name": college_name, "email": email,
                                                             "phone_no": phone_no, "password": password,
                                                             "cnf_password": cnf_password})
        else:

            User.objects.create_user(username=email, password=password,email=email)

            user = authenticate(request,username = email,password = password)

            if user is not None:
                login(request,user)
                print("Auth")
            else:
                print("NOT")

            student_details = student(college_id=college_id, first_name=first_name, last_name=last_name,
                                      year=year, college_name=college_name, phone_no=phone_no)
            student_details.save()
            return render(request, 'users_.html')
    else:
        return render(request, 'users_student/register_student.html')


def login_student(request):

    return render(request, 'users_student/login_student.html')
