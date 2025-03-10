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
from .models import Project, ProjectDraft, Tag, Top3Card  # Adicionado ProjectDraft
from .forms import ProjectForm, ContactForm
from django.utils import timezone
from django.template.loader import render_to_string

# Configure logging
logger = logging.getLogger(__name__)

def home(request):
    # Get all TOP 3 cards (agora incluindo os originais que foram migrados)
    top3_cards = Top3Card.objects.all().order_by('display_order', 'created_at')
    
    context = {
        'top3_cards': top3_cards,
        'user': request.user,
    }
    
    return render(request, 'main/home.html', context)

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
        messages.error(request, 'Você não tem permissão para criar projetos.', extra_tags='project')
        return redirect('main:projects')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # Sempre cria o projeto base
            project = form.save()
            
            # Processar tags
            if 'tags_input' in form.cleaned_data:
                tag_names = [t.strip() for t in form.cleaned_data['tags_input'].split(',') if t.strip()]
                
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)
            
            # Se o botão "Salvar Rascunho" foi clicado, marca como temporário
            if 'save_draft' in request.POST:
                messages.success(request, 'Projeto criado como rascunho! Será visível apenas quando salvar as alterações.', extra_tags='project')
                return redirect('main:edit_project', slug=project.slug)
            else:
                messages.success(request, 'Projeto criado com sucesso!', extra_tags='project')
                return redirect('main:project_detail', slug=project.slug)
    else:
        form = ProjectForm()
    
    return render(request, 'main/create_project.html', {
        'form': form,
        'action': 'create',
        'tinymce_api_key': settings.TINYMCE_API_KEY
    })

@user_passes_test(lambda u: u.is_superuser)
def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        
        if form.is_valid():
            if 'save_draft' in request.POST:
                # Salvar como rascunho
                draft, created = ProjectDraft.objects.get_or_create(project=project)
                
                # Atualizar os campos do rascunho com os dados do formulário
                draft.title = form.cleaned_data['title']
                draft.short_description = form.cleaned_data['short_description']
                draft.content = form.cleaned_data['content']
                draft.status = form.cleaned_data['status']
                draft.project_type = form.cleaned_data['project_type']
                draft.start_date = form.cleaned_data['start_date']
                draft.end_date = form.cleaned_data['end_date']
                draft.url = form.cleaned_data['url']
                draft.github_url = form.cleaned_data['github_url']
                draft.featured = form.cleaned_data['featured']
                
                # Salvar imagem se fornecida
                if 'image' in request.FILES:
                    draft.image = request.FILES['image']
                
                draft.save()
                
                # Processar tags (armazenadas separadamente)
                if 'tags_input' in form.cleaned_data:
                    # Salvar as tags como uma string no rascunho
                    draft.tags_list = form.cleaned_data['tags_input']
                    draft.save()
                
                messages.success(request, 'Alterações salvas como rascunho! O projeto original permanece inalterado até que você salve as alterações.', extra_tags='project')
            else:
                # Salvar alterações diretamente
                project = form.save()
                
                # Processar tags
                if 'tags_input' in form.cleaned_data:
                    project.tags.clear()
                    tag_names = [t.strip() for t in form.cleaned_data['tags_input'].split(',') if t.strip()]
                    
                    for tag_name in tag_names:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        project.tags.add(tag)
                
                # Se existia rascunho, remover
                if hasattr(project, 'draft'):
                    project.draft.delete()
                
                messages.success(request, 'Projeto atualizado com sucesso!', extra_tags='project')
                return redirect('main:project_detail', slug=project.slug)
            
            return redirect('main:edit_project', slug=project.slug)
    else:
        # Verifica se existe um rascunho para este projeto
        form = ProjectForm(instance=project, project=project)
        
        # Preparar as tags para o formulário
        if project.tags.exists():
            form.initial['tags_input'] = ','.join([tag.name for tag in project.tags.all()])
        
        # Se existe rascunho, mostrar dados do rascunho
        has_draft = hasattr(project, 'draft') and project.draft
    
    return render(request, 'main/create_project.html', {
        'form': form,
        'is_edit': True,
        'project': project,
        'has_draft': has_draft,
        'tinymce_api_key': settings.TINYMCE_API_KEY
    })

@user_passes_test(lambda u: u.is_superuser)
def apply_draft(request, slug):
    """Aplica as alterações do rascunho ao projeto original"""
    project = get_object_or_404(Project, slug=slug)
    
    if not hasattr(project, 'draft') or not project.draft:
        messages.error(request, 'Não há rascunho para este projeto.', extra_tags='project')
        return redirect('main:edit_project', slug=project.slug)
    
    draft = project.draft
    
    # Aplicar as alterações do rascunho ao projeto
    project = draft.apply_to_project()
    
    # Processar tags se foram armazenadas no rascunho
    if hasattr(draft, 'tags_list') and draft.tags_list:
        project.tags.clear()
        tag_names = [t.strip() for t in draft.tags_list.split(',') if t.strip()]
        
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            project.tags.add(tag)
    
    # Excluir o rascunho após aplicá-lo
    draft.delete()
    
    messages.success(request, 'As alterações do rascunho foram aplicadas com sucesso!', extra_tags='project')
    return redirect('main:project_detail', slug=project.slug)

