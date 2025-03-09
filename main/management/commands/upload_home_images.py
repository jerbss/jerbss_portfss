from django.core.management.base import BaseCommand
import cloudinary
import cloudinary.uploader
import os
from django.conf import settings
import json

class Command(BaseCommand):
    help = 'Upload all home page images to Cloudinary and generate URLs for them'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando upload das imagens da home page para o Cloudinary...')
        
        # Pasta das imagens estáticas
        image_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        
        # Lista de imagens usadas na home page
        home_images = [
            'profile_photo_1.png',
            'rato.jpg',
            'capivara.jpeg',
            'cavalo.jpeg',
            'cerveja.png',
            'cocacola.png',
            'cafe.png',
            'o_irlandes.png',
            'madmax.jpeg',
            'wallstreet.jpeg',
            'twice.jpg',
            'safadao.jpg',
            'anri.jpg'
        ]
        
        # Dicionário para armazenar as URLs do Cloudinary
        image_urls = {}
        
        uploaded_count = 0
        for image_name in home_images:
            image_path = os.path.join(image_dir, image_name)
            
            if os.path.exists(image_path):
                try:
                    self.stdout.write(f"Fazendo upload de {image_name} para o Cloudinary...")
                    
                    # Fazer o upload para o Cloudinary na pasta 'home'
                    result = cloudinary.uploader.upload(
                        image_path,
                        folder="home",
                        public_id=os.path.splitext(image_name)[0],
                        overwrite=True
                    )
                    
                    # Armazenar a URL no dicionário
                    image_urls[image_name] = result['secure_url']
                    
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ {image_name} enviada com sucesso: {result['secure_url']}"
                    ))
                    uploaded_count += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"✗ Erro ao enviar {image_name}: {str(e)}"
                    ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"⚠ Imagem {image_name} não encontrada em {image_path}"
                ))
        
        # Salvar as URLs em um arquivo JSON para referência
        urls_file = os.path.join(settings.BASE_DIR, 'main', 'templates', 'main', 'home_image_urls.json')
        with open(urls_file, 'w') as f:
            json.dump(image_urls, f, indent=4)
        
        # Gerar um template context processor para uso fácil nos templates
        context_processor_file = os.path.join(settings.BASE_DIR, 'main', 'templatetags', 'cloudinary_images.py')
        
        # Garantir que o diretório templatetags exista
        os.makedirs(os.path.dirname(context_processor_file), exist_ok=True)
        
        # Criar arquivo __init__.py se não existir
        init_file = os.path.join(settings.BASE_DIR, 'main', 'templatetags', '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Pacote para template tags personalizadas\n')
        
        # Escrever o arquivo de template tag
        with open(context_processor_file, 'w') as f:
            f.write('''
from django import template
import json
import os
from django.conf import settings

register = template.Library()

# Carrega as URLs das imagens do arquivo JSON
try:
    with open(os.path.join(settings.BASE_DIR, 'main', 'templates', 'main', 'home_image_urls.json'), 'r') as f:
        IMAGE_URLS = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    IMAGE_URLS = {}

@register.simple_tag
def home_image_url(image_name):
    """
    Retorna a URL do Cloudinary para a imagem da home page.
    Se a imagem não estiver no mapeamento, retorna o caminho estático padrão.
    
    Uso: {% home_image_url "rato.jpg" %}
    """
    if image_name in IMAGE_URLS:
        return IMAGE_URLS[image_name]
    return f"/static/images/{image_name}"
''')
        
        self.stdout.write(self.style.SUCCESS(
            f"Upload concluído! {uploaded_count} de {len(home_images)} imagens foram enviadas para o Cloudinary."
        ))
        self.stdout.write(f"URLs salvas em: {urls_file}")
        self.stdout.write(f"Template tag criada em: {context_processor_file}")
        self.stdout.write("\nPara usar estas imagens, substitua as referências no template home.html por:")
        self.stdout.write("{% load cloudinary_images %}")
        self.stdout.write("{% home_image_url 'nome_da_imagem.jpg' %}")
