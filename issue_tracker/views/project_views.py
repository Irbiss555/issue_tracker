from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from issue_tracker.forms import ProjectModelForm, IssueModelForm, ProjectUsersModelForm
from issue_tracker.models import Project, Issue


class ProjectListView(ListView):
    template_name = 'project/project_list.html'
    model = Project
    context_object_name = 'projects'


class ProjectView(DetailView):
    template_name = 'project/project_detail.html'
    model = Project
    context_object_name = 'project'


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project/project_create.html'
    model = Project
    form_class = ProjectModelForm
    permission_required = 'issue_tracker.add_project'

    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('issue_tracker:project_detail', kwargs={'pk': self.object.pk})


class ProjectUsersUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project/project_users_update.html'
    model = Project
    form_class = ProjectUsersModelForm
    context_object_name = 'project'
    permission_required = 'issue_tracker.change_project_users'

    def has_permission(self):
        return super().has_permission() and (self.request.user in self.get_object().users.all())

    def get_success_url(self):
        return reverse('issue_tracker:project_detail', kwargs={'pk': self.object.pk})


class ProjectIssueCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project/project_issue_create.html'
    model = Issue
    form_class = IssueModelForm
    permission_required = 'issue_tracker.add_issue'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and (self.request.user in project.users.all())

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        return redirect('issue_tracker:project_detail', pk=project.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
        return context


class ProjectEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'project/project_edit.html'
    model = Project
    form_class = ProjectModelForm
    context_object_name = 'project'
    permission_required = 'issue_tracker.change_project'

    def get_success_url(self):
        return reverse('issue_tracker:project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'project/project_detail.html'
    model = Project
    success_url = reverse_lazy('issue_tracker:project_list')
    context_object_name = ''
    permission_required = 'issue_tracker.delete_project'
