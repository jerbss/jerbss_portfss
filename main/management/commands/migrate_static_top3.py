from django.core.management.base import BaseCommand
from main.models import Top3Card
import requests
from cloudinary import uploader
import tempfile
import os

class Command(BaseCommand):
    help = 'Migra os cards TOP 3 estáticos (Animais, Bebidas, Filmes e Artistas) para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a criação de cards mesmo se já existirem',
        )
        parser.add_argument(
            '--ignore-errors',
            action='store_true',
            help='Continua criando cards mesmo se algumas imagens falharem',
        )

    def handle(self, *args, **options):
        # Verificar se os cards já existem
        existing_titles = Top3Card.objects.values_list('title', flat=True)
        force = options.get('force', False)
        ignore_errors = options.get('ignore_errors', False)
        
        # URLs públicas confiáveis para cada imagem - usando Unsplash e imagens de placeholder
        image_urls = {
            # Animais
            'rato': 'https://images.unsplash.com/photo-1618858218608-229fa6ffbb24?w=600',
            'capivara': 'https://images.unsplash.com/photo-1598439210625-5067c578f3f6?w=600',
            'cavalo': 'https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=600',
            
            # Bebidas
            'cerveja': 'https://images.unsplash.com/photo-1567696911980-2c620dbd5060?w=600',
            'cocacola': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=600',
            'cafe': 'https://images.unsplash.com/photo-1497515114629-f71d768fd07c?w=600',
            
            # Filmes
            'o_irlandes': 'https://m.media-amazon.com/images/M/MV5BMGUyM2ZiZmUtMWY0OC00NTQ4LThkOGUtNjY2NjkzMDJiMWMwXkEyXkFqcGdeQXVyMzY0MTE3NzU@._V1_FMjpg_UX600_.jpg',
            'madmax': 'https://m.media-amazon.com/images/M/MV5BN2EwM2I5OWMtMGQyMi00Zjg1LWJkNTctZTdjYTA4OGUwZjMyXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX600_.jpg',
            'wallstreet': 'https://m.media-amazon.com/images/M/MV5BNDIwMDIxNzk3Ml5BMl5BanBnXkFtZTgwMTg0MzQ2MDE@._V1_FMjpg_UX600_.jpg',
            
            # Artistas
            'twice': 'https://upload.wikimedia.org/wikipedia/commons/7/7f/TWICE_in_September_2022.jpg',
            'safadao': 'https://upload.wikimedia.org/wikipedia/commons/1/11/Wesley_Safad%C3%A3o_em_fev.2018.jpg',
            'anri': 'https://upload.wikimedia.org/wikipedia/commons/1/12/Anri_Sugihara_at_Tokyo_Auto_Salon_2012.jpg',

            # Fallbacks gerais para cada categoria
            'fallback_animal': 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=600',
            'fallback_bebida': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=600',
            'fallback_filme': 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600',
            'fallback_artista': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600'
        }

        # Definição dos cards estáticos
        static_cards = [
            {
                'title': 'Animais',
                'icon_class': 'fas fa-paw',
                'items': [
                    {
                        'name': 'Rato',
                        'image_key': 'rato',
                        'fallback_key': 'fallback_animal',
                        'link': None
                    },
                    {
                        'name': 'Capivara',
                        'image_key': 'capivara',
                        'fallback_key': 'fallback_animal',
                        'link': None
                    },
                    {
                        'name': 'Cavalo',
                        'image_key': 'cavalo',
                        'fallback_key': 'fallback_animal',
                        'link': None
                    }
                ],
                'fun_comment': 'O rato me mostra como deixar tudo no lugar 🐭, a capivara me ensina que descansar não é frescura 🦫🌿(Deveria existir emoji de Capivara) e o cavalo me dá aulas sobre correr solto e sem freio 🐎!'
            },
            {
                'title': 'Bebidas',
                'icon_class': 'fas fa-glass-cheers',
                'items': [
                    {
                        'name': 'Cerveja',
                        'image_key': 'cerveja',
                        'fallback_key': 'fallback_bebida',
                        'link': None
                    },
                    {
                        'name': 'Coca-Cola',
                        'image_key': 'cocacola',
                        'fallback_key': 'fallback_bebida',
                        'link': None
                    },
                    {
                        'name': 'Café',
                        'image_key': 'cafe',
                        'fallback_key': 'fallback_bebida',
                        'link': None
                    }
                ],
                'fun_comment': 'Café: a razão de eu ainda estar de pé (na verdade já estou imune aos efeitos do café) ☕; Coca-Cola: a explosão de refrescância quando o calor me pega 🥤; e Cerveja: o \'tch\'(Tentei simular a latinha abrindo) que dá início à diversão 🍺!'
            },
            {
                'title': 'Filmes',
                'icon_class': 'fas fa-film',
                'items': [
                    {
                        'name': 'O Irlandês',
                        'image_key': 'o_irlandes',
                        'fallback_key': 'fallback_filme',
                        'link': 'https://www.imdb.com/pt/title/tt1302006/?ref_=ext_shr_lnk'
                    },
                    {
                        'name': 'Mad Max: Estrada da Fúria',
                        'image_key': 'madmax',
                        'fallback_key': 'fallback_filme',
                        'link': 'https://www.imdb.com/pt/title/tt1392190/?ref_=ext_shr_lnk'
                    },
                    {
                        'name': 'O Lobo de Wall Street',
                        'image_key': 'wallstreet',
                        'fallback_key': 'fallback_filme',
                        'link': 'https://www.imdb.com/pt/title/tt0993846/?ref_=ext_shr_lnk'
                    }
                ],
                'fun_comment': 'Com Scorsese no comando, até o deserto de Mad Max tem cheiro de máfia italiana! 🍷🌪️'
            },
            {
                'title': 'Artistas',
                'icon_class': 'fas fa-music',
                'items': [
                    {
                        'name': 'TWICE',
                        'image_key': 'twice',
                        'fallback_key': 'fallback_artista',
                        'link': 'https://open.spotify.com/intl-pt/artist/7n2Ycct7Beij7Dj7meI4X0?si=QSiHYw83SzitxPlsvUkkbg'
                    },
                    {
                        'name': 'Wesley Safadão',
                        'image_key': 'safadao',
                        'fallback_key': 'fallback_artista',
                        'link': 'https://open.spotify.com/intl-pt/artist/1AL2GKpmRrKXkYIcASuRFa?si=i777P_PVSr28B9MgKTvWZQ'
                    },
                    {
                        'name': 'ANRI',
                        'image_key': 'anri',
                        'fallback_key': 'fallback_artista',
                        'link': 'https://open.spotify.com/intl-pt/artist/0xGtOrmB2hnrNRLG3vhpSo?si=dQlFWdRkSYqNp8hDqB5hGA'
                    }
                ],
                'fun_comment': 'TWICE, Safadão e ANRI: uma mistura muito louca de idiomas, gêneros e estilos, mas o clima é sempre o mesmo: sol, praia e aquele som de verão que não sai da cabeça! 😎🏖️🎶'
            }
        ]
        
        created_count = 0
        skipped_count = 0
        
        # Uma última URL de fallback genérica, caso tudo falhe
        ultimate_fallback = 'https://placehold.co/600x600/cccccc/333333?text=Imagem+Indisponivel'
        
        # Importe cada card estático
        for card_data in static_cards:
            # Verifique se o cartão já existe e decida se vai pular ou não
            if card_data['title'] in existing_titles and not force:
                self.stdout.write(self.style.WARNING(f"Card '{card_data['title']}' já existe. Pulando... (use --force para sobrescrever)"))
                skipped_count += 1
                continue
            elif card_data['title'] in existing_titles and force:
                Top3Card.objects.filter(title=card_data['title']).delete()
                self.stdout.write(self.style.WARNING(f"Card '{card_data['title']}' excluído para ser recriado."))
                
            # Crie um novo Top3Card
            try:
                # Primeiro configure a estrutura básica do card
                card = Top3Card(
                    title=card_data['title'],
                    icon_class=card_data['icon_class'],
                    item1_name=card_data['items'][0]['name'],
                    item1_link=card_data['items'][0]['link'],
                    item2_name=card_data['items'][1]['name'],
                    item2_link=card_data['items'][1]['link'],
                    item3_name=card_data['items'][2]['name'],
                    item3_link=card_data['items'][2]['link'],
                    fun_comment=card_data['fun_comment'],
                    display_order=created_count
                )
                
                # Processar e fazer upload de imagens para o Cloudinary
                success = True
                
                # Item 1
                try:
                    self.stdout.write(f"Processando item 1 '{card_data['items'][0]['name']}' para '{card_data['title']}'...")
                    image_key = card_data['items'][0]['image_key']
                    fallback_key = card_data['items'][0]['fallback_key']
                    
                    # Tentar fazer upload da imagem, com várias opções de fallback
                    card.item1_image = self.upload_image_with_fallbacks(
                        primary_url=image_urls[image_key],
                        fallback_url=image_urls[fallback_key],
                        ultimate_fallback_url=ultimate_fallback,
                        public_id=f"{card_data['title']}_item1_{image_key}"
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao processar imagem 1: {str(e)}"))
                    if not ignore_errors:
                        success = False
                    else:
                        # Tentar usar fallback final
                        try:
                            card.item1_image = self.upload_image_to_cloudinary(
                                ultimate_fallback, 
                                f"{card_data['title']}_item1_fallback"
                            )
                            self.stdout.write(self.style.WARNING(f"Usando imagem de fallback final para item 1"))
                        except:
                            success = False
                
                # Item 2
                if success or ignore_errors:
                    try:
                        self.stdout.write(f"Processando item 2 '{card_data['items'][1]['name']}' para '{card_data['title']}'...")
                        image_key = card_data['items'][1]['image_key']
                        fallback_key = card_data['items'][1]['fallback_key']
                        
                        card.item2_image = self.upload_image_with_fallbacks(
                            primary_url=image_urls[image_key],
                            fallback_url=image_urls[fallback_key],
                            ultimate_fallback_url=ultimate_fallback,
                            public_id=f"{card_data['title']}_item2_{image_key}"
                        )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erro ao processar imagem 2: {str(e)}"))
                        if not ignore_errors:
                            success = False
                        else:
                            # Tentar usar fallback final
                            try:
                                card.item2_image = self.upload_image_to_cloudinary(
                                    ultimate_fallback, 
                                    f"{card_data['title']}_item2_fallback"
                                )
                                self.stdout.write(self.style.WARNING(f"Usando imagem de fallback final para item 2"))
                            except:
                                success = False
                
                # Item 3
                if success or ignore_errors:
                    try:
                        self.stdout.write(f"Processando item 3 '{card_data['items'][2]['name']}' para '{card_data['title']}'...")
                        image_key = card_data['items'][2]['image_key']
                        fallback_key = card_data['items'][2]['fallback_key']
                        
                        card.item3_image = self.upload_image_with_fallbacks(
                            primary_url=image_urls[image_key],
                            fallback_url=image_urls[fallback_key],
                            ultimate_fallback_url=ultimate_fallback,
                            public_id=f"{card_data['title']}_item3_{image_key}"
                        )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erro ao processar imagem 3: {str(e)}"))
                        if not ignore_errors:
                            success = False
                        else:
                            # Tentar usar fallback final
                            try:
                                card.item3_image = self.upload_image_to_cloudinary(
                                    ultimate_fallback, 
                                    f"{card_data['title']}_item3_fallback"
                                )
                                self.stdout.write(self.style.WARNING(f"Usando imagem de fallback final para item 3"))
                            except:
                                success = False
                
                if not success and not ignore_errors:
                    self.stdout.write(self.style.ERROR(f"Falha ao criar card '{card_data['title']}' devido a erro nas imagens"))
                    continue
                elif not success and ignore_errors:
                    self.stdout.write(self.style.WARNING(f"Algumas imagens falharam para '{card_data['title']}', mas continuando mesmo assim"))
                
                # Salvar o card
                card.save()
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Card '{card_data['title']}' criado com sucesso."))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao criar card '{card_data['title']}': {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS(f"Migração concluída. {created_count} cards criados, {skipped_count} ignorados."))
    
    def upload_image_with_fallbacks(self, primary_url, fallback_url, ultimate_fallback_url, public_id):
        """Tenta fazer upload de uma imagem, com opções de fallback se falhar"""
        try:
            # Primeira tentativa: URL principal
            return self.upload_image_to_cloudinary(primary_url, public_id)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Falha na URL primária, tentando fallback: {str(e)}"))
            try:
                # Segunda tentativa: URL de fallback 
                return self.upload_image_to_cloudinary(fallback_url, public_id)
            except Exception as e2:
                self.stdout.write(self.style.WARNING(f"Falha na URL de fallback, usando fallback final: {str(e2)}"))
                # Última tentativa: URL de fallback final
                return self.upload_image_to_cloudinary(ultimate_fallback_url, public_id)
    
    def upload_image_to_cloudinary(self, image_url, public_id):
        """Upload de uma imagem da web para o Cloudinary"""
        self.stdout.write(f"Baixando imagem de {image_url}...")
        
        try:
            # Baixar a imagem da web
            response = requests.get(image_url, timeout=10)
            if response.status_code != 200:
                raise Exception(f"Falha ao baixar imagem: Status {response.status_code}")
            
            # Salvar temporariamente
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
            
            # Upload para o Cloudinary
            self.stdout.write(f"Fazendo upload para o Cloudinary com ID {public_id}...")
            upload_result = uploader.upload(temp_file_path, public_id=public_id)
            os.unlink(temp_file_path)  # Remover arquivo temporário
            
            self.stdout.write(self.style.SUCCESS(f"Imagem obtida e enviada com sucesso: {public_id}"))
            return upload_result['public_id']
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao processar imagem {image_url}: {str(e)}"))
            raise
