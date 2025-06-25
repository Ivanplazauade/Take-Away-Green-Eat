from productos import productos

def generar_slug(nombre):
    return "-".join(nombre.lower().split())


# Ruta para mostrar detalle individual del producto

def detalle_producto(slug):
    productos_filtrados = list(filter(lambda p: generar_slug(p["nombre"]) == slug.lower(), productos))


    if productos_filtrados:
        producto = productos_filtrados
        return producto
    else:
        return "Producto no encontrado"

    
detalle_producto("Tostadas")
