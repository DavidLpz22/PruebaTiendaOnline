from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from mainApp.models import Categoria, Producto
# Create your views here.
def home(request):
    q = request.GET.get('q', '').strip()
    cat = request.GET.get('cat', '').strip()

    productos = Producto.objects.filter(activo=True)

    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q)
        )

    if cat:
        productos = productos.filter(categoria__id=cat)

    destacados = Producto.objects.filter(destacado=True, activo=True)

    data = {
        'productos': productos,
        'destacados': destacados,
        'q': q,
        'cat': cat,
        'categorias': Categoria.objects.all(),
    }

    return render(request, 'home.html', data)

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id, activo=True)

    data = {
        'producto': producto,
    }

    return render(request, 'detalle_producto.html', data)   