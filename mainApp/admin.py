from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Categoria, Producto, Insumo, Pedido, PedidoImagen
from django.utils.html import format_html

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio_base", "destacado", "activo","oferta","vista_imagen_1","vista_imagen_2","vista_imagen_3",)
    list_filter = ("categoria", "destacado", "activo")
    search_fields = ("nombre", "descripcion")
    
    def vista_imagen_1(self, obj):
        if obj.imagen_1:
            return format_html('<img src="{}" width="100" height="100" />', obj.imagen_1.url)
        return "No Image"
    def vista_imagen_2(self, obj):
        if obj.imagen_2:
            return format_html('<img src="{}" width="100" height="100" />', obj.imagen_2.url)
        return "No Image"
    def vista_imagen_3(self, obj):
        if obj.imagen_3:
            return format_html('<img src="{}" width="100" height="100" />', obj.imagen_3.url)
        return "No Image"

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ("nombre","tipo","marca","color","cantidad_disponible","unidad",)
    list_filter = ("tipo", "marca", "color")
    search_fields = ("nombre", "marca", "color")


class PedidoImagenInline(admin.TabularInline):
    model = PedidoImagen
    extra = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("codigo_publico","cliente_nombre","producto_referencia","estado","estado_pago","plataforma_origen","fecha_solicitada","fecha_creacion",)
    list_filter = ("estado","estado_pago","plataforma_origen","fecha_creacion","fecha_solicitada",)
    search_fields = ("cliente_nombre","cliente_email","cliente_telefono","cliente_red_social","token_seguimiento",)
    readonly_fields = ("token_seguimiento",)
    inlines = [PedidoImagenInline]

    fieldsets = (
        ("Datos del cliente", {
            "fields": (
                "cliente_nombre",
                ("cliente_email", "cliente_telefono"),
                "cliente_red_social",
            )
        }),
        ("Detalles del pedido", {
            "fields": (
                "producto_referencia",
                "descripcion",
                "fecha_solicitada",
            )
        }),
        ("Origen y seguimiento", {
            "fields": (
                "plataforma_origen",
                "plataforma_otro",
                "token_seguimiento",
                "fecha_creacion",
                "fecha_actualizacion",
            )
        }),
        ("Estado y pago", {
            "fields": (
                "estado",
                ("estado_pago", "total", "monto_pagado"),
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.estado == "finalizada" and obj.estado_pago != "pagado":
            raise ValidationError(
                "No puedes finalizar el pedido si el estado de pago no es 'Pagado'"
            )
        super().save_model(request, obj, form, change)
