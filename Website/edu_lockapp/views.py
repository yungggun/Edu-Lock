from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.utils.timezone import now
from .forms import ProfilePictureForm
from django.http import JsonResponse
from .models import Profile, Doors, ClassGroup, Log
from django.contrib.auth.models import Group, User

from django.views.decorators.csrf import csrf_exempt
import json



def user_management(request):
    return render(request, "edu_lockapp/dashboard/user_management.html")

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

    if request.method == "POST":
        user = request.user
        profile = user.profile

        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()

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


def open_door(request):
    uid = request.GET.get("uid")
    device_id = request.GET.get("device_id")

    if not uid or not device_id:
        return JsonResponse({"error": "missing parameters"}, status=400)

    try:
        profile = Profile.objects.get(uid_hash=uid)
    except Profile.DoesNotExist:
        return JsonResponse({"allowed": False})

    if profile.is_blocked:
        return JsonResponse({"allowed": False})

    try:
        door = Doors.objects.get(device_id=device_id)
    except Doors.DoesNotExist:
        return JsonResponse({"allowed": False})

    # Admins und Lehrer haben immer Zugriff
    if profile.role in ["teacher", "admin"]:
        return JsonResponse({"allowed": True})

    # Zugriff für Schüler, wenn Klassen übereinstimmen
    if profile.class_group == door.class_group:
        return JsonResponse({"allowed": True})

    return JsonResponse({"allowed": False})



from django.shortcuts import get_object_or_404

@login_required
def user_management(request):

    profiles = Profile.objects.all()
    class_groups = ClassGroup.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")

        # -------------------------------
        # Benutzer blockieren/entblocken
        # -------------------------------
        if action == "toggle_block" and user_id:
            profile = get_object_or_404(Profile, user__id=user_id)
            profile.is_blocked = not profile.is_blocked
            profile.save()
            messages.success(
                request,
                f"{profile.user.username} wurde {'gesperrt' if profile.is_blocked else 'freigegeben'}."
            )
            return redirect('users')

        # -------------------------------
        # Benutzer bearbeiten
        # -------------------------------
        elif action == "edit_user" and user_id:
            profile = get_object_or_404(Profile, user__id=user_id)
            username = request.POST.get('username', profile.user.username).strip()
            email = request.POST.get('email', profile.user.email).strip()
            group_id = request.POST.get('class_group')

            # Username prüfen
            if User.objects.exclude(id=profile.user.id).filter(username=username).exists():
                messages.error(request, "Dieser Benutzername ist bereits vergeben.")
                return redirect('users')

            # Email prüfen
            if User.objects.exclude(id=profile.user.id).filter(email=email).exists():
                messages.error(request, "Diese E-Mail ist bereits vergeben.")
                return redirect('users')

            # Werte setzen
            profile.user.username = username
            profile.user.email = email
            profile.user.save()

            profile.class_group = ClassGroup.objects.get(id=group_id) if group_id else None
            profile.save()

            messages.success(request, f"{profile.user.username} wurde aktualisiert.")
            return redirect('users')

        # -------------------------------
        # Benutzer erstellen
        # -------------------------------
        elif action == "create_user":
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            group_id = request.POST.get('class_group')

            # Validierung
            if not username or not email or not password:
                messages.error(request, "Bitte fülle alle Pflichtfelder aus.")
                return redirect('users')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Dieser Benutzername ist bereits vergeben.")
                return redirect('users')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Diese E-Mail ist bereits vergeben.")
                return redirect('users')

            # User anlegen
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Profile anlegen
            class_group = ClassGroup.objects.get(id=group_id) if group_id else None
            Profile.objects.create(
                user=user,
                class_group=class_group
            )

            messages.success(request, f"Benutzer {username} wurde erstellt.")
            return redirect('users')

    return render(request, "edu_lockapp/dashboard/user_management.html", {
        "profiles": profiles,
        "class_groups": class_groups
    })


@login_required
def doors(request):
    from django.contrib.auth.models import Group  # falls noch nicht importiert

    if request.method == 'POST':
        name = request.POST.get('name')
        controller_ip = request.POST.get('controller_ip')
        is_locked = request.POST.get('is_locked') == 'True'
        access_group_ids = request.POST.getlist('access_groups')

        # Neue Tür erstellen
        door = Doors.objects.create(
            name=name,
            controller_ip=controller_ip,
            is_locked=is_locked
        )

        # Gruppen zuordnen
        for group_id in access_group_ids:
            group = Group.objects.get(id=group_id)
            door.access_groups.add(group)

        return redirect('doors')  # Seite neu laden

    # GET-Request: Seite anzeigen
    doors = Doors.objects.all()  # ✅ richtig
    groups = Group.objects.all()
    show_welcome = True

    context = {
        'doors': doors,
        'groups': groups,
        'show_welcome': show_welcome,
    }

    return render(request, 'edu_lockapp/dashboard/doors.html', context)


def logs(request):
    logs = Log.objects.all().order_by("-timestamp")
    return render(request, "edu_lockapp/dashboard/logs.html", {
        "logs": logs
    })


@csrf_exempt
def api_log(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Werte aus JSON holen
            uid_hash = data.get("uid_hash")          # Hash vom ESP32
            log_type = data.get("type", "Zugriff")  # Standard "Zugriff"
            message = data.get("message", "")
            source = data.get("source", "ESP32")    # z. B. ESP32

            if not uid_hash:
                return JsonResponse({"status": "error", "message": "uid_hash required"}, status=400)

            # Profil anhand des Hash finden
            profile = Profile.objects.filter(uid_hash=uid_hash).first()
            if profile:
                user = profile.user
            else:
                user = None
                message += " (Unbekannter Nutzer)"

            # Log speichern
            Log.objects.create(
                type=log_type,
                message=message,
                user=user,
                source=source
            )

            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "POST required"}, status=405)


