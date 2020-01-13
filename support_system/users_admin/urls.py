from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('register_admin/', views.register_admin, name='register_admin'),
                  path('login_admin/', views.login_admin, name='login_admin'),
                  path('profile_admin/', views.profile_admin, name='profile_admin'),
                  path('phone_no_available/', views.phone_no_available, name='phone_no_available'),
                  path('username_available/', views.username_available, name='username_available'),
                  path('teacher_id_available/', views.teacher_id_available, name='teacher_id_available'),
                  path('email_available/', views.email_available, name='email_available'),
                  path('phone_no_char/', views.phone_no_char, name='phone_no_char'),
                  path('generate_otp/', views.generate_otp, name='generate_otp'),
                  path('check_otp/', views.check_otp, name='check_otp'),
                  path('accept/', views.markaccepted, name='mark_accepted'),
                  path('mark_solved/', views.mark_solved, name='mark_solved'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)