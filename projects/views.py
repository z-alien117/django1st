from django.shortcuts import render
from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from .forms import ProjectForm
from .utils import calculate_distance
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse

# API ViewSet for Project model
class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @swagger_auto_schema(
        operation_description="List all projects",
        responses={200: ProjectSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        List all projects.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new project",
        request_body=ProjectSerializer,
        responses={201: ProjectSerializer()}
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new project.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific project by ID",
        responses={200: ProjectSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific project by ID.
        """
        return super().retrieve(request, *args, **kwargs)

# Class-based views for CRUD operations on Project model
class ProjectListView(ListView):
    """
    View to list all projects.
    """
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    """
    View to display details of a specific project.
    """
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

class ProjectCreateView(CreateView):
    """
    View to create a new project.
    """
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        """
        Validate and save the form.
        """
        serializer = ProjectSerializer(data=form.cleaned_data)
        if not serializer.is_valid():
            for field, errors in serializer.errors.items():
                for error in errors:
                    form.add_error(field, error)
            return self.form_invalid(form)

        form.instance.latitude = serializer.validated_data.get('latitude')
        form.instance.longitude = serializer.validated_data.get('longitude')

        return super().form_valid(form)

class ProjectUpdateView(UpdateView):
    """
    View to update an existing project.
    """
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        """
        Validate and save the form.
        """
        serializer = ProjectSerializer(instance=self.object, data=form.cleaned_data)
        if not serializer.is_valid():
            for field, errors in serializer.errors.items():
                for error in errors:
                    form.add_error(field, error)
            return self.form_invalid(form)

        form.instance.latitude = serializer.validated_data.get('latitude')
        form.instance.longitude = serializer.validated_data.get('longitude')

        return super().form_valid(form)

class ProjectDeleteView(DeleteView):
    """
    View to delete a project.
    """
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

class ProjectDistanceListView(ListView):
    """
    View to list projects along with the distances between them.
    """
    model = Project
    template_name = 'projects/project_distance_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        """
        Add distances between projects to the context.
        """
        context = super().get_context_data(**kwargs)
        projects = context['projects']
        distances = []

        for i, project1 in enumerate(projects):
            for j, project2 in enumerate(projects):
                if i < j:
                    distance = calculate_distance(
                        project1.latitude, project1.longitude,
                        project2.latitude, project2.longitude
                    )
                    distances.append({
                        'project1': project1,
                        'project2': project2,
                        'distance': distance
                    })

        context['distances'] = distances
        return context

def health_check(request):
    """
    Health check endpoint.
    """
    return HttpResponse(status=200)