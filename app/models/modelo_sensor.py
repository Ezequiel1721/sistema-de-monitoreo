from . import DBConnection

class Sensor:
    """
    Clase que representa un sensor en el sistema.
    """
    def __init__(self, id_sensor, tipo, modelo, estado):
        self.id = id_sensor
        self.tipo = tipo
        self.modelo = modelo
        self.estado = estado

    @classmethod
    def obtener_todos(cls):
        """
        Obtiene todos los sensores de la base de datos.
        """
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_sensor, tipo, modelo, estado FROM sensores")
            filas = cursor.fetchall()
            return [cls(**fila) for fila in filas]
        finally:
            cursor.close()
            conn.close()  # Importante cerrar la conexión

    @classmethod
    def agregar(cls, id_zona, tipo, modelo, estado):
        """
        Agrega un nuevo sensor a la base de datos.
        """
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO sensores (id_zona, tipo, modelo, estado) VALUES (%s, %s, %s, %s)"
            print(f"Consulta SQL: {query}")
            print(f"Datos enviados: {id_zona}, {tipo}, {modelo}, {estado}")
            cursor.execute(query, (id_zona, tipo, modelo, estado))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar sensor: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


    @classmethod
    def eliminar(cls, id_sensor):
        """
        Elimina un sensor de la base de datos.
        """
        try:
            conn = DBConnection.get_connection()  # Obtén la conexión
            cursor = conn.cursor()  # Abre el cursor manualmente
            query = "DELETE FROM sensores WHERE id_sensor = %s"
            print(f"Consulta SQL: {query} | Datos: {id_sensor}")  # Para depuración
            cursor.execute(query, (id_sensor,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar sensor: {e}")
            return False
        finally:
            cursor.close()  # Cierra el cursor manualmente
            conn.close()  # Cierra la conexión manualmente



