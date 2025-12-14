from rest_framework import serializers
from .models import Insumo, Pedido


class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

    
    def validate_total(self, value):
        if value <= 0:
            raise serializers.ValidationError("El total debe ser mayor que cero.")
        return value