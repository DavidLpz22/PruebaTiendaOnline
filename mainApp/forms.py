from django import forms
from .models import Pedido, PedidoImagen


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class PedidoForm(forms.ModelForm):
    imagenes = forms.FileField(
        widget=MultipleFileInput(),
        required=False,
        label="Subir imágenes de referencia"
    )

    class Meta:
        model = Pedido
        fields = [
            "cliente_nombre",
            "cliente_email",
            "cliente_telefono",
            "cliente_red_social",
            "producto_referencia",
            "descripcion",
            "fecha_solicitada",
            "plataforma_origen",
        ]
        widgets = {
            "fecha_solicitada": forms.DateInput(attrs={"type": "date"}),
        }

class ReporteFiltroForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    estados = forms.MultipleChoiceField(
        required=False,
        choices=Pedido.ESTADO_PEDIDO_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    plataformas = forms.MultipleChoiceField(
        required=False,
        choices=Pedido.PLATAFORMA_ORIGEN_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    limite = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=500,
        initial=50
    )