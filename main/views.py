from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm

def home(request):
    return render(request, 'main/home.html')

def projects(request):
    projects = Project.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    
    # Contexto para renderização do template
    context = {
        'projects': projects,
        'tags': tags,
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

@login_required
def delete_project(request, project_id):
    # Garantir que apenas superusers possam excluir
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para excluir projetos.')
        return redirect('main:projects')
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Projeto excluído com sucesso!')
        return redirect('main:projects')
    
    return render(request, 'main/delete_project.html', {'project': project})

def contact(request):
    return render(request, 'main/contact.html')

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    # Projetos relacionados baseados em tags
    related_projects = Project.objects.filter(tags__in=project.tags.all()).exclude(id=project.id).distinct()[:3]
    
    return render(request, 'main/project_detail.html', {
        'project': project,
        'related_projects': related_projects
    })
