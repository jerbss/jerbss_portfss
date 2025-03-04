from django import forms
from .models import Project, Tag
from django.utils.text import slugify

class ProjectForm(forms.ModelForm):
    tags_input = forms.CharField(
        label='Tags',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Separe as tags por vírgula'
        }),
        help_text='Separe as tags por vírgula (ex.: django, python, web)'
    )
    
    class Meta:
        model = Project
        fields = [
            'title',
            'short_description',
            'content',
            'image',
            'status',
            'project_type',
            'start_date',
            'end_date',
            'tags_input',
            'url',
            'github_url',
            'featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 200}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'project_type': forms.Select(attrs={
                'class': 'form-control',
                'aria-label': 'Selecione o tipo do projeto'
            }),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializar tags_input com as tags existentes
        if self.instance.pk:
            self.fields['tags_input'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Gerar slug se for nova instância
        if not instance.pk:
            instance.slug = slugify(instance.title)
            
            # Verificar se o slug já existe e adicionar sufixo se necessário
            original_slug = instance.slug
            counter = 1
            while Project.objects.filter(slug=instance.slug).exists():
                instance.slug = f"{original_slug}-{counter}"
                counter += 1
        
        if commit:
            instance.save()
            self.save_m2m()
            
            # Processar as tags
            if 'tags_input' in self.cleaned_data:
                instance.tags.clear()
                tag_names = [t.strip() for t in self.cleaned_data['tags_input'].split(',') if t.strip()]
                
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)
        
        return instance

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image and not self.instance.pk:  # Only require image for new projects
            raise forms.ValidationError("A imagem é obrigatória.")
        return image