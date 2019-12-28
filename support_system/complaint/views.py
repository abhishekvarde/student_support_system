from django.http import HttpResponse
from django.shortcuts import render
from complaint.models import Complaint, cat
from users_student.models import student
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.shortcuts import redirect


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


def post(request):

    if not request.user.is_authenticated:
        return redirect('/users_student/login/')

    if request.method == 'POST':
        user = User.objects.get(username = request.user.username)
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
        complain = Complaint(user=user, title=title, description=des, tags=tags, image=url)
        complain.save()
        student_obj = student.objects.get(user=user)
        ids = student_obj.post_ids
        ids = ids.split(",")
        ids.append(str(complain.id))
        if "" in ids:
            ids.remove("")
        student_obj.post_ids = ",".join(ids)
        student_obj.save()
        redirect("/")
    else:
        level = request.GET.get('level')
        if level is None or level == "":
            level = "department"
        return render(request, 'complaint/post.html', {'level': level})


# def display(request):
