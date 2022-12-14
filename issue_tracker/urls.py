from django.urls import path

from issue_tracker.views import (
    IssueListView, DetailIssueView,
    IssueEditView, DeleteIssueView, IssueCreateView
)
from issue_tracker.views.project_views import (
    ProjectListView, ProjectView, ProjectCreateView,
    ProjectIssueCreateView, ProjectEditView, ProjectDeleteView, ProjectUsersUpdateView)

app_name = 'issue_tracker'

issue_urls = [
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
    path('project/<int:pk>/users/edit/', ProjectUsersUpdateView.as_view(), name='project_users_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/issue/create/', ProjectIssueCreateView.as_view(), name='project_issue_create'),
]

urlpatterns = issue_urls + project_urls
