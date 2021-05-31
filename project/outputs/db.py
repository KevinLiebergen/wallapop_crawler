import pymysql
import os
import warnings


class BaseDatos:
    def __init__(self):
        db_addr = os.environ.get('DB_ADDR', 'localhost')

        self.db = pymysql.connect(
            host=db_addr, port=3306, user="wallapop",
            passwd="wallapop", db="crawler"
        )
        self.cursor = self.db.cursor()

    def guardar_elemento_bbdd(self, produc):

        query = "INSERT IGNORE INTO productos VALUES ( '" + produc["titulo"] + "', '" + \
                produc["precio"] + "', " + produc["barrio"] + ", '" + produc["ciudad"] + "', '" + \
                produc["fechaPublicacion"] + "', " + produc["puntuacion"] + ", '" + produc["imagenURL"] + "', '" + \
                produc["url"] + "')"

        try:
            # Suprime los warnings de mysql (util para cuando inserta filas duplicadas y no deja)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.cursor.execute(query)

                self.db.commit()
        except:
            self.db.rollback()
