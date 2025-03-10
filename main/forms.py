from django import forms
from .models import Project, Tag, Contact
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from cloudinary.forms import CloudinaryFileField

class ProjectForm(forms.ModelForm):
    # Replace standard ImageField with CloudinaryFileField with custom widget
    image = CloudinaryFileField(
        options={
            'folder': 'projects',
            'use_filename': True,
            'unique_filename': True,
            'overwrite': False,
        },
        required=False,
        label="Imagem do Projeto",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        }),
    )
    tags_input = forms.CharField(
        label='Tags',
        required=False,
        help_text='Adicione até 7 tags separadas por vírgula.',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: python, django, web'
        })
    )
    
    class Meta:
        model = Project
        fields = [
            'image',             # Required
            'title',            # Required
            'short_description', # Required
            'project_type',     # Required
            'collaboration',    # Adicionado o novo campo
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
            'collaboration': forms.Select(attrs={
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
            'collaboration': 'Tipo de Colaboração *',  # Adicionar label
            'start_date': 'Data de Início *',
            'url': 'Link Externo *',
            'content': 'Conteúdo do Projeto *',
            'end_date': 'Data de Conclusão',
            'github_url': 'Link do GitHub',
            'status': 'Status do Projeto',
            'featured': 'Projeto Destacado'
        }
    
    def __init__(self, *args, project=None, **kwargs):
        """
        Inicializa o formulário, permitindo carregar dados do rascunho se existir
        """
        instance = kwargs.get('instance')
        
        # Se um projeto foi fornecido e tem rascunho, use os dados do rascunho
        if instance and hasattr(instance, 'draft') and instance.draft:
            draft = instance.draft
            initial = kwargs.get('initial', {})
            
            # Preenche os dados iniciais com os valores do rascunho
            initial.update({
                'title': draft.title,
                'short_description': draft.short_description,
                'content': draft.content,
                'status': draft.status,
                'project_type': draft.project_type,
                'collaboration': draft.collaboration,
                'start_date': draft.start_date,
                'end_date': draft.end_date,
                'url': draft.url,
                'github_url': draft.github_url,
                'featured': draft.featured,
            })
            
            # Adiciona um indicador de que estamos carregando dados de um rascunho
            kwargs['initial'] = initial
            self.has_draft = True
        else:
            self.has_draft = False
        
        super().__init__(*args, **kwargs)
        
        # Inicializar tags_input com as tags existentes
        if self.instance.pk:
            self.fields['tags_input'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
            # Não mostrar que a imagem é obrigatória na edição
            self.fields['image'].label = "Alterar Imagem (opcional)"
    
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
            if len(tag_list) > 7:  # Atualizado de 3 para 7
                raise ValidationError('Máximo de 7 tags permitidas.')
            if len(tag_list) == 0:
                raise ValidationError('Pelo menos uma tag é necessária.')
        return tags

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']