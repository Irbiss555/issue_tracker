from django.forms import ModelForm

from issue_tracker.models import Issue


class IssueModelForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'type']
