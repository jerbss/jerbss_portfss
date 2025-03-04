from django.db import models
from django.utils.html import mark_safe
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
import uuid
from datetime import date
from tinymce.models import HTMLField

class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'Em andamento'),
        ('completed', 'Concluído'),
    )
    
    TYPE_CHOICES = (
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('design', 'Design'),
        ('other', 'Outro'),
    )
    
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField('Breve Descrição', max_length=500, default='')
    content = HTMLField('Conteúdo Completo', default='')
    image = models.ImageField('Capa do Projeto', upload_to='projects/')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='in_progress')
    project_type = models.CharField('Tipo', max_length=20, choices=TYPE_CHOICES, default='web')
    start_date = models.DateField('Data de Início')  # Removed auto_now_add=True
    end_date = models.DateField('Data de Conclusão', null=True, blank=True)
    created_at = models.DateTimeField('Data de Publicação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name="projects")
    url = models.URLField('Link do Projeto', blank=True, null=True)
    github_url = models.URLField('Link do GitHub', blank=True, null=True)
    featured = models.BooleanField('Projeto Destacado', default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
    
    def __str__(self):
        return self.title
    
    def get_status_display_html(self):
        if self.status == 'in_progress':
            return mark_safe('<span class="badge bg-warning">Em Andamento</span>')
        return mark_safe('<span class="badge bg-success">Concluído</span>')
    
    def get_date_display(self):
        if self.status == 'in_progress':
            return f"{self.start_date.strftime('%d/%m/%Y')} - Em Andamento"
        return f"{self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_id = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_id}"
        super().save(*args, **kwargs)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
