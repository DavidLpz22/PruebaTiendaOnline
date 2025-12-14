from django.shortcuts import render, redirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from mainApp.models import Categoria, Producto, Pedido, PedidoImagen, Insumo
from django.http import Http404
from django.utils import timezone

from rest_framework import viewsets, mixins
from .serializers import InsumoSerializer, PedidoSerializer


# Create your views here.

def home(request):
    q = request.GET.get('q', '').strip()
    cat = request.GET.get('cat', '').strip()

    ver_ofertas = request.GET.get('ofertas', '').strip()
    ver_destacados = request.GET.get('destacados', '').strip()

    productos = Producto.objects.filter(activo=True)

    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q)
        )

    if cat:
        productos = productos.filter(categoria__id=cat)

    productos_destacados = Producto.objects.filter(destacado=True, activo=True)

    productos_oferta = Producto.objects.filter(oferta=True, activo=True)

    if ver_destacados:
        productos = productos_destacados

    if ver_ofertas:
        productos = productos_oferta

    return render(request, 'home.html', {
        'productos': productos,
        'destacados': productos_destacados,
        'ofertas': productos_oferta,
        'ver_destacados': ver_destacados,
        'ver_ofertas': ver_ofertas,
        'q': q,
        'cat': cat,
        'categorias': Categoria.objects.all(),
    })


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id, activo=True)

    data = {
        'producto': producto,
    }

    return render(request, 'detalle_producto.html', data)  

def solicitar_pedido(request):

    producto_id = request.GET.get("producto")
    producto_seleccionado = None

    if producto_id:
        try:
            producto_seleccionado = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            producto_seleccionado = None

    if request.method == "POST":
        nombre = request.POST.get("cliente_nombre")
        email = request.POST.get("cliente_email", "")
        telefono = request.POST.get("cliente_telefono", "")
        red_social = request.POST.get("cliente_red_social", "")
        producto_ref = request.POST.get("producto_referencia")
        descripcion = request.POST.get("descripcion")
        fecha_solicitada = request.POST.get("fecha_solicitada")

        pedido = Pedido.objects.create(
            cliente_nombre=nombre,
            cliente_email=email,
            cliente_telefono=telefono,
            cliente_red_social=red_social,
            descripcion=descripcion,
            fecha_solicitada=fecha_solicitada if fecha_solicitada else None,
            fecha_creacion=timezone.now().date(),
            fecha_actualizacion=timezone.now().date(),
            plataforma_origen="sitio_web",
            estado="solicitado",
            estado_pago="pendiente",
            producto_referencia=Producto.objects.get(id=producto_ref) if producto_ref else None
        )

        
        imagenes = request.FILES.getlist("imagenes")
        for img in imagenes:
            PedidoImagen.objects.create(
                pedido=pedido,
                imagen=img
            )

        url_seguimiento = request.build_absolute_uri(
            f"/pedido/seguimiento/{pedido.token_seguimiento}/"
        )   

        return render(
            request,
            "pedido_creado.html",
            {"pedido": pedido, "url_seguimiento": url_seguimiento}
        )

    return render(request, "crear_pedido.html", { 
        "productos": Producto.objects.all(),
        "producto_seleccionado": producto_seleccionado
    })

def seguimiento_pedido(request, token):
    try:
        pedido = Pedido.objects.get(token_seguimiento=token)
    except Pedido.DoesNotExist:
        raise Http404("No existe un pedido con este código.")

    return render(request, "seguimiento.html", {
        "pedido": pedido,
        "imagenes": pedido.imagenes.all()
    })

def pedido_personalizado(request):
    if request.method == "POST":
        pedido = Pedido.objects.create(
            cliente_nombre = request.POST.get("cliente_nombre"),
            cliente_email = request.POST.get("cliente_email"),
            cliente_telefono = request.POST.get("cliente_telefono"),
            cliente_red_social = request.POST.get("cliente_red_social"),
            descripcion = request.POST.get("descripcion"),
            fecha_solicitada = request.POST.get("fecha_solicitada") or None,
            producto_referencia = None,
            plataforma_origen = "sitio_web",
            estado = "solicitado",
            estado_pago = "pendiente",
        )
        for img in request.FILES.getlist("imagenes"):
            PedidoImagen.objects.create(
                pedido=pedido,
                imagen=img
            )
        return redirect("pedido_creado", token=pedido.token_seguimiento)
    return render(request, "pedido_personalizado.html")

class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

class PedidoViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer



