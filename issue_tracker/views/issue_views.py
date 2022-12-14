from urllib.parse import urlencode

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from issue_tracker.forms import IssueModelForm, SimpleSearchForm
from issue_tracker.models import Issue


class IssueListView(ListView):
    template_name = 'issue/issue_list.html'
    context_object_name = 'issues'
    model = Issue
    paginate_by = 5
    allow_empty = False

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            context = {
                '404_error': 'Oops something went wrong!',
                'form': self.form
            }
            if self.search_value:
                context['query'] = urlencode({'search': self.search_value})
            return render(request, 'issue/issue_list.html', context=context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class IssueCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'issue/create_issue.html'
    form_class = IssueModelForm
    permission_required = 'issue_tracker.add_issue'

    def has_permission(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('issue_tracker:detail_issue', kwargs={'pk': self.object.pk})


class DetailIssueView(TemplateView):
    template_name = 'issue/issue_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = get_object_or_404(Issue, pk=kwargs['pk'])
        return context


class IssueEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'issue/edit_issue.html'
    model = Issue
    form_class = IssueModelForm
    context_object_name = 'issue'
    permission_required = 'issue_tracker.change_issue'

    def has_permission(self):
        issue = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        project = issue.project
        return (
                (super().has_permission() and (self.request.user in project.users.all())) or
                self.request.user.is_superuser
        )

    def get_success_url(self):
        return reverse('issue_tracker:detail_issue', kwargs={'pk': self.object.pk})


class DeleteIssueView(PermissionRequiredMixin, DeleteView):
    template_name = 'issue/issue_template.html'
    model = Issue
    permission_required = 'issue_tracker.delete_issue'

    def has_permission(self):
        issue = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        project = issue.project
        return (
                (super().has_permission() and (self.request.user in project.users.all())) or
                self.request.user.is_superuser
        )

    def get_success_url(self):
        return reverse('issue_tracker:project_detail', kwargs={'pk': self.object.project.pk})
