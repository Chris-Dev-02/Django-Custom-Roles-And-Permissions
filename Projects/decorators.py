from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import ProjectMembership

def project_permission_required(permission_codename):
    def decorator(func):
        @wraps(func)
        def wrapped_view(request, *args, **kwargs):
            project_id = kwargs.get('project_id')
            user = request.user

            membership = ProjectMembership.objects.filter(user=user, project_id=project_id).first()

            if not membership:
                return Response({"detail": "User is not a member of this project."}, status=status.HTTP_403_FORBIDDEN)

            if not membership.role.permissions.filter(codename=permission_codename).exists():
                return Response({"detail": "You do not have the required permission."}, status=status.HTTP_403_FORBIDDEN)

            return func(request, *args, **kwargs)

        return wrapped_view
    return decorator
