
from django.contrib import admin
from django.urls import path, include
from mainApp import views
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter
from mainApp.views import InsumoViewSet, PedidoViewSet, PedidoFiltroAPIView

router = DefaultRouter()
router.register(r'insumos', InsumoViewSet, basename='insumo')
router.register(r'pedidos', InsumoViewSet, basename='pedido')

urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path("pedido/nuevo/", views.solicitar_pedido, name="solicitar_pedido"),
    path("pedido/seguimiento/<str:token>/", views.seguimiento_pedido, name="seguimiento_pedido"),
    path("pedido/personalizado/", views.pedido_personalizado, name="pedido_personalizado"),
    path('api/', include(router.urls)),
    path('api/pedidos-filtrar/', PedidoFiltroAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
