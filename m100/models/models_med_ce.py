from django.db import models

# Create your models here.
class MCE(models.Model):
    id_med_ce = models.AutoField(primary_key=True)
    dci = models.CharField(max_length=50)
    dci_busqueda = models.CharField(max_length=50)
    concentracion = models.CharField(max_length=50)
    forma_farmaceutica = models.CharField(max_length=50)
    nota = models.CharField(max_length=512)
    codigo_cum = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "m100_ce"