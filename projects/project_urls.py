# filepath: /Users/alien/Desktop/django1st/oowlish/projects/project_urls.py
from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, ProjectDistanceListView, health_check

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('distances/', ProjectDistanceListView.as_view(), name='project_distance_list'),
    path('health/', health_check, name='health_check'),

]