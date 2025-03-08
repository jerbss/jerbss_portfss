#!/bin/bash

# Script de build para Railway
echo "Running build.sh..."

# Criar diretório para arquivos estáticos se não existir
mkdir -p staticfiles

# Coletar arquivos estáticos
python manage.py collectstatic --noinput --no-post-process

# Criar diretório para arquivos de mídia dentro de staticfiles
mkdir -p staticfiles/media

# Copiar arquivos de mídia para o diretório de arquivos estáticos
if [ -d "media" ]; then
  cp -r media/* staticfiles/media/
  echo "Media files copied to staticfiles/media/"
else
  echo "No media directory found"
fi

# Listar diretórios para verificar se foram criados
echo "Directory structure:"
ls -la
echo "Static files directory:"
ls -la staticfiles/

echo "Build completed!"
