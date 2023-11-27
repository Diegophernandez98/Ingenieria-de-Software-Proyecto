from django.db import models

class Rol_Lista(models.Model):
    nombre = models.CharField(max_length=15)

class Tipo_Producto(models.Model):
    nombre = models.CharField(max_length=15)

class Tipo_Animal(models.Model):
    nombre = models.CharField(max_length=15)

class Usuario(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    correo = models.CharField(max_length=50, null=False, unique=True)
    celular = models.CharField(max_length=50, null=False)
    comuna = models.CharField(max_length=50, null=False)
    direccion = models.CharField(max_length=100, null=False)
    contrasena = models.CharField(max_length=50, null=False)
    rol = models.ForeignKey(Rol_Lista, on_delete=models.CASCADE)

class Producto(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True)
    precio = models.IntegerField(null=False, default=10000)
    stock = models.IntegerField(null=False, default=100)
    tipo_producto = models.ForeignKey(Tipo_Producto, on_delete=models.CASCADE)
    tipo_animal = models.ForeignKey(Tipo_Animal, on_delete=models.CASCADE)

class Venta(models.Model):
    valor = models.IntegerField(null=False)
    fecha = models.DateTimeField(null=False)
    comuna = models.CharField(max_length=50, null=False)
    direccion = models.CharField(max_length=100, null=False)
    id_producto = models.ManyToManyField('Producto', related_name='ventas_id_producto')
    productos = models.ManyToManyField(Producto, related_name='ventas_productos')

class Dudas(models.Model):
    correo = models.CharField(max_length=50)
    duda = models.CharField(max_length=1000)
