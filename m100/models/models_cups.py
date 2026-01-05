from django.db import models

# Create your models here.
class Cups(models.Model):
    id_red = models.AutoField(primary_key=True)
    codigo_cups = models.CharField(max_length=12)
    codigo_homologo_manual = models.CharField(max_length=30)
    descripcion_del_cups = models.CharField(max_length=1000)
    nombre = models.CharField(max_length=500)
    nit = models.IntegerField()
    departamento = models.CharField(max_length=500)
    municipio = models.CharField(max_length=500)
    numero_contrato = models.CharField(max_length=4)
    year_contrato = models.IntegerField()

    class Meta:
        managed = False
        db_table = "red_positiva_cups"