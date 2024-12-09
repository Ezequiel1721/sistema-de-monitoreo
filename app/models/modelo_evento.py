from . import DBConnection

class Evento:
    """
    Clase que representa un evento o historial de riego en el sistema.
    """
    def __init__(self, id_evento, id_zona, id_usuario, id_condiciones, fecha, hora, duracion, estado):
        self.id_evento = id_evento
        self.id_zona = id_zona
        self.id_usuario = id_usuario
        self.id_condiciones = id_condiciones
        self.fecha = fecha
        self.hora = hora
        self.duracion = duracion
        self.estado = estado

    @classmethod
    def obtener_historial(cls):
        """
        Obtiene el historial de eventos de riego, incluyendo datos relacionados.
        """
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    e.id_evento, 
                    z.nombre AS nombre_zona, 
                    u.nombre_usuario AS nombre_usuario, 
                    c.temperatura, 
                    c.hum_suelo, 
                    c.hum_relativa, 
                    DATE(e.fecha) AS fecha, 
                    TIME(e.hora) AS hora, 
                    e.duracion, 
                    e.estado
                FROM eventos e
                JOIN zonas z ON e.id_zona = z.id_zona
                JOIN usuarios u ON e.id_usuario = u.id_usuario
                JOIN condiciones_meteorologicas c ON e.id_condiciones = c.id_condiciones;
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()


