from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.utils.timezone import now
from .forms import ProfilePictureForm


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            try:
                profile, created = Profile.objects.get_or_create(user=user)
                profile.last_login = now().strftime("%d.%m.%Y %H:%M")
                if profile.registered_since is None:
                    profile.registered_since = now().date()
                profile.save()
            except:
                pass

            return redirect('dashboard')
        else:
            messages.error(request, "E-Mail oder Passwort ist falsch.")

    return render(request, 'edu_lockapp/login.html')


def home(request):
    return render(request, 'edu_lockapp/index.html')


@login_required
def dashboard(request):
    if request.user.groups.filter(name='admin').exists():

        profile, created = Profile.objects.get_or_create(user=request.user)
        
        profile.last_login = now().strftime("%d.%m.%Y %H:%M") 
        profile.save()

        show_welcome = not request.session.get('welcome_shown', False)

        if show_welcome:
            request.session['welcome_shown'] = True

        return render(request, 'edu_lockapp/dashboard.html', {
            'show_welcome': show_welcome
        })

    messages.error(request, "Du hast keine Berechtigung, auf das Dashboard zuzugreifen.")
    return redirect('login')


@login_required
def profile(request):
    if not request.user.groups.filter(name='admin').exists():
        messages.error(request, "Keine Berechtigung.")
        return redirect('login')

    if request.method == "POST":
        user = request.user
        profile = user.profile

        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()
        
        messages.success(request, "Profil erfolgreich gespeichert.")
        return redirect('profile')

    return render(request, 'edu_lockapp/dashboard/profile.html', {
        "profile": request.user.profile,
        "user": request.user
    })


@login_required
def upload_avatar(request):
    if request.method == "POST":
        try:
            profile = request.user.profile
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]
                profile.save()
        except Exception as e:
            messages.error(request, "Fehler beim Hochladen.")
            
    return redirect("profile")