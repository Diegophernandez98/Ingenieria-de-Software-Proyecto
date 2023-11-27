from django.shortcuts import render, redirect
from django.db import IntegrityError
from app.models import Usuario, Rol_Lista, Producto, Tipo_Producto, Tipo_Animal, Dudas, Venta
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.db.models import Sum
from django.db.models.functions import TruncMonth

def inicio(request):
    return render(request, "index.html")

def nosotros(request):
    return render(request, "nosotros.html")

def contacto(request):
    if request.method == "GET":
        return render(request, "contacto.html")
    elif request.method == "POST":
            getCorreo = request.POST.get('correo')
            getDuda = request.POST.get('duda')

            if getCorreo and getDuda: 
                usuarioDuda = Dudas(correo=getCorreo, duda= getDuda)
                usuarioDuda.save()
                return redirect('contacto')
            else:
                error_message = "Error. Verifique que haya ingresado correctamente los datos"
                return render(request, "contacto.html", {"error_message": error_message})
        
def registro(request):
    if request.method == "GET":
        return render(request, "registro.html")
    elif request.method == "POST":
        rut = request.POST.get("rut")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        celular = request.POST.get("celular")
        comuna = request.POST.get("comuna")
        direccion = request.POST.get("direccion")
        contrasena = request.POST.get("contrasena")

        # Crear un nuevo registro
        nuevoRegistro = Usuario(
            rut=rut,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            celular=celular,
            comuna=comuna,
            direccion=direccion,
            contrasena=contrasena,
            rol_id=1
        )

        # Verificar si el rut ya existe en la base de datos
        if Usuario.objects.filter(rut=rut).exists():
            error_messagerut = "El rut ya existe"
            return render(request, "registro.html", {"error_messagerut": error_messagerut})
        else:
            # Guardar el nuevo registro si el rut no existe
            nuevoRegistro.save()
            return redirect('/inicio_sesion')
    else:
        # Enviar un mensaje de error si el método de solicitud no es GET o POST
        error_message = "Error. Método de solicitud no permitido"
        return render(request, "registro.html", {"error_message": error_message})
    
def inicio_sesion(request):
    if request.method == "GET":
        return render(request, "inicio_sesion.html")
    
    elif request.method == "POST":
        getUsuario = request.POST.get('rut')
        getContrasena = request.POST.get('contrasena')
        usuario = Usuario.objects.filter(rut=getUsuario, contrasena=getContrasena).first()
        
        if usuario is not None:

            if usuario.rol_id == 1 :
                # Para agregar un valor dentro de la SESSION, lo hacemos como si fuera un diccionario
                request.session["usuario"] = getUsuario
                print(f"El usuario {usuario.nombre} ha iniciado sesión.")
                return render(request, "cliente.html", {'rut':getUsuario})
            
            elif usuario.rol_id == 2 :
                request.session["usuario"] = getUsuario
                print(f"El usuario {usuario.nombre} ha iniciado sesión.")
                return render(request, "administrador.html", {'rut':getUsuario})

        else:
            error_message = "Error. Verifique que haya ingresado correctamente los datos"
            return render(request, "inicio_sesion.html", {"error_message": error_message})
            
def cambiar_clave(request):
    if request.method == 'GET':
        return render(request, "cambiar_clave.html")
    
    elif request.method == 'POST':
        contrasena_Actual = request.POST.get('contrasena_actual')
        contrasena_Nueva = request.POST.get('contrasena_nueva')

        if request.session.get('usuario'):
            usuario = Usuario.objects.get(rut=request.session.get('usuario'))


            if contrasena_Actual == usuario.contrasena:
                usuario.contrasena = contrasena_Nueva
                usuario.save()
                print("Clave cambiada exitosamente.")
                return render(request, "cambiar_clave.html", {'usuario': usuario})
            
            else:
                error_message = "Error, contraseña actual incorrecta."
    else:
        return redirect('inicio_Sesion')
    return render(request, "cambiar_clave.html", {'error_message': error_message})
        
