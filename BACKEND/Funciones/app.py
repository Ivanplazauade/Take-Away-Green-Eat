from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

# Ruta al archivo donde se almacenará la lista de usuarios
usuarios_file = 'usuarios.py'

# Función para cargar los usuarios 
def cargar_usuarios():
    try:
        # Intentar importar el archivo de usuarios
        import usuarios
        return usuarios.lista_usuarios
    except ImportError:
        # Si el archivo no existe o no tiene datos, devolver lista vacía
        return []

# Función para guardar los usuarios en el archivo .py
def guardar_usuarios(usuarios):
    with open(usuarios_file, 'w') as f:
        f.write(f"lista_usuarios = {usuarios}\n")

# Lista de usuarios (cargada del archivo)
usuarios = cargar_usuarios()

@app.route('/')
def index():
    return render_template('index.html')  # Página principal

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        
        # Crear un diccionario con los datos del usuario
        nuevo_usuario = {'usuario': usuario, 'contrasena': contrasena}
        
        # Agregar el nuevo usuario a la lista
        usuarios.append(nuevo_usuario)
        
        # Guardar la lista de usuarios en el archivo .py
        guardar_usuarios(usuarios)
        
        # Mostrar la lista actualizada de usuarios en la consola
        print("Usuarios registrados:", usuarios)
        
        return redirect(url_for('index'))  # Redirigir después de registrar al usuario

    return render_template('registro.html')  # Mostrar el formulario de registro

if __name__ == '__main__':
    app.run(debug=True)

