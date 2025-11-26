from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
<<<<<<< HEAD
    path('dashboard/profile/', views.profile, name='profile'),  
=======
>>>>>>> 791a39d86f5272bb4f13927b5cda6de149304c60
]
