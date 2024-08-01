from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Connection, Project, Message

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'name', 'is_developer', 'is_marketer', 'featured', 'subscription_status']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('name', 'is_developer', 'is_marketer', 'skills', 'bio', 'featured', 'profile_views', 'subscription_status')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Connection)
admin.site.register(Project)
admin.site.register(Message)
