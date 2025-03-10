from django.contrib import admin
from .models import Project, Tag, Contact, Top3Card
from django.db.models import Sum, Count
from django.utils.html import format_html
from .models import Visitor

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'project_type', 'start_date', 'created_at')
    list_filter = ('status', 'project_type', 'tags')
    search_fields = ('title', 'short_description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

class Top3CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'created_at')
    list_editable = ('display_order',)
    search_fields = ('title',)
    fieldsets = (
        ('Card Information', {
            'fields': ('icon_class', 'title', 'display_order')
        }),
        ('First Item', {
            'fields': ('item1_image', 'item1_name', 'item1_link')
        }),
        ('Second Item', {
            'fields': ('item2_image', 'item2_name', 'item2_link')
        }),
        ('Third Item', {
            'fields': ('item3_image', 'item3_name', 'item3_link')
        }),
        ('Additional Information', {
            'fields': ('fun_comment',)
        }),
    )

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'visit_count', 'last_visit', 'timestamp')
    list_filter = ('path', 'timestamp', 'last_visit')
    search_fields = ('ip_address', 'path', 'user_agent')
    date_hierarchy = 'timestamp'
    readonly_fields = ('ip_address', 'path', 'user_agent', 'visit_count', 'timestamp', 'last_visit')
    
    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        # Permitir excluir para limpar dados antigos se necessário
        return True
        
    def has_change_permission(self, request, obj=None):
        return False
        
    def changelist_view(self, request, extra_context=None):
        # Adicionar estatísticas resumidas ao topo da lista
        extra_context = extra_context or {}
        
        # Total de visitantes únicos (IPs)
        unique_visitors = Visitor.objects.values('ip_address').distinct().count()
        
        # Total de visitas
        total_visits = Visitor.objects.aggregate(total=Sum('visit_count'))['total'] or 0
        
        # Páginas mais visitadas
        top_pages = Visitor.objects.values('path').annotate(
            visits=Sum('visit_count')
        ).order_by('-visits')[:5]
        
        # Dias com mais visitas (últimos 30 dias)
        from django.db.models.functions import TruncDate
        
        daily_visits = Visitor.objects.annotate(
            visit_date=TruncDate('timestamp')
        ).values('visit_date').annotate(
            visits=Count('id')
        ).order_by('-visit_date')[:7]
        
        # Adicionar ao contexto
        extra_context['unique_visitors'] = unique_visitors
        extra_context['total_visits'] = total_visits
        extra_context['top_pages'] = top_pages
        extra_context['daily_visits'] = daily_visits
        
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Top3Card, Top3CardAdmin)
