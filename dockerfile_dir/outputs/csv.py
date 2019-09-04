
class CSV:
    def __init__(self, titulo_busqueda):
        self.titulo_busqueda = titulo_busqueda
        with open('csvs/' + self.titulo_busqueda + '.csv', 'w') as f:
            f.write("Titulo, Precio, Barrio, Ciudad, Fecha publicacion, Puntuacion vendedor, Imagen, URL \n")

    def escribir_a_csv(self, producto, titulo_busqueda):
        with open('csvs/' + titulo_busqueda + '.csv', 'a') as f:
            f.write(producto["titulo"] + "," + producto["precio"] + "," + producto["barrio"] + ","
                    + producto["ciudad"] + "," + producto["fechaPublicacion"] + ", " + producto["puntuacion"]
                    + "," + producto["imagenURL"] + "," + producto["url"] + "\n")

