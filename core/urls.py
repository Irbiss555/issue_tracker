"""issue_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from issue_tracker.views import (
    IssueListView, DetailIssueView,
    IssueEditView, DeleteIssueView, IssueCreateView
)
from issue_tracker.views.project_views import (
    ProjectListView, ProjectView, ProjectCreateView,
    ProjectIssueCreateView, ProjectEditView, ProjectDeleteView)

issue_urls = [
    path('admin/', admin.site.urls),
    path('issues/', IssueListView.as_view(), name='issue_list'),
    path('issue/create/', IssueCreateView.as_view(), name='create_issue'),
    path('issue/<int:pk>', DetailIssueView.as_view(), name='detail_issue'),
    path('issue/edit/<int:pk>', IssueEditView.as_view(), name='edit_issue'),
    path('issue/delete/<int:pk>', DeleteIssueView.as_view(), name='delete_issue'),
]

project_urls = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>', ProjectView.as_view(), name='project_detail'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/edit/', ProjectEditView.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/issue/create/', ProjectIssueCreateView.as_view(), name='project_issue_create'),
]

urlpatterns = issue_urls
urlpatterns += project_urls
