from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_student, name='register_student'),
    path('login/', views.login_student, name='login_student'),

]
