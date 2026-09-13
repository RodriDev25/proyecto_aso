from django.contrib import admin

from .models import PrestamoSolicitud, ValeSolicitud


@admin.register(ValeSolicitud)
class ValeSolicitudAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'monto', 'motivo', 'estado', 'creado_en')
	list_filter = ('estado', 'monto', 'motivo')
	search_fields = ('usuario__email', 'usuario__username')


@admin.register(PrestamoSolicitud)
class PrestamoSolicitudAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'monto', 'plazo_meses', 'destino', 'estado', 'creado_en')
	list_filter = ('estado', 'plazo_meses', 'destino')
	search_fields = ('usuario__email', 'usuario__username')
