# Importamos los módulos necesarios de Flask y el archivo de productos
from flask import Flask, request, redirect, url_for, render_template
from productos import productos
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, flash
import json

app = Flask(__name__)  # Creamos la aplicación Flask
app.secret_key = 'clave-super-secreta'  # Clave secreta para manejar sesiones y mensajes flash

usuarios_file = 'usuarios.py'  # Archivo donde se guardarán los usuarios registrados
carrito = []

# Función para cargar los usuarios desde el archivo usuarios.py
def cargar_usuarios():
    try:
        import usuarios  # Importa dinámicamente el archivo usuarios.py
        return usuarios.lista_usuarios  # Devuelve la lista de usuarios
    except ImportError:
        return []  # Si no existe el archivo, devuelve una lista vacía

# Función para guardar los usuarios en el archivo usuarios.py
def guardar_usuarios(usuarios):
    with open(usuarios_file, 'w') as f:
        # Guarda la lista como una variable de Python en el archivo
        f.write(f"lista_usuarios = {usuarios}\n")

usuarios = cargar_usuarios()  # Cargamos los usuarios al iniciar la app

# Ruta para la página principal (landing page)
@app.route('/')
def index():
    return render_template('LandingPage.html')  # Muestra la página principal

# Ruta para registrarse, permite GET (mostrar formulario) y POST (procesar datos)
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Procesamos el formulario
        usuario = request.form['usuario'].strip().lower()
        mail = request.form['mail'].strip().lower()
        contrasena = request.form['contrasena'].strip()
        
        # Creamos un nuevo usuario como diccionario
        nuevo_usuario = {'usuario': usuario, 'mail': mail, 'contrasena': contrasena}
        usuarios.append(nuevo_usuario)  # Lo agregamos a la lista
        guardar_usuarios(usuarios)  # Guardamos la lista actualizada en el archivo
        print("Usuarios registrados:", usuarios)  # Solo para debug
        return redirect(url_for('login'))  # Redirige a la página de inicio de sesión

    return render_template('registro.html')  # Muestra el formulario de registro

# Ruta para iniciar sesión, también acepta GET (mostrar) y POST (verificar)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Procesamos el formulario de inicio de sesión
        mail_ingresado = request.form['mail'].strip().lower()
        contrasena_ingresada = request.form['contrasena'].strip()

        # Buscamos el usuario en la lista que coincida con mail y contraseña
        usuario_encontrado = list(filter(
            lambda u: u['mail'].lower() == mail_ingresado and u['contrasena'] == contrasena_ingresada,
            usuarios
        ))

        if usuario_encontrado:
            # Si lo encontramos, damos la bienvenida
            nombre_usuario = usuario_encontrado[0]['usuario']
            return f"""
                <html>
                <body style="font-family: Arial; text-align: center; padding-top: 100px;">
                    <h2>Bienvenido, {nombre_usuario}!</h2>
                    <a href='/menu' style="text-decoration:none; padding:10px; background:#2ecc71;
                    color:white; border-radius:5px;">Ir al menú</a>
                </body>
                </html>"""
        else:
            # Si no se encuentra, mostramos mensaje de error
            return f"""
                <html>
                <body style="font-family: Arial; text-align: center; padding-top: 100px;">
                    <h3 style="color:red;">Correo o contraseña incorrectos</h3>
                    <a href='/login' style="text-decoration:none; padding:10px; background:#e74c3c;
                    color:white; border-radius:5px;">Volver</a>
                </body>
                </html>
            """
    return render_template('iniciosesion.html')  # Muestra el formulario de login

# Ruta alternativa que también muestra el formulario de inicio de sesión
@app.route('/iniciosesion')
def iniciosesion():
    return render_template('iniciosesion.html')

# Ruta para mostrar el menú de productos, permite ordenarlos por nombre o precio
@app.route('/menu')
def menu():
    criterio = request.args.get('ordenar_por', 'nombre')
    if criterio not in ['nombre', 'precio']:
        criterio = 'nombre'  # Valor por defecto seguro
    
    productos_ordenados = sorted(productos, key=lambda x: x[criterio])
    return render_template('menu.html', productos=productos_ordenados)



# Ruta para mostrar el carrito de compra con los precios totales
@app.route('/carrito')
def ver_carrito():
    total = sum(item['precio'] for item in carrito)
    return render_template('carrito.html', carrito=carrito, total=total)


# Ruta para agregar un producto al carrito, recibe el ID del producto
@app.route('/agregar_al_carrito/<int:id>', methods=['POST'])
def agregar_al_carrito(id):
    for producto in productos:
        if producto['id'] == id:
            carrito.append({'nombre': producto['nombre'], 'precio': producto['precio']})
            break
    return redirect(url_for('ver_carrito'))

# Función para generar un slug a partir del nombre del producto
def generar_slug(nombre):
    return "-".join(nombre.lower().split())

# Ruta para ver los detalles de un producto específico, recibe el nombre del producto
@app.route('/producto/<nombre>')
def detalle_producto(nombre):
    slug = generar_slug(nombre)

    # Aseguramos que todos los productos tengan un slug
    for producto in productos:
        if 'slug' not in producto:
            producto['slug'] = generar_slug(producto['nombre'])

    # Buscamos el producto que coincida con el slug
    producto_encontrado = next((p for p in productos if p['slug'] == slug), None)

    if producto_encontrado:
        return render_template('detalle_producto.html', producto=producto_encontrado)
    else:
        return "<h3>Producto no encontrado</h3>", 404

# Ruta para comprar el carrito, guarda el historial de compras
@app.route('/comprar_carrito')
def comprar_carrito():
    global carrito
    mensaje = ""

    if not carrito:
        mensaje = "⚠️ El carrito está vacío, no hay nada para comprar."
        total = 0
        return render_template('carrito.html', carrito=carrito, total=total, mensaje=mensaje)

    # Crear nueva compra
    compra = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": carrito.copy()
    }

    historial = []

    # Intentar cargar historial anterior si existe
    try:
        with open('historial_compras.json', 'r') as f:
            historial = json.load(f)
    except FileNotFoundError:
        historial = []
    except Exception as e:
        mensaje = f"⚠️ Error al leer el historial anterior: {e}"
        historial = []

    historial.append(compra)

    try:
        with open('historial_compras.json', 'w') as f:
            json.dump(historial, f, indent=4)
        mensaje = "✅ Carrito comprado y guardado en historial."
        carrito.clear()
    except Exception as e:
        mensaje = f"❌ Error al guardar el historial: {e}"

    total = sum(item['precio'] for item in carrito)
    return render_template('carrito.html', carrito=carrito, total=total, mensaje=mensaje)


    
    
@app.route('/eliminar_item/<nombre>')
def eliminar_item_carrito(nombre):
    global carrito
    carrito = [item for item in carrito if item['nombre'] != nombre]
    flash(f"🗑 Se eliminó '{nombre}' del carrito.")
    return redirect(url_for('ver_carrito'))



@app.route('/vaciar_carrito')
def vaciar_carrito():
    global carrito
    carrito = []
    flash("🧹 Carrito vaciado.")
    return redirect(url_for('ver_carrito'))




# Iniciamos la aplicación si ejecutamos este archivo directamente
if __name__ == '__main__':
    app.run(debug=True)
