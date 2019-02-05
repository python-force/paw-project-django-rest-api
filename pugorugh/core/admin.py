from django.contrib import admin

from pugorugh.core.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)