import os

class CSV:
    def __init__(self, busqueda):
        self.busqueda = busqueda

        if not os.path.exists('../csvs/'):
            os.makedirs('../csvs/')

        with open('../csvs/' + self.busqueda + '.csv', 'w') as f:
            f.write("Titulo, Precio, Barrio, Ciudad, Fecha publicacion, Puntuacion vendedor, Imagen, URL \n")

    def escribir_a_csv(self, producto):
        with open('../csvs/' + self.busqueda + '.csv', 'a') as f:
            f.write(producto.titulo + "," + producto.precio + "," + producto.barrio + ","
                    + producto.ciudad + "," + producto.fecha_publicacion + ", "
                    + producto.puntuacion_vendedor + "," + producto.imagen[0] + "," + producto.url + "\n")
