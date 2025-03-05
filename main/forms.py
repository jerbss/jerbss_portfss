from django import forms
from .models import Project, Tag
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class ProjectForm(forms.ModelForm):
    tags_input = forms.CharField(
        label='Tags *',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Separe as tags por vírgula (máximo 3)'
        }),
        help_text='Separe as tags por vírgula (ex.: django, python, web). Máximo 3 tags.'
    )
    
    class Meta:
        model = Project
        fields = [
            'image',             # Required
            'title',            # Required
            'short_description', # Required
            'project_type',     # Required
            'start_date',       # Required
            'url',              # Required
            'tags_input',       # Required, max 3
            'content',          # Required
            'end_date',         # Optional
            'github_url',       # Optional
            'status',           # Optional
            'featured'          # Optional
        ]
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                # Remover o "required": True para permitir edição sem re-upload
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Digite o título do projeto'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': 200,
                'required': True,
                'placeholder': 'Breve descrição do projeto (máximo 200 caracteres)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'https://...'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'image': 'Foto do Projeto *',
            'title': 'Título do Projeto *',
            'short_description': 'Breve Descrição *',
            'project_type': 'Tipo de Projeto *',
            'start_date': 'Data de Início *',
            'url': 'Link Externo *',
            'content': 'Conteúdo do Projeto *',
            'end_date': 'Data de Conclusão',
            'github_url': 'Link do GitHub',
            'status': 'Status do Projeto',
            'featured': 'Projeto Destacado'
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
        # Só exige a imagem se for um novo projeto (self.instance.pk está vazio)
        if not image and not self.instance.pk:
            raise forms.ValidationError("A imagem é obrigatória para novos projetos.")
        return image

    def clean_tags_input(self):
        tags = self.cleaned_data.get('tags_input')
        if tags:
            tag_list = [t.strip() for t in tags.split(',') if t.strip()]
            if len(tag_list) > 3:
                raise ValidationError('Máximo de 3 tags permitidas.')
            if len(tag_list) == 0:
                raise ValidationError('Pelo menos uma tag é necessária.')
        return tags

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome'
        })
    )
    email = forms.EmailField(
        label='Seu e-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@exemplo.com'
        })
    )
    message = forms.CharField(
        label='Mensagem',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Digite sua mensagem'
        })
    )