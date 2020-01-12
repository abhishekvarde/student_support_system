from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('post/', views.post, name='post'),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('tracker/', views.tracker, name='tracker'),
    path('allow/', views.allow, name='allow'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
