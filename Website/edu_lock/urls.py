"""
URL configuration for edu_lock project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
<<<<<<< HEAD
from django.urls import path, include
from django.contrib import admin
=======
from django.contrib import admin
from django.urls import path
>>>>>>> 791a39d86f5272bb4f13927b5cda6de149304c60
from edu_lockapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('edu_lockapp.urls')),   # ⭐ Deine App-URLs aktivieren!
]
=======
    path('', views.home, name='home'),               # /
    path('login/', views.login_view, name='login'),  # /login
    path('dashboard/', views.dashboard, name='dashboard'),   # /dashboard
]

>>>>>>> 791a39d86f5272bb4f13927b5cda6de149304c60
