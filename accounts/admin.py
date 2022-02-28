from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.models import Profile


class ProfileInLine(admin.StackedInline):
    model = Profile
    fields = ['avatar', 'github_link', 'about_info']


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInLine]


User = get_user_model()
admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
