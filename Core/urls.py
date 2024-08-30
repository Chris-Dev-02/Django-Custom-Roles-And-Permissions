"""
URL configuration for Core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Projects import views as projectViews
from Auth import views as authViews

urlpatterns = [
    path('admin/', admin.site.urls),
    #Authentication
    path('login', authViews.login),
    path('signup', authViews.signup),
    path('test_token', authViews.test_token),
    #Testing
    path('roles/<int:role_id>/add-permissions/', projectViews.add_permissions_to_role, name='add-permissions-to-role'),
    path('projects/<int:project_id>/', projectViews.project_list, name='project-task-list'),
    # Project URLs
    path('projects/', projectViews.list_projects, name='list-projects'),
    path('projects/create/', projectViews.create_project, name='create-project'),
    path('projects/<int:pk>/', projectViews.retrieve_project, name='retrieve-project'),
    path('projects/<int:pk>/update/', projectViews.update_project, name='update-project'),
    path('projects/<int:pk>/delete/', projectViews.delete_project, name='delete-project'),
    # Role URLs
    path('roles/', projectViews.list_roles, name='list-roles'),
    path('roles/create/', projectViews.create_role, name='create-role'),
    path('roles/<int:pk>/', projectViews.retrieve_role, name='retrieve-role'),
    path('roles/<int:pk>/update/', projectViews.update_role, name='update-role'),
    path('roles/<int:pk>/delete/', projectViews.delete_role, name='delete-role'),
    # Project Membership URLs
    path('memberships/', projectViews.list_project_memberships, name='list-memberships'),
    path('memberships/create/', projectViews.create_project_membership, name='create-membership'),
    path('memberships/<int:pk>/', projectViews.retrieve_project_membership, name='retrieve-membership'),
    path('memberships/<int:pk>/update/', projectViews.update_project_membership, name='update-membership'),
    path('memberships/<int:pk>/delete/', projectViews.delete_project_membership, name='delete-membership'),
    # Permission URLs
    path('permissions/', projectViews.list_permissions, name='list-permissions'),
    path('permissions/create/', projectViews.create_permission, name='create-permission'),
    path('permissions/<int:pk>/', projectViews.retrieve_permission, name='retrieve-permission'),
    path('permissions/<int:pk>/update/', projectViews.update_permission, name='update-permission'),
    path('permissions/<int:pk>/delete/', projectViews.delete_permission, name='delete-permission'),
    
    path('projects/<int:project_id>/permissions/', projectViews.get_user_permissions, name='project-permissions'),
    path('app-permissions/', projectViews.get_all_permissions, name='app-permissions'),
    path('model-permissions/', projectViews.model_permissions, name='model-permissions'),
]
