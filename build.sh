#!/bin/bash

# Script de build para Railway
echo "Running build.sh..."

# Criar diretório para arquivos estáticos se não existir
mkdir -p staticfiles

# Coletar arquivos estáticos
python manage.py collectstatic --noinput --clear

# Criar diretório para arquivos de mídia dentro de staticfiles
mkdir -p staticfiles/media

# Copiar arquivos de mídia para o diretório de arquivos estáticos
if [ -d "media" ]; then
  echo "Copying media files..."
  cp -r media/* staticfiles/media/
else
  echo "Creating media directory and copying static images to media folder..."
  mkdir -p media
  # Copy images from static to media as a fallback
  if [ -d "static/images" ]; then
    cp -r static/images/* staticfiles/media/
  fi
fi

# Verificar se os diretórios foram criados
echo "Directory structure:"
ls -la
echo "Static files directory:"
ls -la staticfiles/
echo "Media directory:"
ls -la staticfiles/media/

# Definir permissões de leitura para todos os arquivos
chmod -R 755 staticfiles/

echo "Build completed!"
