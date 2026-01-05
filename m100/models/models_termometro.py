from django.db import models

# Create your models here.
class termometro(models.Model):
    id_termometro = models.AutoField(primary_key=True)
    expediente_invima = models.IntegerField()
    principio_activo = models.CharField(max_length=500)
    concentracion = models.CharField(max_length=500)
    unidad_base = models.CharField(max_length=25)
    unidad_de_dispensacion = models.CharField(max_length=250)
    nombre_comercial = models.CharField(max_length=500)
    fabricante = models.CharField(max_length=250)
    medicamento = models.CharField(max_length=500)
    canal = models.CharField(max_length=13)
    precio_por_tableta = models.CharField(max_length=20)
    factores_precio = models.CharField(max_length=5)
    numero_factor = models.IntegerField()
    presentacion = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = "termometro_2024"