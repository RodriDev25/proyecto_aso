from django.db import models


class ValeSolicitud(models.Model):
	class Monto(models.IntegerChoices):
		QUINIENTOS_MIL = 500_000, 'Gs. 500.000'
		UN_MILLON = 1_000_000, 'Gs. 1.000.000'

	class Motivo(models.TextChoices):
		PERSONAL = 'personal', 'Gastos personales'
		SALUD = 'salud', 'Salud'
		EDUCACION = 'educacion', 'Educación'
		OTRO = 'otro', 'Otro'

	class Estado(models.TextChoices):
		PENDIENTE = 'pendiente', 'Pendiente'
		APROBADO = 'aprobado', 'Aprobado'
		RECHAZADO = 'rechazado', 'Rechazado'

	usuario = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='vales')
	monto = models.PositiveIntegerField(choices=Monto.choices)
	motivo = models.CharField(max_length=20, choices=Motivo.choices)
	observaciones = models.TextField(blank=True)
	estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
	creado_en = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-creado_en']

	def __str__(self):
		return f'{self.get_monto_display()} - {self.usuario.email}'


class PrestamoSolicitud(models.Model):
	class Plazo(models.IntegerChoices):
		SEIS_MESES = 6, '6 meses'
		DOCE_MESES = 12, '12 meses'
		DIECIOCHO_MESES = 18, '18 meses'
		VEINTICUATRO_MESES = 24, '24 meses'

	class Destino(models.TextChoices):
		VIVIENDA = 'vivienda', 'Vivienda'
		SALUD = 'salud', 'Salud'
		EDUCACION = 'educacion', 'Educación'
		CONSUMO = 'consumo', 'Consumo'
		OTRO = 'otro', 'Otro'

	class Estado(models.TextChoices):
		PENDIENTE = 'pendiente', 'Pendiente'
		EN_EVALUACION = 'evaluacion', 'En evaluación'
		APROBADO = 'aprobado', 'Aprobado'
		RECHAZADO = 'rechazado', 'Rechazado'

	usuario = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='prestamos')
	monto = models.DecimalField(max_digits=12, decimal_places=2)
	plazo_meses = models.PositiveSmallIntegerField(choices=Plazo.choices)
	destino = models.CharField(max_length=20, choices=Destino.choices)
	detalle = models.TextField()
	estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
	creado_en = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-creado_en']

	def __str__(self):
		return f'Préstamo de {self.usuario.email} - {self.monto}'
