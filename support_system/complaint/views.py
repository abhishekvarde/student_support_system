from django.http import HttpResponse
from django.shortcuts import render
from complaint.models import Complaint
from users_student.models import student


def post(request):
    return render(request, 'complaint/post.html')


# dont call this function.

def like(request):
    username = request.POST.get('username')
    post_id = request.POST.get('post_id')
    response = 'Failed'
    if request.user.is_authenticated:
        if request.user == username:
            if Complaint.objects.filter(id=post_id).exists():
                user_obj = student.objects.get(username=username)
                liked_post = user_obj.liked_complaint
                liked_list = liked_post.split(",")
                if post_id not in liked_list:
                    compile_obj = Complaint.objects.get(id=post_id)
                    compile_obj.liked += 1
                    liked_list.append(post_id)
                    liked_post = ",".join(liked_list)
                    user_obj.liked_complaint = liked_post
                    user_obj.save()
                    response = 'Success'
    return request
