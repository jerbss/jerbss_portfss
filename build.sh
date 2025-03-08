#!/bin/bash

# Script de build para Railway
echo "Running build.sh..."

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Criar diretório para arquivos de mídia dentro de staticfiles
mkdir -p staticfiles/media

# Copiar arquivos de mídia para o diretório de arquivos estáticos
if [ -d "media" ]; then
  cp -r media/* staticfiles/media/
fi

echo "Build completed!"
