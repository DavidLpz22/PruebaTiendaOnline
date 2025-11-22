
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)