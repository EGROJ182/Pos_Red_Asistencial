from django.db import models

# Create your models here.
class m100Vigente(models.Model):
    id_med = models.AutoField(primary_key=True)
    cums_canal = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    descripcion_medicamento = models.CharField(max_length=1000)
    marca = models.CharField(max_length=250)
    principio_activo = models.CharField(max_length=1000)
    concentracion = models.CharField(max_length=500)
    forma_farmaceutica = models.CharField(max_length=250)
    presentacion = models.CharField(max_length=1000)
    registro_sanitario = models.CharField(max_length=50)
    estado_registro = models.CharField(max_length=100)
    atc = models.CharField(max_length=50)
    cum = models.CharField(max_length=50)
    expediente = models.IntegerField()
    consecutivo = models.IntegerField()
    codigo_cum_homologo = models.CharField(max_length=50)
    alianza = models.CharField(max_length=2)
    laboratorio_alianza = models.CharField(max_length=500)
    canal = models.CharField(max_length=50)
    cantidad_minima_de_dispensacion = models.CharField(max_length=250)
    variable_cantidad_unidad_minima_negociada = models.CharField(max_length=50)
    valor_medicamento_regulado = models.CharField(max_length=20)
    tarifa_pactada_por_unidad_sin_iva = models.CharField(max_length=20)
    medicamentos_de_control_especial = models.CharField(max_length=2)
    medicamentos_monopolio_del_estado = models.CharField(max_length=2)
    nit_proveedor = models.IntegerField()
    nombre_del_proveedor_pactado = models.CharField(max_length=500)
    numero_acta_inicial = models.CharField(max_length=25)
    fecha_pactada = models.DateField()
    validador_acta_duplicada = models.CharField(max_length=25)
    circular_valor_regulado = models.CharField(max_length=32)
    precio_maximo_final_institucional = models.CharField(max_length=20)
    precio_maximo_final_comercial = models.CharField(max_length=20)
    status_invima = models.CharField(max_length=37)
    validador_precio_mismo_canal = models.CharField(max_length=9)
    precio_regulado_institucional_2022 = models.CharField(max_length=20)
    novedad = models.CharField(max_length=500)
    status = models.BooleanField()

    class Meta:
        managed = False
        db_table = "consolidado_medicamentos"
        # db_table = "m100_vigente"