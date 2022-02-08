from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from issue_tracker.forms import ProjectModelForm
from issue_tracker.models import Project


class ProjectListView(ListView):
    template_name = 'project/project_list.html'
    model = Project
    context_object_name = 'projects'


class ProjectView(DetailView):
    template_name = 'project/project_detail.html'
    model = Project
    context_object_name = 'project'


class ProjectCreateView(CreateView):
    template_name = 'project/project_create.html'
    model = Project
    form_class = ProjectModelForm

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})
