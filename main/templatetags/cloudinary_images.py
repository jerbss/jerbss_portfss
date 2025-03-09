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
    Returns the Cloudinary URL for a home page image.
    If the image is not in the mapping, returns the default static path.
    
    Usage: {% home_image_url "rato.jpg" %}
    """
    if image_name in IMAGE_URLS:
        return IMAGE_URLS[image_name]
    return f"/static/images/{image_name}"
