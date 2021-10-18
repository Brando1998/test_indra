from django.urls import path, include 
from apps.projects.views import ProjectsListView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, ProjectChangeStatusView

urlpatterns = [
    # projects crud
    path('projects/list', ProjectsListView.as_view(), name='projects_list'),
    path('projects/create', ProjectCreateView.as_view(), name='project_create'),
    path('projects/update/<int:id>', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/delete/<int:id>', ProjectDeleteView.as_view(), name='project_delete'),
    path('projects/change_status/<int:id>', ProjectChangeStatusView.as_view(), name='project_change_status'),
]