from . import DBConnection

class Monitoreo:
    """
    Clase que representa los datos meteorológicos monitoreados.
    """
    def __init__(self, temperatura, humedad_relativa, humedad_suelo, fecha, hora):
        self.temperatura = temperatura
        self.humedad_relativa = humedad_relativa
        self.humedad_suelo = humedad_suelo
        self.fecha = fecha
        self.hora = hora

    @classmethod
    def obtener_datos_recientes(cls, limite=8):
        """
        Obtiene los datos meteorológicos más recientes.
        """
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT temperatura, 
                       hum_relativa AS humedad_relativa, 
                       hum_suelo AS humedad_suelo, 
                       fecha, 
                       hora
                FROM condiciones_meteorologicas
                ORDER BY fecha DESC, hora DESC
                LIMIT %s
            """, (limite,))
            filas = cursor.fetchall()
            return [cls(**fila) for fila in filas]
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return []
        finally:
            cursor.close()



