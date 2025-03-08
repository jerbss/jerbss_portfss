from django.db import models
from django.utils.html import mark_safe
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
import uuid
from datetime import date
from tinymce.models import HTMLField
from cloudinary.models import CloudinaryField
import logging
from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver

# Configure logging
logger = logging.getLogger(__name__)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Ordem alfabética padrão

class Project(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'Em Andamento'),  # Corrigido para "Em Andamento" com A maiúsculo
        ('completed', 'Concluído'),
    )
    
    TYPE_CHOICES = (
        ('academic', 'Acadêmico'),
        ('personal', 'Pessoal'),
        ('professional', 'Profissional'),
    )
    
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    short_description = models.CharField('Breve Descrição', max_length=200, default='')  # Limite de 200 caracteres
    content = models.TextField('Conteúdo Completo', default='')
    image = CloudinaryField('image', folder='projects', blank=True, null=True)
    status = models.CharField('Status', max_length=50, choices=STATUS_CHOICES, default='in_progress')
    project_type = models.CharField(
        'Tipo',
        max_length=50,
        choices=TYPE_CHOICES,
        default='personal'
    )
    start_date = models.DateField('Data de Início', null=True, blank=True)
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
    
    @property
    def get_status_display_html(self):
        status_classes = {
            'in_progress': 'badge bg-warning text-dark',
            'completed': 'badge bg-success text-light'
        }
        status_class = status_classes.get(self.status, 'badge bg-secondary text-light')
        return mark_safe(f'<span class="{status_class}">{self.get_status_display()}</span>')
    
    @property
    def get_date_display(self):
        if not self.start_date:
            return "Data não definida"
        
        if self.status == 'completed' and self.end_date:
            return mark_safe(f'<span class="text-body">{self.start_date.strftime("%d/%m/%Y")} - {self.end_date.strftime("%d/%m/%Y")}</span>')
        return mark_safe(f'<span class="text-body">{self.start_date.strftime("%d/%m/%Y")} - Em Andamento</span>')  # Corrigido "Em Andamento"
    
    @property
    def get_type_display_html(self):
        """Retorna o tipo do projeto com formatação HTML adequada"""
        type_classes = {
            'academic': 'project-card__type project-card__type--academic',
            'personal': 'project-card__type project-card__type--personal',
            'professional': 'project-card__type project-card__type--professional'
        }
        type_class = type_classes.get(self.project_type, 'project-card__type')
        return mark_safe(f'<span class="{type_class}">{self.get_project_type_display()}</span>')

    @property
    def safe_image_url(self):
        """Safely get image URL with fallback"""
        try:
            if self.image:
                return self.image.url
        except Exception as e:
            logger.error(f"Error getting image URL for project {self.id}: {str(e)}")
        return None

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

# Signal para limpar tags órfãs quando um projeto for excluído
@receiver(post_delete, sender=Project)
def clean_orphan_tags(sender, instance, **kwargs):
    """Remove tags that are not associated with any projects"""
    Tag.objects.annotate(project_count=models.Count('projects')).filter(project_count=0).delete()

# Signal para limpar tags quando um projeto é atualizado e tags são removidas
@receiver(m2m_changed, sender=Project.tags.through)
def clean_tags_on_m2m_change(sender, instance, action, **kwargs):
    """Clean orphan tags when they are removed from a project"""
    if action in ['post_remove', 'post_clear']:
        # Apenas execute a limpeza após as operações de remoção
        Tag.objects.annotate(project_count=models.Count('projects')).filter(project_count=0).delete()
