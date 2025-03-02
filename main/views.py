from django.shortcuts import render
from .models import Project, Tag

def home(request):
    return render(request, 'main/home.html')

def projects(request):
    projects = Project.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    return render(request, 'main/projects.html', {
        'projects': projects,
        'tags': tags
    })

def contact(request):
    return render(request, 'main/contact.html')
