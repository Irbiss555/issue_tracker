from urllib.parse import urlencode

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, FormView, ListView
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


class IssueCreateView(FormView):
    template_name = 'issue/create_issue.html'
    form_class = IssueModelForm

    def form_valid(self, form):
        summary = form.cleaned_data['summary']
        description = form.cleaned_data['description']
        status = form.cleaned_data['status']
        types = form.cleaned_data['type']
        self.issue = Issue.objects.create(
            summary=summary,
            description=description,
            status=status
        )
        self.issue.type.set(types)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_issue', kwargs={'pk': self.issue.pk})


class DetailIssueView(TemplateView):
    template_name = 'issue/issue_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = get_object_or_404(Issue, pk=kwargs['pk'])
        return context


class IssueEditView(FormView):
    template_name = 'issue/edit_issue.html'
    form_class = IssueModelForm

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = self.issue
        return context

    def get_initial(self):
        initial = {}
        for key in 'summary', 'description', 'status':
            initial[key] = getattr(self.issue, key)
        initial['type'] = self.issue.type.all()
        return initial

    def form_valid(self, form):
        types = form.cleaned_data.pop('type')
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(self.issue, key, value)
        self.issue.save()
        self.issue.type.set(types)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_issue', kwargs={'pk': self.issue.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Issue, pk=pk)


class DeleteIssueView(TemplateView):
    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        issue.delete()
        return redirect('index')
