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


# Create your views here.

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
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new project",
        request_body=ProjectSerializer,
        responses={201: ProjectSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific project by ID",
        responses={200: ProjectSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


# Vistas basadas en clases para el CRUD
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'  # Ruta a la plantilla para listar proyectos
    context_object_name = 'projects'  # Nombre de la variable en el contexto

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'  # Ruta a la plantilla para detalles de un proyecto
    context_object_name = 'project'  # Nombre de la variable en el contexto

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm  # Usar el formulario personalizado para crear un proyecto
    template_name = 'projects/project_form.html'  # Ruta a la plantilla para crear un proyecto
    success_url = reverse_lazy('project_list')  # Redirección al listar proyectos tras crear uno

    def form_valid(self, form):
        serializer = ProjectSerializer(data=form.cleaned_data)
        if not serializer.is_valid():
            for field, errors in serializer.errors.items():
                for error in errors:
                    form.add_error(field, error)
            return self.form_invalid(form)

        # Asignar latitud y longitud desde el serializer
        form.instance.latitude = serializer.validated_data.get('latitude')
        form.instance.longitude = serializer.validated_data.get('longitude')

        return super().form_valid(form)

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm  # Usar el formulario personalizado para crear un proyecto
    template_name = 'projects/project_form.html'  # Reutilizamos la plantilla para crear/editar
    success_url = reverse_lazy('project_list')  # Redirección al listar proyectos tras editar uno

    def form_valid(self, form):
        serializer = ProjectSerializer(instance=self.object, data=form.cleaned_data)
        if not serializer.is_valid():
            for field, errors in serializer.errors.items():
                for error in errors:
                    form.add_error(field, error)
            return self.form_invalid(form)

        # Asignar latitud y longitud desde el serializer
        form.instance.latitude = serializer.validated_data.get('latitude')
        form.instance.longitude = serializer.validated_data.get('longitude')

        return super().form_valid(form)

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'  # Ruta a la plantilla para confirmar eliminación
    success_url = reverse_lazy('project_list')  # Redirección al listar proyectos tras eliminar uno

class ProjectDistanceListView(ListView):
    model = Project
    template_name = 'projects/project_distance_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
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