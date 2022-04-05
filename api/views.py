from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import ProjectSerializer, IssueSerializer

from issue_tracker.models import Project, Issue


class ProjectApiView(APIView):
    def get(self, request, *args, **kwargs):
        object = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        serializer = ProjectSerializer(object)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = ProjectSerializer(
            data=request.data,
            instance=get_object_or_404(Project, pk=self.kwargs.get('pk'))
        )
        if serializer.is_valid():
            project = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response({'pk': pk})


class IssueApiView(APIView):
    def get(self, request, *args, **kwargs):
        object = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        serializer = IssueSerializer(object)
        return Response(serializer.data)
