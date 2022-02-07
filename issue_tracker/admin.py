from django.contrib import admin

# Register your models here.
from issue_tracker.models import Status, Type, Issue, Project


class IssueAdmin(admin.ModelAdmin):
    list_display = ['summary', 'status', 'type', 'updated_at']
    search_fields = ['summary']
    fields = ['summary', 'project', 'status', 'type', 'description', 'updated_at', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    fields = ['title', 'description', 'start_date', 'end_date']


admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Issue)
admin.site.register(Project)
