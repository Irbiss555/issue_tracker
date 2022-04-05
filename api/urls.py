from django.urls import path

from api.views import ProjectApiView, IssueApiView

urlpatterns = [
    path('projects/<int:pk>', ProjectApiView.as_view()),
    path('issues/<int:pk>', IssueApiView.as_view()),
]
