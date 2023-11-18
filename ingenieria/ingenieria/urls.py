from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name="inicio"),
    path('alimentos/', views.alimentos, name="alimentos"),
    path('accesorios/', views.accesorios, name="accesorios"),
    path('farmacia/', views.farmacia, name="farmacia"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('contacto/', views.contacto, name="contacto"),
    path('registro/', views.registro, name="registro"),
    path('inicio_sesion/', views.inicio_sesion, name="login"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
    path('cliente/', views.cliente, name="cliente"),
    path('administrador/', views.administrador, name="administrador"),
    path('carrito_compras/', views.carrito_compras, name="carrito_compras"),
    path('empleado/', views.empleado, name="empleado"),
    path('gatos/', views.gatos, name="gatos"),
    path('perros/', views.perros, name="perros"),
    path('otras_mascotas/', views.otras_mascotas, name="otras_mascotas"),
    path('todo_alimento/', views.todo_alimento, name="todo_alimento"),
    path('cambiar_clave/', views.cambiar_clave, name="cambiar_clave"),
    path('cambiar_domicilio/', views.cambiar_domicilio, name="cambiar_domicilio"),
    path('cambiar_nomape/', views.cambiar_nomape, name="cambiar_nomape"),
    path('agregar_producto', views.agregar_producto, name="agregar_producto"),
    path('productos/', views.productos, name="productos"),
    path("eliminar_producto/<int:producto_id>/", views.eliminar_producto),
    path("actualizar_producto/", views.actualizar_producto, name="actualizar_producto"),
    path("producto_editar/", views.producto_editar, name="producto_editar")
]
