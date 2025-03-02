from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Type(models.TextChoices):
        PERSONAL = 'PERSONAL', 'Personal'
        PROFESSIONAL = 'PROFESSIONAL', 'Professional'
        
    project_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.PERSONAL
    )

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    projects = models.ManyToManyField(Project, related_name='tags')

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
