from rest_framework import serializers
from issue_tracker.models import Project, Issue


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'users',
            'title',
            'description',
            'start_date',
            'end_date'
        ]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id',
            'project',
            'summary',
            'description',
            'status',
            'type',
            'created_at',
            'updated_at',
        ]
