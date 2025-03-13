from django.urls import path
from . import views
from .views import test_cloudinary

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.create_project, name='create_project'),
    # Colocar a URL de preview ANTES das URLs com parâmetros dinâmicos (slug)
    path('projects/preview/', views.project_preview, name='project_preview'),
    # URLs com slugs vêm depois para não capturarem o "preview" como slug
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('projects/<slug:slug>/edit/', views.edit_project, name='edit_project'),
    path('projects/<slug:slug>/delete/', views.delete_project, name='delete_project'),
    path('projects/<slug:slug>/apply-draft/', views.apply_draft, name='apply_draft'),
    path('projects/<slug:slug>/discard-draft/', views.discard_draft, name='discard_draft'),
    path('contact/', views.contact, name='contact'),
    path('test-cloudinary/', test_cloudinary, name='test_cloudinary'),
    path('debug/projects/', views.debug_projects, name='debug_projects'),
    path('top3/add/', views.add_top3, name='add_top3'),
    path('top3/delete/<int:top3_id>/', views.delete_top3, name='delete_top3'),
    path('api/top3/<int:top3_id>/', views.get_top3, name='get_top3'),
    path('top3/save-order/', views.save_top3_order, name='save_top3_order'),
    path('api/cloudinary/upload/', views.cloudinary_upload, name='cloudinary_upload'),
    path('api/tags/search/', views.search_tags, name='search_tags'),
]