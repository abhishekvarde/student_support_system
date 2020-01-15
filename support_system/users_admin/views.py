from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import CommitteeMember, Otp
from complaint.models import Complaint


def register_admin(request):
    if request.POST:
        first_name = request.POST.get('first_name_admin')
        last_name = request.POST.get('last_name_admin')
        gender = request.POST.get('gender_admin')
        dob = request.POST.get('dob_admin')
        branch = request.POST.get('branch_admin')
        phone_no = request.POST.get('phone_no_admin')
        username = request.POST.get('username_admin')
        committee = request.POST.get('level_admin')
        college = request.POST.get('college_admin')
        teacher_id = request.POST.get('college_id_admin')
        email = request.POST.get('email_admin')
        password = request.POST.get('password_admin')
        cnf_password = request.POST.get('re_password_admin')
        print('--------------------------------')
        print(committee)
        print('--------------------------------')

        if not User.objects.filter(username=username).exists():
            user_obj = User.objects.create_user(username=username, password=password, email=email)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.save()
        else:
            message = "username already taken."
            return redirect("/login")

        committee_obj = CommitteeMember(user=user_obj, committee=committee, phone_no=phone_no, college=college,
                                        teacher_id=teacher_id)  # , gender=gender, dob=dob, branch=branch)
        committee_obj.save()

    return redirect("/login")


def send_request(committee_obj):
    print(committee_obj.usern)


def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username_admin')
        password = request.POST.get('password_admin')

        print("--------------------")
        print(username)
        print(password)
        print("--------------------")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("i am in loogin")
            login(request, user)
            return redirect("/users_admin/profile_admin")
        return redirect("/login")


def profile_admin(request):
    print("i am here")
    requesteddata = request.GET.get("requesteddata")
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        complaints = []
        if CommitteeMember.objects.filter(user=request.user).exists():
            print(request.user.username)
            print(request.user.username)
            print(request.user.username)
            print(request.user.username)
            print(request.user.username)
            print(request.user.username)
            userdata = CommitteeMember.objects.get(user=request.user)

            if requesteddata == "pending" or requesteddata is None:
                complaints = Complaint.objects.filter(level=userdata.committee, status="pending")
            if requesteddata == "ongoing":
                userobj = CommitteeMember.objects.get(user=request.user)
                ongoint_list = userobj.ongoing_complaints
                ongoint_list = ongoint_list.split(",")
                while '' in ongoint_list:
                    ongoint_list.remove('')
                print("##################")
                print(ongoint_list)
                for i in ongoint_list:
                    if Complaint.objects.filter(id=int(i), status="ongoing").exists():
                        complaints.append(Complaint.objects.get(id=int(i), status="ongoing"))
                for i in complaints:
                    print(i.id)
            if requesteddata == "solved":
                userobj = CommitteeMember.objects.get(user=request.user)
                solved_list = userobj.solved_complaints
                solved_list = solved_list.split(",")
                print("##################")
                print(solved_list)
                if '' in solved_list:
                    solved_list.remove('')
                for i in solved_list:
                    if Complaint.objects.filter(id=int(i), status="solved").exists():
                        complaints.append(Complaint.objects.get(id=int(i), status="solved"))
                for i in complaints:
                    print(i.id)
            print(request.user.username)
            print(request.user.username)
            print(request.user.username)
            print(request.user.username)
            print(request.user.username)
            print(request.user.username)

            if requesteddata == "rejected":
                userobj = CommitteeMember.objects.get(user=request.user)
                rejected_list = userobj.rejected_complaints
                rejected_list = rejected_list.split(",")
                print("##################")
                print(rejected_list)
                for i in rejected_list:
                    if Complaint.objects.filter(id=int(i), status="rejected").exists():
                        complaints.append(Complaint.objects.get(id=int(i), status="rejected"))
                for i in complaints:
                    print(i.id)
            return render(request, "users_admin/profile_admin.html", {'userdata': userdata, 'posts': complaints,"requesteddata":requesteddata})
    return redirect("/login")


def phone_no_available(request):
    phone_no = request.GET.get('phone_no', None)
    print(phone_no)

    data = {
        "is_valid": CommitteeMember.objects.filter(phone_no=phone_no).exists()
    }

    return JsonResponse(data)


def username_available(request):
    username = request.GET.get('username', None)
    print(username)

    data = {
        "is_valid": User.objects.filter(username=username).exists()
    }

    return JsonResponse(data)


def teacher_id_available(request):
    teacher_id = request.GET.get('teacher_id', None)
    print(teacher_id)

    data = {
        "is_valid": CommitteeMember.objects.filter(teacher_id=teacher_id).exists()
    }

    return JsonResponse(data)


