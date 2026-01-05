from django.db import models

# Create your models here.
class dane_data(models.Model):
    id_dane = models.AutoField(primary_key=True)
    region = models.CharField(max_length=50)
    codigo_del_departamento = models.CharField(max_length=2)
    departamento = models.CharField(max_length=100)
    codigo_del_municipio = models.CharField(max_length=3)
    municipio = models.CharField(max_length=100)
    codigo_dane = models.CharField(max_length=5)
    zona_especial = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = "codigos_dane"