def cerrar_sesion(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    return redirect('login')

@login_required(login_url='/inicio_sesion/')
@never_cache
def cliente(request):
    return render(request, "cliente.html")

@login_required(login_url='/inicio_sesion/')
@never_cache
def administrador(request):
    return render(request, "administrador.html")

def cambiar_nomape(request):
    if request.method == 'GET':
        return render(request, "cambiar_nomape.html")
    
    elif request.method == 'POST':

        if request.session.get('usuario'):
            usuario = Usuario.objects.get(rut=request.session.get('usuario'))
            usuario.nombre = request.POST.get('nombre_nuevo', usuario.nombre)
            usuario.apellido = request.POST.get('apellido_nuevo', usuario.apellido)
            usuario.comuna = request.POST.get('comuna_nueva', usuario.comuna)
            usuario.direccion = request.POST.get('direccion_nueva', usuario.direccion)

            usuario.save()
            print("Datos cambiados exitosamente.")
            return render(request, "cambiar_nomape.html", {'usuario': usuario})
            
        else:
            error_message = "Error, datos ingresados incorrectos."
            return render(request, "cambiar_nomape.html", {'error_message': error_message})
    
    else:
        return redirect('cliente')
    
def agregar_producto(request):
    if request.method == "GET":
        return render(request, "agregar_producto.html")
    
    elif request.method == "POST":
        nombre = request.POST.get("nombre")
        precio = request.POST.get("precio")
        stock = request.POST.get("stock")
        id_tipo_producto = request.POST.get("id_tipo_producto")
        id_tipo_animal = request.POST.get("id_tipo_animal")

        nuevoProducto = Producto(nombre=nombre,
                                 precio=precio, 
                                 stock=stock, 
                                 id_tipo_producto_id=id_tipo_producto, 
                                 id_tipo_animal_id=id_tipo_animal,
                                )
        
        if nuevoProducto is not None:
            nuevoProducto.save()
            return redirect('/agregar_producto')
        else:
            error_message = "Error. Verifique que haya ingresado correctamente los datos"
            return render(request, "agregar_producto.html", {"error_message": error_message})

def productos(request):
    productos = Producto.objects.all()
    data={"productos": productos}
    return render(request, "productos.html", data)

def eliminar_producto(request, producto_id):
    producto = Producto.objects.get(pk=producto_id)
    producto.delete()
    return redirect('/productos')

def actualizar_producto(request, producto_id):
        producto = Producto.objects.get(pk=producto_id)

        if request.method == 'POST':

            nombre_nuevo = request.POST.get('nombre_nuevo')
            precio_nuevo = request.POST.get('precio_nuevo')
            stock_nuevo = request.POST.get('stock_nuevo')

            producto.nombre = nombre_nuevo
            producto.precio = precio_nuevo
            producto.stock = stock_nuevo
            producto.save()

            return redirect('/productos')
        
        return render(request, 'actualizar_producto.html', {'producto': producto})

def alimentos(request):
    if request.method == "GET":
        lista_alimentos_gatos = Producto.objects.all()
        return render(request, "alimentos.html", {'lista_alimentos_gatos': lista_alimentos_gatos})
    
    elif request.method == "POST":
           return render(request, "alimentos.html")
        
def alimento(request, tipoP_id, tipoA_id):
    producto = Producto.objects.filter(id_tipo_producto_id=tipoP_id,id_tipo_animal_id=tipoA_id)
    tipo_producto = Tipo_Producto.objects.get(id=tipoP_id)
    tipo_animal = Tipo_Animal.objects.get(id=tipoA_id)
    return render(request, "alimento_tp.html", {"producto":producto, "tipo_producto": tipo_producto, "tipo_animal":tipo_animal})

def accesorio(request, tipoP_id, tipoA_id):
    producto = Producto.objects.filter(id_tipo_producto_id=tipoP_id,id_tipo_animal_id=tipoA_id)
    tipo_producto = Tipo_Producto.objects.get(id=tipoP_id)
    tipo_animal = Tipo_Animal.objects.get(id=tipoA_id)
    return render(request, "accesorio.html", {"producto":producto, "tipo_producto": tipo_producto, "tipo_animal":tipo_animal})

def farmacia_tipo(request, tipoP_id, tipoA_id):
    producto = Producto.objects.filter(id_tipo_producto_id=tipoP_id,id_tipo_animal_id=tipoA_id)
    tipo_producto = Tipo_Producto.objects.get(id=tipoP_id)
    tipo_animal = Tipo_Animal.objects.get(id=tipoA_id)
    return render(request, "farmacia_tipo.html", {"producto":producto, "tipo_producto": tipo_producto, "tipo_animal":tipo_animal})

def todos_productos(request):
    producto = Producto.objects.all()
    return render(request, "farmacia_tipo.html", {"producto":producto})

def accesorios(request):
    return render(request, "accesorios.html")

def farmacia(request):
    return render(request, "farmacia.html")

def otras_mascotas(request):
    return render(request, "otras_mascotas.html")

def todo_alimento(request):
    return render(request, "todo_alimento.html")

def carritoCompra(request, producto_id):

    producto = Producto.objects.get(pk=producto_id)

    if producto.stock > 0:
        carrito = request.session.get('carrito', [])
        carrito.append({'id': producto.id, 'nombre': producto.nombre, 'precio': float(producto.precio)})
        request.session['carrito'] = carrito
        carrito = request.session.get('carrito', [])
        total = sum(item['precio'] for item in carrito)
        return render(request, 'carritoCompra.html', {'carrito': carrito, 'total': total})

    return render(request, 'carritoCompra.html', {'producto': producto})

def verCarrito(request):
    carrito = request.session.get('carrito', [])
    return render(request, 'carritoCompra.html', {'carrito': carrito})

def eliminarProductoCarrito(request, producto_id):
    carrito = request.session.get('carrito', [])

    for item in carrito:
        if item['id'] == producto_id:
            # Restaurar stock
            producto = Producto.objects.get(pk=producto_id)
            producto.stock += 0
            producto.save()

            carrito.remove(item)
            request.session['carrito'] = carrito
            if not carrito:
                error_message = "El carrito está vacío."
                return render(request, 'carritoCompra.html', {'error_message': error_message})
            else:
                return render(request, 'carritoCompra.html', {'producto': producto})
        error_message = "El producto no se encontró en el carrito."
        return render(request, 'carritoCompra.html', {'error_message': error_message})    

def vaciarCarrito(request):
    carrito = request.session.get('carrito', [])
    for item in carrito:
        producto = Producto.objects.get(pk=item['id'])
        producto.stock += 1
        producto.save()

    request.session['carrito'] = []

    return render(request, 'index.html')

def procesar_compra(request):
    if request.method == 'POST':
        comuna = request.POST.get('comuna')
        direccion = request.POST.get('direccion')

        carrito = request.session.get('carrito', [])

        valor_total = sum(item['precio'] for item in carrito)

        try:
            # Obtener la fecha actual
            fecha_actual = datetime.now()

            # Crear la venta con solo el día, mes y año
            nueva_venta = Venta.objects.create(
                valor=valor_total,
                fecha=fecha_actual.date(),  # Obtener solo la fecha
                comuna=comuna,
                direccion=direccion
            )

            for item in carrito:
                producto = Producto.objects.get(pk=item['id'])

                # Verificar si hay suficiente stock
                if producto.stock >= 1:
                    nueva_venta.id_producto.add(producto)
                    producto.stock -= 1
                    producto.save()
                else:
                    raise IntegrityError("Stock insuficiente para el producto {}".format(producto.nombre))

            request.session['carrito'] = []

            return render(request, 'venta_realizada.html', {'venta': nueva_venta})

        except IntegrityError as e:
            error_message = str(e)
            return render(request, 'carritoCompra.html', {'error_message': error_message})

    return redirect('carritoCompra')

def ganancias(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        ventas = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])

        # Modificar la consulta para agrupar por mes y calcular la suma de las ganancias
        ganancias_por_mes = ventas.annotate(mes=TruncMonth('fecha')).values('mes').annotate(ganancia=Sum('valor')).order_by('mes')

        return render(request, 'ganancias.html', {'ganancias_por_mes': ganancias_por_mes})
    else:
        return render(request, 'comparar_ganancias.html')
    
def comparar_ganancias(request):
    return render(request, 'comparar_ganancias.html')

def ver_boletas(request):
    ventas = Venta.objects.all()
    data = {'ventas': ventas}
    return render(request, 'ver_boletas.html', data)