@user_passes_test(lambda u: u.is_superuser)
def discard_draft(request, slug):
    """Descarta o rascunho sem aplicar as alterações"""
    project = get_object_or_404(Project, slug=slug)
    
    if not hasattr(project, 'draft') or not project.draft:
        messages.error(request, 'Não há rascunho para este projeto.', extra_tags='project')
    else:
        project.draft.delete()
        messages.success(request, 'Rascunho descartado com sucesso!', extra_tags='project')
    
    return redirect('main:edit_project', slug=project.slug)

@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Projeto excluído com sucesso!', extra_tags='project')
        return redirect('main:projects')
    
    return render(request, 'main/delete_project.html', {'project': project})

@login_required
def project_preview(request):
    """Gera uma prévia do projeto sem salvá-lo no banco de dados"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Criar uma instância temporária do projeto
            temp_project = Project(
                title=request.POST.get('title', 'Título do Projeto'),
                short_description=request.POST.get('short_description', ''),
                content=request.POST.get('content', ''),
                project_type=request.POST.get('project_type', 'personal'),
                status=request.POST.get('status', 'in_progress'),
                start_date=request.POST.get('start_date') or timezone.now().date(),
                url=request.POST.get('url', '#')
            )
            
            # Processar data de término se fornecida
            end_date = request.POST.get('end_date')
            if end_date:
                temp_project.end_date = end_date
                
            # Processar URL do GitHub se fornecida
            github_url = request.POST.get('github_url')
            if github_url:
                temp_project.github_url = github_url
                
            # Processar tags
            tags_input = request.POST.get('tags_input', '')
            tags = []
            for tag_name in [t.strip() for t in tags_input.split(',') if t.strip()]:
                tags.append({'name': tag_name})
                
            # Renderizar o template de preview
            html = render_to_string('main/project_preview.html', {
                'project': temp_project,
                'tags': tags,
                'is_preview': True
            }, request=request)
            
            return JsonResponse({'html': html, 'success': True})
        except Exception as e:
            logger.error(f"Error in project_preview: {str(e)}")
            return JsonResponse({'error': str(e), 'success': False}, status=400)
    
    return JsonResponse({'error': 'Método não permitido', 'success': False}, status=405)

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
                body,  # Usando a variável de ambiente
                sender_email,
                ['jerbessonc@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, 'Sua mensagem foi enviada com sucesso!', extra_tags='contact')
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

@user_passes_test(lambda u: u.is_superuser)
def add_top3(request):
    if request.method == 'POST':
        top3_id = request.POST.get('top3_id')
        
        # Determinar se estamos editando ou criando
        if top3_id:
            # Editar TOP3 existente
            top3 = get_object_or_404(Top3Card, id=top3_id)
            
            # Atualizar campos de texto
            top3.icon_class = request.POST.get('icon_class')
            top3.title = request.POST.get('title')
            top3.item1_name = request.POST.get('item1_name')
            top3.item1_link = request.POST.get('item1_link') or None
            top3.item2_name = request.POST.get('item2_name')
            top3.item2_link = request.POST.get('item2_link') or None
            top3.item3_name = request.POST.get('item3_name')
            top3.item3_link = request.POST.get('item3_link') or None
            top3.fun_comment = request.POST.get('fun_comment')
            
            # Atualizar imagens apenas se fornecidas
            if 'item1_image' in request.FILES:
                top3.item1_image = request.FILES['item1_image']
            if 'item2_image' in request.FILES:
                top3.item2_image = request.FILES['item2_image']
            if 'item3_image' in request.FILES:
                top3.item3_image = request.FILES['item3_image']
                
            top3.save()
            messages.success(request, 'TOP 3 atualizado com sucesso!')
            
        else:
            # Criar novo TOP3
            top3 = Top3Card(
                icon_class=request.POST.get('icon_class'),
                title=request.POST.get('title'),
                item1_name=request.POST.get('item1_name'),
                item1_link=request.POST.get('item1_link') or None,
                item2_name=request.POST.get('item2_name'),
                item2_link=request.POST.get('item2_link') or None,
                item3_name=request.POST.get('item3_name'),
                item3_link=request.POST.get('item3_link') or None,
                fun_comment=request.POST.get('fun_comment')
            )
            
            # Adicionar imagens
            if 'item1_image' in request.FILES:
                top3.item1_image = request.FILES['item1_image']
            if 'item2_image' in request.FILES:
                top3.item2_image = request.FILES['item2_image']
            if 'item3_image' in request.FILES:
                top3.item3_image = request.FILES['item3_image']
                
            top3.save()
            messages.success(request, 'Novo TOP 3 adicionado com sucesso!')
            
    return redirect('main:home')

@user_passes_test(lambda u: u.is_superuser)
def delete_top3(request, top3_id):
    if request.method == 'POST':
        top3 = get_object_or_404(Top3Card, id=top3_id)
        top3.delete()
        messages.success(request, 'TOP 3 excluído com sucesso!')
    return redirect('main:home')

@user_passes_test(lambda u: u.is_superuser)
def get_top3(request, top3_id):
    """API para obter dados de um TOP3 card para edição"""
    top3 = get_object_or_404(Top3Card, id=top3_id)
    data = {
        'id': top3.id,
        'icon_class': top3.icon_class,
        'title': top3.title,
        'item1_name': top3.item1_name,
        'item1_link': top3.item1_link or '',
        'item1_image_url': top3.item1_image.url,
        'item2_name': top3.item2_name,
        'item2_link': top3.item2_link or '',
        'item2_image_url': top3.item2_image.url,
        'item3_name': top3.item3_name,
        'item3_link': top3.item3_link or '',
        'item3_image_url': top3.item3_image.url,
        'fun_comment': top3.fun_comment
    }
    return JsonResponse(data)
