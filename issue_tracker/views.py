from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from issue_tracker.forms import IssueModelForm
from issue_tracker.models import Issue


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = Issue.objects.all()
        return context


class CreateIssueView(TemplateView):
    template_name = 'create_issue.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IssueModelForm()
        return context
