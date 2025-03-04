from django import forms
from .models import Project, Tag
from tinymce.widgets import TinyMCE
from django.utils.text import slugify

class ProjectForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={'cols': 80, 'rows': 30},
            mce_attrs={
                'menubar': 'file edit view insert format tools table help',
                'plugins': '''
                    advlist autolink lists link image charmap print preview anchor
                    searchreplace visualblocks code fullscreen
                    insertdatetime media table paste code help wordcount
                ''',
                'toolbar': '''
                    undo redo | formatselect | bold italic backcolor |
                    alignleft aligncenter alignright alignjustify |
                    bullist numlist outdent indent | removeformat | link image media | help |
                    code
                ''',
                'skin': 'oxide-dark',  # Dark theme for TinyMCE
                'content_css': 'dark',  # Dark theme for content
                'content_style': '''
                    body { background-color: #1a1a1a; color: #e1e1e1; }
                    a { color: #58a6ff; }
                ''',
            }
        ),
        required=False
    )
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
            'start_date',  # Add this
            'end_date',    # Add this
            'tags_input',
            'url',
            'github_url',
            'featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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