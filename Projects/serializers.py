from rest_framework import serializers
from django.contrib.auth.models import Permission
from .models import Project, Role, ProjectMembership

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']

class ProjectMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMembership
        fields = ['id', 'user', 'project', 'role', 'date_joined']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name', 'content_type']

class AddPermissionsToRoleSerializer(serializers.Serializer):
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )

    def validate_permission_ids(self, value):
        permissions = Permission.objects.filter(id__in=value)
        if len(permissions) != len(value):
            raise serializers.ValidationError("Some of the provided permissions do not exist.")
        return value
