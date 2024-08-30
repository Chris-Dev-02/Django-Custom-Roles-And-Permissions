from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Role, ProjectMembership
from django.contrib.auth.models import User, Permission
from .serializers import ProjectSerializer, RoleSerializer, ProjectMembershipSerializer, PermissionSerializer, AddPermissionsToRoleSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .decorators import project_permission_required
from django.contrib.contenttypes.models import ContentType
from .models import Role, ProjectMembership

'''
==================================================================================================================================
Only Testing
==================================================================================================================================
'''
@api_view(['POST'])
def assign_role(request, project_id, user_id):
    project = Project.objects.get(id=project_id)
    user = User.objects.get(id=user_id)
    role = Role.objects.get(id=request.data.get('role_id'))
    
    ProjectMembership.objects.create(user=user, project=project, role=role)
    
    return Response({"message": "Role assigned successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_permissions_to_role(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return Response({"error": "Role not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AddPermissionsToRoleSerializer(data=request.data)
    
    if serializer.is_valid():
        permission_ids = serializer.validated_data['permission_ids']
        permissions = Permission.objects.filter(id__in=permission_ids)
        role.permissions.add(*permissions)
        return Response({"message": "Permissions added successfully."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
==================================================================================================================================
CRUD for Project
==================================================================================================================================
'''
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@project_permission_required('can_view_project')
def list_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectSerializer(project)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectSerializer(project, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
'''
==================================================================================================================================
CRUD for Role
==================================================================================================================================
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_role(request):
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_roles(request):
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_role(request, pk):
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RoleSerializer(role)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_role(request, pk):
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RoleSerializer(role, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_role(request, pk):
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    role.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
'''
==================================================================================================================================
CRUD for membership
==================================================================================================================================
'''
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_project_membership(request):
    serializer = ProjectMembershipSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_project_memberships(request):
    memberships = ProjectMembership.objects.all()
    serializer = ProjectMembershipSerializer(memberships, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_project_membership(request, pk):
    try:
        membership = ProjectMembership.objects.get(pk=pk)
    except ProjectMembership.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectMembershipSerializer(membership)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_project_membership(request, pk):
    try:
        membership = ProjectMembership.objects.get(pk=pk)
    except ProjectMembership.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectMembershipSerializer(membership, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_project_membership(request, pk):
    try:
        membership = ProjectMembership.objects.get(pk=pk)
    except ProjectMembership.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    membership.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

'''
==================================================================================================================================
CRUD for Permissions
==================================================================================================================================
'''
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_permission(request):
    serializer = PermissionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_permissions(request):
    permissions = Permission.objects.all()
    serializer = PermissionSerializer(permissions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_permission(request, pk):
    try:
        permission = Permission.objects.get(pk=pk)
    except Permission.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PermissionSerializer(permission)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_permission(request, pk):
    try:
        permission = Permission.objects.get(pk=pk)
    except Permission.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PermissionSerializer(permission, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_permission(request, pk):
    try:
        permission = Permission.objects.get(pk=pk)
    except Permission.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    permission.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_user_permissions(request, project_id):
    user = request.user
    membership = ProjectMembership.objects.filter(user=user, project_id=project_id).first()

    if not membership:
        return Response({"error": "User is not a member of this project"}, status=400)

    permissions = membership.role.permissions.all()
    serializer = PermissionSerializer(permissions, many=True)

    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_all_permissions(request):
    app_labels = ['Projects']  # Replace with your actual app labels

    permissions = Permission.objects.filter(content_type__app_label__in=app_labels)
    serializer = PermissionSerializer(permissions, many=True)

    return Response(serializer.data, status=200)

@api_view(['GET'])
def model_permissions(request):
    # Define the models for which you want to get permissions
    models = [Role, ProjectMembership]  # Replace with your actual models
    
    # Get content types for these models
    content_types = ContentType.objects.get_for_models(*models).values()
    
    # Filter permissions by these content types
    permissions = Permission.objects.filter(content_type__in=content_types)
    
    # Serialize and return the permissions
    serializer = PermissionSerializer(permissions, many=True)
    return Response(serializer.data, status=200)
