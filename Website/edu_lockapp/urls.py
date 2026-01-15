from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import open_door

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.profile, name='profile'), 
    path("dashboard/profile/upload-avatar/", views.upload_avatar, name="profile_upload_avatar"),
    path("api/open-door/", open_door),
    path("dashboard/users/", views.user_management, name="users"),
    path('dashboard/doors/', views.doors, name='doors'),
    path("dashboard/logs/", views.logs, name="logs"),
    path('api/log/', views.api_log, name='api_log'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


