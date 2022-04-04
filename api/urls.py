from django.urls import path

from api.views import ProjectApiView

urlpatterns = [
    path('projects/<int:pk>', ProjectApiView.as_view()),
]
