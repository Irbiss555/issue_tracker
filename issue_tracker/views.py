from django.shortcuts import render, get_object_or_404, redirect
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

    def post(self, request, *args, **kwargs):
        form = IssueModelForm(request.POST)
        if form.is_valid():
            summary = form.cleaned_data['summary']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']
            type = form.cleaned_data['type']
            issue = Issue.objects.create(
                summary=summary,
                description=description,
                status=status,
                type=type
            )
            return redirect('detail_issue', pk=issue.pk)
        else:
            context = super().get_context_data(**kwargs)
            context['form'] = form
            return super().render_to_response(context=context)


class DetailIssueView(TemplateView):
    template_name = 'issue_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = get_object_or_404(Issue, pk=kwargs['pk'])
        return context


class EditIssueView(TemplateView):
    template_name = 'edit_issue.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IssueModelForm()
        context['issue'] = get_object_or_404(Issue, pk=kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        form = IssueModelForm(request.POST)
        if form.is_valid():
            issue.summary = form.cleaned_data['summary']
            issue.description = form.cleaned_data['description']
            issue.status = form.cleaned_data['status']
            issue.type = form.cleaned_data['type']
            issue.save(update_fields=['summary', 'description', 'status', 'type'])
            return redirect('detail_issue', pk=issue.pk)
        else:
            context = super().get_context_data(**kwargs)
            context['form'] = form
            context['issue'] = issue
            return super().render_to_response(context=context)


class DeleteIssueView(TemplateView):
    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        issue.delete()
        return redirect('index')
