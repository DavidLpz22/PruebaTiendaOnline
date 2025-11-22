from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE,related_name="productos",verbose_name="Categoría",)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio_base = models.IntegerField()
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    imagen_1 = models.ImageField(upload_to='productos/',blank=True,null=True,)
    imagen_2 = models.ImageField(upload_to='productos/',blank=True,null=True,)
    imagen_3 = models.ImageField(upload_to='productos/',blank=True,null=True,)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Insumo(models.Model):
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=100, help_text="Ej: textil, cerámica, 3D, etc.")
    cantidad_disponible = models.PositiveIntegerField(default=0)
    unidad = models.CharField(max_length=50,blank=True,help_text="Ej: unidades, metros, kg",)
    marca = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        unidad_txt = f" {self.unidad}" if self.unidad else ""
        return f"{self.nombre} ({self.cantidad_disponible}{unidad_txt})"


class Pedido(models.Model):
    ESTADO_PEDIDO_CHOICES = (
        ("solicitado", "Solicitado"),
        ("aprobado", "Aprobado"),
        ("en_proceso", "En proceso"),
        ("realizada", "Realizada"),
        ("entregada", "Entregada"),
        ("finalizada", "Finalizada"),
        ("cancelada", "Cancelada"),
    )

    ESTADO_PAGO_CHOICES = (
        ("pendiente", "Pendiente"),
        ("parcial", "Parcial"),
        ("pagado", "Pagado"),
    )

    PLATAFORMA_ORIGEN_CHOICES = (
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("whatsapp", "WhatsApp"),
        ("presencial", "Presencial"),
        ("sitio_web", "Sitio web"),
        ("otro", "Otra plataforma"),
    )

    cliente_nombre = models.CharField(max_length=150)
    cliente_email = models.EmailField(blank=True)
    cliente_telefono = models.CharField(max_length=30, blank=True)
    cliente_red_social = models.CharField(max_length=150,blank=True,help_text="Opcional: @usuario de Instagram, Facebook, etc.",)

    producto_referencia = models.ForeignKey(Producto,on_delete=models.SET_NULL,null=True,blank=True)

    descripcion = models.TextField("Descripción de lo solicitado")

    fecha_solicitada = models.DateField(null=True,blank=True,help_text="Fecha en que necesita el producto",)

    plataforma_origen = models.CharField(max_length=20,choices=PLATAFORMA_ORIGEN_CHOICES,default="sitio_web",)
    plataforma_otro = models.CharField(max_length=100,blank=True,help_text="Especificar",)

    estado = models.CharField(max_length=20,choices=ESTADO_PEDIDO_CHOICES,default="solicitado",)

    estado_pago = models.CharField(max_length=20,choices=ESTADO_PAGO_CHOICES,default="pendiente",)

    total = models.DecimalField(max_digits=10,decimal_places=2,default=0,)
    monto_pagado = models.DecimalField(max_digits=10,decimal_places=2,default=0,)

    token_seguimiento = models.CharField(max_length=20,unique=True,editable=False,blank=True,default="",)

    fecha_creacion = models.DateField()
    fecha_actualizacion = models.DateField()

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente_nombre}"

    def save(self, *args, **kwargs):
        creando = self.pk is None
        super(Pedido, self).save(*args, **kwargs)

        if creando and not self.token_seguimiento and self.id:
            self.token_seguimiento = "TKN%06d" % self.id
            super(Pedido, self).save(update_fields=["token_seguimiento"])

    @property
    def pagado_completo(self):
        return self.estado_pago == "pagado"

    @property
    def codigo_publico(self):
        return f"P-{self.id:06d}" if self.id else "Sin ID"


class PedidoImagen(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="imagenes",
        verbose_name="Pedido",
    )
    imagen = models.ImageField(upload_to="pedidos/",)
    descripcion = models.CharField(max_length=200,blank=True,)

    def __str__(self):
        return f"Imagen de {self.pedido}"
