from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('projects/<slug:slug>/edit/', views.edit_project, name='edit_project'),
    path('projects/<slug:slug>/delete/', views.delete_project, name='delete_project'),
    path('contact/', views.contact, name='contact'),
]