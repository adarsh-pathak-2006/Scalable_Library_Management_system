from django.contrib import admin
from .models import User, Profile, College

admin.site.register(College)
admin.site.register(Profile)
admin.site.register(User)
