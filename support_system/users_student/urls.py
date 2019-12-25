from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.register_student, name='register_student'),
    path('username_avaliable/', views.username_avaliable, name='username_avaliable'),
    path('login/', views.login_student, name='login_student'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

