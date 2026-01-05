from django.db import models

# Create your models here.
class proveedores(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nit = models.IntegerField()
    nombre = models.CharField(max_length=250)
    tipo_proveedor = models.CharField(max_length=100)
    numero_contrato = models.CharField(max_length=4)
    year_contrato = models.IntegerField(max_length=4)
    fecha_inicio_contrato = models.DateField()
    fecha_fin_contrato = models.CharField(max_length=100)
    sucursal = models.CharField(max_length=100)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "proveedores"