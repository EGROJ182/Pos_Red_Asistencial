from django.db import models

# Create your models here.
class proveedores(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nit = models.IntegerField()
    nombre = models.CharField(max_length=250)
    tipo_proveedor = models.CharField(max_length=100)
    numero_contrato = models.CharField(max_length=4)
    year_contrato = models.IntegerField()
    fecha_inicio_contrato = models.DateField()
    fecha_fin_contrato = models.CharField(max_length=100)
    sucursal = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    supervisor = models.CharField(max_length=250)
    direccion = models.CharField(max_length=500)
    categoria = models.CharField(max_length=50)
    complejidad = models.CharField(max_length=50)
    categoria_cuentas_medicas = models.CharField(max_length=50)
    departamento = models.CharField(max_length=150)
    municipio = models.CharField(max_length=50)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    novedad = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = "proveedores"