from django import forms

from .models import PrestamoSolicitud, ValeSolicitud


class ValeSolicitudForm(forms.ModelForm):
    class Meta:
        model = ValeSolicitud
        fields = ['monto', 'motivo', 'observaciones']
        widgets = {
            'monto': forms.Select(attrs={'required': True}),
            'motivo': forms.Select(attrs={'required': True}),
            'observaciones': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Podés agregar información adicional'}),
        }
        labels = {
            'monto': 'Monto del vale',
            'motivo': 'Motivo del vale',
            'observaciones': 'Observaciones',
        }


class PrestamoSolicitudForm(forms.ModelForm):
    class Meta:
        model = PrestamoSolicitud
        fields = ['monto', 'plazo_meses', 'destino', 'detalle']
        widgets = {
            'monto': forms.NumberInput(attrs={'min': '1', 'step': '0.01', 'placeholder': '0,00'}),
            'plazo_meses': forms.Select(attrs={'required': True}),
            'destino': forms.Select(attrs={'required': True}),
            'detalle': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Contanos brevemente para qué lo necesitás'}),
        }
        labels = {
            'monto': 'Monto solicitado',
            'plazo_meses': 'Plazo estimado',
            'destino': 'Destino del préstamo',
            'detalle': 'Detalle del pedido',
        }