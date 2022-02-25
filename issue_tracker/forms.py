from django import forms

from issue_tracker.models import Issue, Project


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date']


class ProjectUsersModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['users']


class IssueModelForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['project', 'summary', 'description', 'status', 'type']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")
