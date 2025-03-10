from django.utils import timezone
from datetime import timedelta
from .models import Visitor
import logging

logger = logging.getLogger(__name__)

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Processamos a visita apenas após a resposta ser gerada
        response = self.get_response(request)
        
        # Não rastreamos requisições AJAX, favicon, admin ou estáticas
        if request.path.startswith('/admin/') or \
           request.path.startswith('/static/') or \
           request.path.startswith('/media/') or \
           'favicon' in request.path.lower() or \
           self.is_ajax_request(request):  # Substituindo is_ajax() por um método personalizado
            return response
            
        # Rastrear visita
        try:
            # Obter o endereço IP real (considerando proxy)
            ip_address = self.get_client_ip(request)
            
            # Obter o user-agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            
            # Verificar se este IP já visitou este caminho nas últimas 24 horas
            one_day_ago = timezone.now() - timedelta(days=1)
            visitor, created = Visitor.objects.get_or_create(
                ip_address=ip_address,
                path=request.path,
                defaults={
                    'user_agent': user_agent
                }
            )
            
            # Se o visitante já existir, atualizamos os dados
            if not created:
                visitor.visit_count += 1
                visitor.last_visit = timezone.now()
                visitor.save()
            
        except Exception as e:
            # Log de erro, mas não interrompe a requisição
            logger.error(f"Erro ao rastrear visitante: {str(e)}")
            
        return response
    
    def get_client_ip(self, request):
        """Extrai o IP real do cliente, mesmo com proxies"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # X-Forwarded-For pode ter vários IPs, pegamos o primeiro
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_ajax_request(self, request):
        """
        Verifica se uma solicitação é AJAX examinando o cabeçalho HTTP X-Requested-With.
        Substitui o método obsoleto request.is_ajax()
        """
        return request.headers.get('X-Requested-With') == 'XMLHttpRequest'
