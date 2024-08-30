from django.contrib.auth.models import User, Group, Permission
from django.db import models

from rest_framework.permissions import BasePermission

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Role(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, related_name='roles')

class ProjectMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)



class HasProjectPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get('project_id')
        membership = ProjectMembership.objects.filter(user=user, project_id=project_id).first()
        
        if not membership:
            return False
        
        required_permission = view.permission_required
        if membership.role.permissions.filter(codename=required_permission).exists():
            return True
        
        return False
