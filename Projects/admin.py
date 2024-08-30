from django.contrib import admin
from .models import Project, Role, ProjectMembership

# Register your models here.
'''
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Role)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'permissions']

@admin.register(ProjectMembership)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role', 'date_joined']
from django.contrib import admin
'''
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = ['permissions']

class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role', 'date_joined']
    search_fields = ['user__username', 'project__name', 'role__name']
    list_filter = ['project', 'role']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(ProjectMembership, ProjectMembershipAdmin)