def email_available(request):
    email = request.GET.get('email', None)
    print(email)

    data = {
        "is_valid": User.objects.filter(email=email).exists()
    }

    return JsonResponse(data)


def phone_no_char(request):
    phone_no = request.GET.get('phone_no', None)
    print(phone_no)
    send = "False"

    for no in phone_no:
        if no not in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            send = "True"
            break

    data = {
        "is_valid": send
    }
    return JsonResponse(data)


def generate_otp(request):
    phone_no = request.GET.get('phone_no', None)
    print(phone_no)
    email = request.GET.get('email', None)
    print(email)

    otp_phone_no = "123456"
    otp_email = "123456"

    otp_details = Otp(phone_no=phone_no, otp_phone_no=otp_phone_no,
                      email=email, otp_email=otp_email)
    otp_details.save()

    data = {
        "is_valid": "Sent successfully"
    }

    return JsonResponse(data)


def check_otp(request):
    flag = 0

    phone_no = request.GET.get('phone_no', None)
    print(phone_no)
    email = request.GET.get('email', None)
    print(email)

    otp_phone_no = request.GET.get('otp_phone_no', None)
    print(otp_phone_no)
    otp_email = request.GET.get('otp_email', None)
    print(otp_email)

    # check

    check_otp = Otp.objects.filter(phone_no=phone_no).filter(email=email).first()

    if check_otp:
        if otp_phone_no == check_otp.otp_phone_no and otp_email == check_otp.otp_email:
            flag = 1

    if flag == 1:
        data = {
            "correct_otp": "true"
        }
        return JsonResponse(data)
    else:
        data = {
            "correct_otp": "false"
        }
        return JsonResponse(data)


def markaccepted(request):
    print("+++++++++++++++++++++++++++++++++")
    if request.user.is_authenticated:
        post_id = request.GET.get('post_id')

        print("-----------------------------------------")
        print(post_id)
        if Complaint.objects.filter(id=int(post_id)).exists():
            user_obj = CommitteeMember.objects.get(user=request.user)
            accepted_post = user_obj.ongoing_complaints
            accepted_list = accepted_post.split(",")

            if "" in accepted_list:
                accepted_list.remove("")
            if post_id not in accepted_list:
                compile_obj = Complaint.objects.get(id=post_id)
                compile_obj.status = "ongoing"
                compile_obj.save()
                accepted_list.append(post_id)
                accepted_post = ",".join(accepted_list)
                user_obj.ongoing_complaints = accepted_post
                user_obj.save()
                return profile_admin(request)


def mark_solved(request):
    if request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        response = request.POST.get('response')
        action_type = request.POST.get('action_type')
        print(response)
        print("-----------------------------------------")
        print(action_type)
        print(post_id)
        if Complaint.objects.filter(id=int(post_id)).exists():
            user_obj = CommitteeMember.objects.get(user=request.user)
            if int(action_type) == 1:
                solved_post = user_obj.solved_complaints
                solved_list = solved_post.split(",")
                accepted_post = user_obj.ongoing_complaints
                accepted_list = accepted_post.split(",")
                if post_id in accepted_list:
                    accepted_list.remove(post_id)
                    accepted_post = ",".join(accepted_list)
                    user_obj.ongoing_complaints = accepted_post
                    user_obj.save()
                if "" in solved_list:
                    solved_list.remove("")
                if post_id not in solved_list:
                    compile_obj = Complaint.objects.get(id=post_id)
                    compile_obj.status = "solved"
                    compile_obj.solution = response
                    compile_obj.save()
                    solved_list.append(post_id)
                    solved_post = ",".join(solved_list)
                    user_obj.solved_complaints = solved_post
                    user_obj.save()
                    return redirect("/users_admin/profile_admin?requesteddata=ongoing")
                else:
                    return redirect("/users_admin/profile_admin?requesteddata=ongoing")

            else:
                rejected_post = user_obj.rejected_complaints
                rejected_list = rejected_post.split(",")
                accepted_post = user_obj.ongoing_complaints
                accepted_list = accepted_post.split(",")
                if post_id in accepted_list:
                    accepted_list.remove(post_id)
                    accepted_post = ",".join(accepted_list)
                    user_obj.ongoing_complaints = accepted_post
                    user_obj.save()
                if "" in rejected_list:
                    rejected_list.remove("")
                if post_id not in rejected_list:
                    compile_obj = Complaint.objects.get(id=post_id)
                    compile_obj.status = "rejected"
                    compile_obj.solution = response
                    compile_obj.save()
                    rejected_list.append(post_id)
                    rejected_post = ",".join(rejected_list)
                    user_obj.rejected_complaints = rejected_post
                    user_obj.save()
                    return redirect("/users_admin/profile_admin?requesteddata=ongoing")
                else:
                    return redirect("/users_admin/profile_admin?requesteddata=ongoing")
