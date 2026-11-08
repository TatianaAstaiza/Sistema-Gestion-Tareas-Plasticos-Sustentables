from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Tarea


class PruebasAutenticacion(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='usuario_prueba',
            password='Prueba12345'
        )

    def test_inicio_sesion_exitoso(self):
        respuesta = self.client.post(reverse('login'), {
            'username': 'usuario_prueba',
            'password': 'Prueba12345'
        })
        self.assertRedirects(respuesta, reverse('inicio'))
        self.assertTrue(respuesta.wsgi_request.user.is_authenticated)

    def test_inicio_sesion_con_password_incorrecto(self):
        respuesta = self.client.post(reverse('login'), {
            'username': 'usuario_prueba',
            'password': 'Incorrecta123'
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(respuesta.wsgi_request.user.is_authenticated)

    def test_acceso_sin_autenticacion(self):
        respuesta = self.client.get(reverse('crear_tarea'))
        self.assertRedirects(
            respuesta,
            f"{reverse('login')}?next={reverse('crear_tarea')}"
        )

    def test_cerrar_sesion(self):
        self.client.login(
            username='usuario_prueba',
            password='Prueba12345'
        )
        respuesta = self.client.post(reverse('logout'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.url, reverse('inicio'))
        self.assertNotIn('_auth_user_id', self.client.session)


class PruebasCreacionTareas(TestCase):

    def setUp(self):
        self.creador = User.objects.create_user(
            username='creador_prueba',
            password='Prueba12345'
        )

        self.empleado = User.objects.create_user(
            username='empleado_prueba',
            password='Prueba12345'
        )

        self.client.login(
            username='creador_prueba',
            password='Prueba12345'
        )

    def enviar_tarea(self):
        return self.client.post(reverse('crear_tarea'), {
            'titulo': 'Verificar inventario',
            'descripcion': 'Revisar materiales disponibles',
            'fecha_limite': '',
            'asignada_a': self.empleado.id
        })

    def test_crear_tarea_correctamente(self):
        respuesta = self.enviar_tarea()
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Tarea.objects.count(), 1)

    def test_tarea_guarda_creador(self):
        self.enviar_tarea()
        tarea = Tarea.objects.first()
        self.assertEqual(tarea.creada_por, self.creador)

    def test_tarea_guarda_empleado_asignado(self):
        self.enviar_tarea()
        tarea = Tarea.objects.first()
        self.assertEqual(tarea.asignada_a, self.empleado)

    def test_usuario_sin_autenticacion_no_crea_tarea(self):
        self.client.logout()

        respuesta = self.client.post(reverse('crear_tarea'), {
            'titulo': 'Tarea no autorizada',
            'descripcion': 'Prueba de acceso',
            'fecha_limite': '',
            'asignada_a': self.empleado.id
        })

        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Tarea.objects.count(), 0)