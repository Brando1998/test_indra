from django.shortcuts import render, redirect
from apps.projects.models import Project
from apps.users.models import Company
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
import json
# Create your views here.
# CRUD VIEWS

class ProjectsListView(LoginRequiredMixin, View):
    def get(self, request):
        template_name = 'dashboard/projects_list.html'
        context = {
            'company': Company.objects.get(id=request.user.profile.company.id),
            'projects': Project.objects.filter(company=request.user.profile.company),
        }
        return render(request, template_name, context)

class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'company': Company.objects.get(id=request.user.profile.company.id),
        }
        template_name = 'dashboard/projects_create_update.html'
        return render(request, template_name, context)
    
    def post(self, request):
        name = request.POST.get('project_name')
        details = request.POST.get('project_details')
        file_1 = request.FILES['project_docfile_1'] if 'project_docfile_1' in request.FILES else None
        state = request.POST.get('project_state')
        #Project creation
        project = Project(
            company=request.user.profile.company,
            name=name,
            details=details,
            file_1=file_1,
            state=state
        )
        project.save()
        
        return redirect('projects_list')


class ProjectUpdateView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        project = Project.objects.get(id=id)
        context = {
            'project':project,
            'company': Company.objects.get(id=request.user.profile.company.id),
        }
        template_name = 'dashboard/projects_create_update.html'
        return render(request, template_name, context)
    
    def post(self, request, id, *args, **kwargs):
        name = request.POST.get('project_name')
        details = request.POST.get('project_details')
        file_1 = request.FILES['project_docfile_1'] if 'project_docfile_1' in request.FILES else None
        state = request.POST.get('project_state')
        #Project update
        project = Project.objects.get(id=id)
        project.name = name
        project.details = details
        project.file_1 = file_1 if file_1 is not None else project.file_1
        project.state = state
        project.save()
        
        return redirect('projects_list')

class ProjectChangeStatusView(LoginRequiredMixin, View):
    def post(self, request, id, *args, **kwargs):
        result = {}
        project = Project.objects.get(id=id)
        json_data = json.loads(request.body)
        try:
            state = json_data.get("state")
            project.state = state
            project.save()
            result["success"] = "The status has been changed"
        except Exception as e:
            result["error"] = str(e)
        return JsonResponse(result, safe=False)

class ProjectDeleteView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        project = Project.objects.get(id=id)
        project.delete()
        return redirect('projects_list')