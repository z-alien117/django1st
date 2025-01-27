from django.shortcuts import render
from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from .forms import ProjectForm



# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


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

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm  # Usar el formulario personalizado para crear un proyecto
    template_name = 'projects/project_form.html'  # Reutilizamos la plantilla para crear/editar
    success_url = reverse_lazy('project_list')  # Redirección al listar proyectos tras editar uno

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'  # Ruta a la plantilla para confirmar eliminación
    success_url = reverse_lazy('project_list')  # Redirección al listar proyectos tras eliminar uno