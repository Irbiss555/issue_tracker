from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import ProjectSerializer, IssueSerializer

from issue_tracker.models import Project, Issue


class ProjectApiView(APIView):
    # template_name = 'project/project_detail.html'
    # model = Project
    # context_object_name = 'project'
    def get(self, request, *args, **kwargs):
        object = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        serializer = ProjectSerializer(object)
        return Response(serializer.data)



# class ProjectEditView(APIView):
#     template_name = 'project/project_edit.html'
#     model = Project
#     form_class = ProjectModelForm
#     context_object_name = 'project'
#     permission_required = 'issue_tracker.change_project'
#
#     def get_success_url(self):
#         return reverse('issue_tracker:project_detail', kwargs={'pk': self.object.pk})
#
#
# class ProjectDeleteView(APIView):
#     template_name = 'project/project_detail.html'
#     model = Project
#     success_url = reverse_lazy('issue_tracker:project_list')
#     context_object_name = ''
#     permission_required = 'issue_tracker.delete_project'
