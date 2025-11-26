from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "E-Mail oder Passwort ist falsch.")

    return render(request, 'edu_lockapp/login.html')


def home(request):
    return render(request, 'edu_lockapp/index.html')


@login_required
def dashboard(request):
    if request.user.groups.filter(name='admin').exists():
        # Prüfen, ob der Benutzer die Welcome-Message schon gesehen hat
        show_welcome = not request.session.get('welcome_shown', False)

        # Session-Flag setzen, damit es nur einmal pro Login angezeigt wird
        if show_welcome:
            request.session['welcome_shown'] = True

        return render(request, 'edu_lockapp/dashboard.html', {
            'show_welcome': show_welcome
        })
    else:
        messages.error(request, "Du hast keine Berechtigung, auf das Dashboard zuzugreifen.")
        return redirect('login')
<<<<<<< HEAD

@login_required
def profile(request):
    if request.user.groups.filter(name='admin').exists():
        return render(request, 'edu_lockapp/dashboard/profile.html')
    else:
        messages.error(request, "Du hast keine Berechtigung, auf das Profil zuzugreifen.")
        return redirect('login')
=======
>>>>>>> 791a39d86f5272bb4f13927b5cda6de149304c60
