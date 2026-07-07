from django.contrib import admin
from .models import Analise
from django.utils.html import format_html


class AnaliseAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'ver_imagem')

    def ver_imagem(self, obj):
        try:
            return format_html('<img src="{}" width="100" />', obj.amostra.imagem.url)
        except:
            return "SEM IMG"
admin.site.register(Analise, AnaliseAdmin)