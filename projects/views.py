from django.shortcuts import render
from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms



# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project_form.html'
    fields = ['name', 'description', 'start_date', 'end_date', 'status', 'location']
    success_url = reverse_lazy('project_list')

    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})
        form.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'project_form.html'
    fields = ['name', 'description', 'start_date', 'end_date', 'status', 'location']
    success_url = reverse_lazy('project_list')

    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})
        form.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('project_list')