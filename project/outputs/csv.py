import os


class CSV:
    def __init__(self, busqueda):
        self.busqueda = busqueda
        self.directorio_csv = os.path.dirname(os.path.abspath(__file__)) + '/../../csvs'
        self.fichero_csv = self.directorio_csv + '/' + self.busqueda + '.csv'

        if not os.path.exists(self.directorio_csv):
            os.makedirs(self.directorio_csv)

        with open(self.fichero_csv, 'w') as f:
            f.write("Titulo, Precio, Barrio, Ciudad, Fecha publicacion, Puntuacion vendedor, Imagen, URL \n")
            f.close()

    def escribir_a_csv(self, producto):
        with open(self.fichero_csv, 'a') as f:
            f.write(producto.titulo + "," + producto.precio + "," + producto.barrio + ","
                    + producto.ciudad + "," + producto.fecha_publicacion + ", "
                    + producto.puntuacion_vendedor + "," + producto.imagen[0] + "," + producto.url + "\n")
            f.close()
