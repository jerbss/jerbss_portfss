from django.contrib import admin
from .models import Project, Tag, Contact, Top3Card

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

admin.site.register(Top3Card, Top3CardAdmin)
