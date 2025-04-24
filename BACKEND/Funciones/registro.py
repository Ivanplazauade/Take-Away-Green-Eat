usuarios = []
def registrar_usuario():
    nombre = input("Nombre: ")
    email = input("Email: ")
    contraseña = input("Contraseña: ")
    usuarios.append([nombre, email, contraseña])
    print("✅ Usuario registrado con éxito.\n")

def login_usuario():
    email = input("Email: ")
    contraseña = input("Contraseña: ")
    for u in usuarios:
        if u[1] == email and u[2] == contraseña:
            print(f"\n🎉 Bienvenido, {u[0]}!\n")
            return True
    print("❌ Credenciales incorrectas.\n")
    return False