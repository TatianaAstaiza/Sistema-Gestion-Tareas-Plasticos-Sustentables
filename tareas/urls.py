
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion_view, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('crear-tarea/', views.crear_tarea, name='crear_tarea'),
    path('editar-tarea/<int:id>/', views.editar_tarea, name='editar_tarea'),
    path('eliminar-tarea/<int:id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('cambiar-estado/<int:id>/', views.cambiar_estado, name='cambiar_estado'),
]
