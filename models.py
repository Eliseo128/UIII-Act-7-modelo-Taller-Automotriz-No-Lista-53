from django.db import models


class ClienteTaller(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    dni = models.CharField(max_length=15)
    fecha_registro = models.DateField()
    preferencias_contacto = models.CharField(max_length=50)
    historial_vehiculos = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Vehiculo(models.Model):
    placa = models.CharField(max_length=20)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano_fabricacion = models.IntegerField()
    color = models.CharField(max_length=30)
    numero_chasis = models.CharField(max_length=100)
    cliente = models.ForeignKey(ClienteTaller, on_delete=models.CASCADE, related_name="vehiculos")
    kilometraje_actual = models.IntegerField()
    tipo_combustible = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"


class Mecanico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    licencia_mecanico = models.CharField(max_length=50)
    fecha_contratacion = models.DateField()
    salario_hora = models.DecimalField(max_digits=8, decimal_places=2)
    turno_trabajo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class OrdenServicio(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="ordenes_servicio")
    mecanico = models.ForeignKey(Mecanico, on_delete=models.SET_NULL, null=True, related_name="ordenes")
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()
    problema_reportado = models.TextField()
    diagnostico_inicial = models.TextField()
    estado_orden = models.CharField(max_length=50)
    prioridad = models.CharField(max_length=50)
    kilometraje_ingreso = models.IntegerField()

    def __str__(self):
        return f"Orden #{self.id} - {self.vehiculo.placa}"


class ServicioTaller(models.Model):
    nombre_servicio = models.CharField(max_length=100)
    descripcion = models.TextField()
    tiempo_estimado_horas = models.DecimalField(max_digits=4, decimal_places=2)
    costo_mano_obra = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_servicio = models.CharField(max_length=50)
    garantia_meses = models.IntegerField()
    requerimientos_especiales = models.TextField()

    def __str__(self):
        return self.nombre_servicio


class Repuesto(models.Model):
    nombre_repuesto = models.CharField(max_length=255)
    descripcion = models.TextField()
    marca_compatible = models.CharField(max_length=50)
    modelo_compatible = models.CharField(max_length=50)
    stock_actual = models.IntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.CharField(max_length=100)
    numero_parte = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_repuesto


class FacturaTaller(models.Model):
    orden = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE, related_name="facturas")
    fecha_emision = models.DateField()
    subtotal_repuestos = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_mano_obra = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length=50)
    observaciones_finales = models.TextField()

    def __str__(self):
        return f"Factura #{self.id} - Orden {self.orden.id}"

