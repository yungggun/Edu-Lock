from django.contrib import admin
from .models import Profile, Doors, ClassGroup, Log

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "class_group", "is_blocked")
    list_filter = ("role", "class_group", "is_blocked")

    search_fields = ('user__username', 'group')

admin.site.register(Doors)
admin.site.register(ClassGroup)
admin.site.register(Log)

