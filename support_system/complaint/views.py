from django.http import HttpResponse
from django.shortcuts import render

def post(request):
    return render(request,'complaint/post.html')