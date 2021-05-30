
class InformacionPantalla:
    def __init__(self, producto):
        self.titulo = producto.titulo
        self.precio = producto["precio"]
        self.descripcion = producto["descripcion"]
        self.barrio = producto["barrio"]
        self.ciudad = producto["ciudad"]
        self.fecha_publicacion = producto["fechaPublicacion"]
        self.puntuacion_vendedor = producto["puntuacion"]
        self.imagen = producto["imagenURL"]
        self.url = producto["url"]

    def imprimir_elementos(self):
        print("#"*50)
        print("Titulo: " + self.titulo)
        print("Precio: " + self.precio)
        print("Descripcion: " + self.descripcion)
        print("Barrio: " + self.barrio)
        print("Ciudad: " + self.ciudad)
        print("Fecha publicacion: " + self.fecha_publicacion)
        print("Puntuacion vendedor: " + self.puntuacion_vendedor)
        print("Imagen: " + self.imagen)
        print("URL: " + self.url)
