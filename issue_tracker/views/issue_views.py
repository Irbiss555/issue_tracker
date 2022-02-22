from urllib.parse import urlencode

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class IssueCreateView(LoginRequiredMixin, FormView):
    template_name = 'issue/create_issue.html'
    form_class = IssueModelForm

    def form_valid(self, form):
        project = form.cleaned_data['project']
        summary = form.cleaned_data['summary']
        description = form.cleaned_data['description']
        status = form.cleaned_data['status']
        types = form.cleaned_data['type']
        self.issue = Issue.objects.create(
            project=project,
            summary=summary,
            description=description,
            status=status
        )
        self.issue.type.set(types)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue_tracker:detail_issue', kwargs={'pk': self.issue.pk})


class DetailIssueView(TemplateView):
    template_name = 'issue/issue_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = get_object_or_404(Issue, pk=kwargs['pk'])
        return context


class IssueEditView(LoginRequiredMixin, UpdateView):
    template_name = 'issue/edit_issue.html'
    model = Issue
    form_class = IssueModelForm
    context_object_name = 'issue'

    def get_success_url(self):
        return reverse('issue_tracker:detail_issue', kwargs={'pk': self.object.pk})


class DeleteIssueView(LoginRequiredMixin, DeleteView):
    template_name = 'issue/issue_template.html'
    model = Issue
    success_url = reverse_lazy('issue_tracker:issue_list')
