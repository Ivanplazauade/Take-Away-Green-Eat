# Importamos los módulos necesarios de Flask y el archivo de productos
from flask import Flask, request, redirect, url_for, render_template
from productos import productos

app = Flask(__name__)  # Creamos la aplicación Flask

usuarios_file = 'usuarios.py'  # Archivo donde se guardarán los usuarios registrados

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
                    <a href='/menu' style="text-decoration:none; padding:10px; background:#2ecc71; color:white; border-radius:5px;">Ir al menú</a>
                </body>
                </html>"""
        else:
            # Si no se encuentra, mostramos mensaje de error
            return f"""
                <html>
                <body style="font-family: Arial; text-align: center; padding-top: 100px;">
                    <h3 style="color:red;">Correo o contraseña incorrectos</h3>
                    <a href='/login' style="text-decoration:none; padding:10px; background:#e74c3c; color:white; border-radius:5px;">Volver</a>
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
    criterio = request.args.get('ordenar_por', 'nombre')  # Obtenemos el criterio de ordenamiento
    productos_ordenados = sorted(productos, key=lambda x: x[criterio])  # Ordenamos los productos
    return render_template('menu.html', productos=productos_ordenados)  # Mostramos la vista del menú

# Iniciamos la aplicación si ejecutamos este archivo directamente
if __name__ == '__main__':
    app.run(debug=True)  # Ejecutamos Flask en modo debug
