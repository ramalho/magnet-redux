# coding: utf-8

from django.contrib import admin

from .models import Noticia

class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['dt_criacao', 'publicado', 'destaque', 'secao', 'titulo']
    list_display_links = ['secao', 'titulo']
    list_editable = ['destaque']
    search_fields = ['titulo', 'resumo', 'corpo']
    list_filter = ['secao', 'destaque']
    date_hierarchy = 'dt_criacao'

admin.site.register(Noticia, NoticiaAdmin)
