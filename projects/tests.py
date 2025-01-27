from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from .models import Project
from .serializers import ProjectSerializer

class ProjectModelTest(TestCase):
    def setUp(self):
        self.project_data = {
            'name': 'Test Project',
            'description': 'Test Description',
            'start_date': date(2024, 1, 1),
            'status': 'pending',
            'location': 'New York, NY'
        }
        self.project = Project.objects.create(**self.project_data)

    def test_project_creation(self):
        """Test project creation"""
        self.assertTrue(isinstance(self.project, Project))
        self.assertEqual(str(self.project), self.project_data['name'])

    def test_project_fields(self):
        """Test project fields"""
        self.assertEqual(self.project.name, self.project_data['name'])
        self.assertEqual(self.project.description, self.project_data['description'])
        self.assertEqual(self.project.start_date, self.project_data['start_date'])
        self.assertEqual(self.project.status, self.project_data['status'])
        self.assertEqual(self.project.location, self.project_data['location'])

class ProjectAPITest(APITestCase):
    def setUp(self):
        self.project_data = {
            'name': 'API Test Project',
            'description': 'API Test Description',
            'start_date': '2024-01-01',
            'status': 'pending',
            'location': 'New York, NY'
        }
        self.project = Project.objects.create(
            name='Existing Project',
            description='Existing Description',
            start_date='2024-01-01',
            status='pending',
            location='Los Angeles, CA'
        )

    def test_create_project(self):
        """Test creating a project via API"""
        url = reverse('project-list')
        response = self.client.post(url, self.project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(Project.objects.get(name='API Test Project').description, 
                        'API Test Description')

    def test_get_project_list(self):
        """Test getting project list"""
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_project_detail(self):
        """Test getting project detail"""
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Existing Project')

    def test_update_project(self):
        """Test updating a project"""
        url = reverse('project-detail', args=[self.project.id])
        update_data = {
            'name': 'Updated Project',
            'description': 'Updated Description',
            'start_date': '2024-01-01',
            'status': 'in_progress',
            'location': 'Chicago, IL'
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.get(id=self.project.id).name, 
                        'Updated Project')

    def test_delete_project(self):
        """Test deleting a project"""
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_invalid_project_creation(self):
        """Test creating a project with invalid data"""
        url = reverse('project-list')
        invalid_data = {
            'name': '',  # Name is required
            'start_date': '2024-01-01',
            'status': 'invalid_status',  # Invalid status
            'location': 'New York, NY'
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)