from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
import cloudinary
import cloudinary.api
import os
import logging
import traceback
import sys
from django.db.models import Count
from django.conf import settings
from cloudinary.uploader import upload
from .models import Project, Tag
from .forms import ProjectForm, ContactForm

# Configure logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'main/home.html')

def projects(request):
    try:
        logger.info("Entering projects view")
        projects = Project.objects.all().order_by('-created_at')
        
        # Debug info - check number of projects and their image fields
        project_info = []
        for p in projects:
            try:
                has_image = bool(p.image)
                image_url = str(p.image.url) if p.image else "No image URL"
                project_info.append({
                    'id': p.id,
                    'title': p.title,
                    'has_image': has_image,
                    'image_url': image_url
                })
            except Exception as img_err:
                logger.error(f"Error accessing image for project {p.id}: {str(img_err)}")
                project_info.append({
                    'id': p.id,
                    'title': p.title,
                    'has_image': "ERROR",
                    'image_error': str(img_err)
                })
        
        logger.debug(f"Project info: {project_info}")
        
        # Buscar apenas tags que estão em uso e ordená-las por frequência e depois alfabeticamente
        tags_with_count = Tag.objects.annotate(
            project_count=Count('projects')
        ).filter(
            project_count__gt=0
        ).order_by('-project_count', 'name')
        
        # Contexto para renderização do template
        context = {
            'projects': projects,
            'tags': tags_with_count,
        }
        
        # Para superuser, adicionar funcionalidades de gerenciamento
        if request.user.is_superuser:
            # Lidar com formulários de criação/edição apenas se for superuser
            if request.method == 'POST':
                form = ProjectForm(request.POST, request.FILES)
                if form.is_valid():
                    project = form.save()
                    
                    # Processar tags
                    tags = request.POST.get('tags', '').split(',')
                    for tag_name in tags:
                        tag_name = tag_name.strip()
                        if tag_name:
                            tag, created = Tag.objects.get_or_create(name=tag_name)
                            project.tags.add(tag)
                            
                    messages.success(request, 'Projeto criado com sucesso!')
                    return redirect('main:projects')
            else:
                form = ProjectForm()
                
            context['form'] = form
        
        return render(request, 'main/projects.html', context)
    except Exception as e:
        logger.error(f"Error in projects view: {str(e)}")
        # Get detailed traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_text = ''.join(tb_lines)
        logger.error(f"Full traceback: {tb_text}")
        
        return render(request, 'main/error.html', {
            'error_message': 'Houve um problema ao carregar os projetos. Por favor, tente novamente mais tarde.',
            'error_details': f"{str(e)}\n\n{tb_text if settings.DEBUG else ''}",
            'debug': settings.DEBUG
        }, status=500)

# Add a new debug view
def debug_projects(request):
    """Debug view to inspect projects and diagnose issues"""
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=401)
    
    try:
        # Get all project data with detailed info
        projects = Project.objects.all()
        project_data = []
        
        for p in projects:
            project_info = {
                'id': p.id,
                'title': p.title,
                'slug': p.slug,
                'image_field_type': type(p.image).__name__,
                'has_image': bool(p.image),
                'tags': [t.name for t in p.tags.all()]
            }
            
            # Try to get image URL
            try:
                if p.image:
                    project_info['image_url'] = p.image.url
                    project_info['cloudinary_public_id'] = getattr(p.image, 'public_id', 'N/A')
                else:
                    project_info['image_url'] = None
            except Exception as img_err:
                project_info['image_error'] = str(img_err)
                
            project_data.append(project_info)
        
        # Get storage configuration
        storage_info = {
            'DEFAULT_FILE_STORAGE': settings.DEFAULT_FILE_STORAGE,
            'CLOUDINARY_ENABLED': settings.CLOUDINARY_ENABLED,
            'CLOUDINARY_STORAGE': {k: "***" if k == "API_SECRET" else v 
                                 for k, v in settings.CLOUDINARY_STORAGE.items()}
        }
        
        # Return as JSON for easy debugging
        return JsonResponse({
            'projects': project_data,
            'storage_config': storage_info,
            'cloudinary_health': test_cloudinary_connection()
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'traceback': traceback.format_exc() if settings.DEBUG else 'Enable DEBUG for traceback'
        }, status=500)

def test_cloudinary_connection():
    """Test Cloudinary connection and return status"""
    try:
        # Simple test to check if Cloudinary is properly configured
        result = cloudinary.api.ping()
        return {'success': True, 'status': 'Connected', 'details': result}
    except Exception as e:
        return {'success': False, 'status': 'Error', 'details': str(e)}

@login_required
def create_project(request):
    # Garantir que apenas superusers possam criar
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para criar projetos.')
        return redirect('main:projects')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Projeto criado com sucesso!')
            return redirect('main:project_detail', slug=project.slug)
    else:
        form = ProjectForm()
    
    return render(request, 'main/create_project.html', {
        'form': form,
        'action': 'create'
    })

@user_passes_test(lambda u: u.is_superuser)
def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            return redirect('main:project_detail', slug=project.slug)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'main/create_project.html', {
        'form': form,
        'is_edit': True,
        'project': project
    })

@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Projeto excluído com sucesso!')
        return redirect('main:projects')
    
    return render(request, 'main/delete_project.html', {'project': project})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            subject = f"Contato via Site - {name}"
            body = (
                f"Você recebeu uma nova mensagem pelo formulário de contato.\n\n"
                f"Nome: {name}\n"
                f"E-mail: {sender_email}\n\n"
                f"Mensagem:\n{message}"
            )
            
            send_mail(
                subject,
                body,
                sender_email,  # Remetente (opcional: pode ser um endereço fixo)
                ['jerbessonc@gmail.com'],  # Destinatário
                fail_silently=False,
            )
            
            messages.success(request, 'Sua mensagem foi enviada com sucesso!')
            return redirect('main:contact')
    else:
        form = ContactForm()
        
    return render(request, 'main/contact.html', {'form': form})

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    # Projetos relacionados baseados em tags
    related_projects = Project.objects.filter(tags__in=project.tags.all()).exclude(id=project.id).distinct()[:3]
    
    return render(request, 'main/project_detail.html', {
        'project': project,
        'related_projects': related_projects
    })

def test_cloudinary(request):
    """Test function to verify Cloudinary configuration."""
    try:
        # Check configuration
        config_info = {
            'cloud_name': settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'),
            'is_setup': bool(settings.CLOUDINARY_STORAGE.get('CLOUD_NAME') and 
                            settings.CLOUDINARY_STORAGE.get('API_KEY') and 
                            settings.CLOUDINARY_STORAGE.get('API_SECRET')),
            'storage_backend': str(settings.DEFAULT_FILE_STORAGE),
            'debug_mode': settings.DEBUG,
        }
        
        # Small test upload
        test_upload = upload("https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg", 
                      public_id="test_connection")
        
        # Check existing resources
        resources = cloudinary.api.resources(
            resource_type="image",
            max_results=5,
            type="upload"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Successfully connected to Cloudinary',
            'configuration': config_info,
            'test_upload': test_upload,
            'existing_files': resources.get('resources', [])[:5]  # Show first 5 files
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error connecting to Cloudinary: {str(e)}'
        })
