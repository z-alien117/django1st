# filepath: /Users/alien/Desktop/django1st/oowlish/projects/api_urls.py
from django.urls import path
from .views import ProjectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = router.urls