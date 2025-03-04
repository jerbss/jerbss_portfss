from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'url', 'project_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }