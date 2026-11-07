from django.db import models
from django.contrib.auth.models import User


class Tarea(models.Model):

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    creada_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tareas_creadas'
    )

    asignada_a = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tareas_asignadas'
    )

    def __str__(self):
        return self.titulo
