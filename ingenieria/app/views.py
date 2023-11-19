from django.shortcuts import render, redirect
from app.models import Usuario, Rol_Lista, Producto, Tipo_Producto, Tipo_Animal, Dudas
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

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
        nuevoRegistro = Usuario(rut=rut,
                                nombre=nombre,
                                apellido=apellido,
                                correo=correo,
                                celular=celular,
                                comuna=comuna,
                                direccion=direccion,
                                contrasena=contrasena,
                                rol_id=1)
        
        if nuevoRegistro is not None:
            nuevoRegistro.save()
            return redirect('/inicio_sesion')
        else:
            # Enviar un mensaje de error si no se proporciona un nombre de usuario
            error_message = "Error. Verifique que haya ingresado correctamente los datos"
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

def cambiar_domicilio(request):
    if request.method == 'GET':
        return render(request, "cambiar_domicilio.html")
    
    elif request.method == 'POST':
        comuna_Nueva = request.POST.get('comuna_nueva')
        direccion_Nueva = request.POST.get('direccion_nueva')

        if request.session.get('usuario'):
            usuario = Usuario.objects.get(rut=request.session.get('usuario'))
            usuario.comuna = comuna_Nueva
            usuario.direccion = direccion_Nueva
            usuario.save()
            print("Domicilio cambiado exitosamente.")
            return render(request, "cambiar_domicilio.html", {'usuario': usuario})
            
        else:
            error_message = "Error, comuna o dirección incorrectos."
    else:
        return redirect('cliente')
    return render(request, "cambiar_domicilio.html", {'error_message': error_message})

def cambiar_nomape(request):
    if request.method == 'GET':
        return render(request, "cambiar_nomape.html")
    
    elif request.method == 'POST':
        nombre_Nuevo = request.POST.get('nombre_nuevo')
        apellido_Nuevo = request.POST.get('apellido_nuevo')

        if request.session.get('usuario'):
            usuario = Usuario.objects.get(rut=request.session.get('usuario'))
            usuario.nombre = nombre_Nuevo
            usuario.apellido = apellido_Nuevo
            usuario.save()
            print("Datos cambiados exitosamente.")
            return render(request, "cambiar_nomape.html", {'usuario': usuario})
            
        else:
            error_message = "Error, nombre o apellido incorrectos."
    else:
        return redirect('cliente')
    return render(request, "cambiar_nomape.html", {'error_message': error_message})

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

def actualizar_producto(request):
    if request.method == 'GET':
        return render(request, "actualizar_producto.html")
    
    elif request.method == "POST":
        id_producto = request.POST.get('id_producto')
        nombre_nuevo = request.POST.get('nombre_nuevo')
        precio_nuevo = request.POST.get('precio_nuevo')
        stock_nuevo = request.POST.get('stock_nuevo')
        id_tipo_producto_nuevo = int(request.POST.get('id_tipo_producto_nuevo'))
        id_tipo_animal_nuevo = int(request.POST.get('id_tipo_animal_nuevo'))

        if id_producto is not None:

            producto = Producto.objects.get(id=id_producto)

            tipo_producto = Tipo_Producto.objects.get(id=id_tipo_producto_nuevo)
            tipo_animal = Tipo_Animal.objects.get(id=id_tipo_animal_nuevo)

            producto.nombre = nombre_nuevo
            producto.precio = precio_nuevo
            producto.stock = stock_nuevo
            producto.id_tipo_producto = tipo_producto
            producto.id_tipo_animal = tipo_animal
            producto.save()

            print("Datos cambiados exitosamente.")
            return render(request, "actualizar_producto.html", {'producto': producto})
        
        else:
            error_message = "Error, el ID del producto no existe"
            return render(request, "actualizar_producto.html", {'error_message': error_message})

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

def carrito_compras(request):
    return render(request, "carrito_compras.html")