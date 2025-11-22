from django import forms
from .models import Pedido, PedidoImagen

class PedidoForm(forms.ModelForm):
    imagenes = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
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
        ]
        widgets = {
            "fecha_solicitada": forms.DateInput(attrs={"type": "date"}),
        }
