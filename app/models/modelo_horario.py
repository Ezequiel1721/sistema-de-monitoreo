from . import DBConnection

class Horario:
    """
    Clase que representa un horario de riego en el sistema.
    """
    def __init__(self, id_horario, hora_inicio, duracion, frecuencia, id_zona):
        self.id = id_horario
        self.hora_inicio = hora_inicio
        self.duracion = duracion
        self.frecuencia = frecuencia
        self.id_zona = id_zona

    @classmethod
    def obtener_todos(cls):
        """
        Retorna una lista de todos los horarios registrados, incluyendo el nombre de la zona.
        """
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    h.id_horario, 
                    h.hora_inicio, 
                    h.duracion, 
                    h.frecuencia, 
                    z.id_zona, 
                    z.nombre AS nombre_zona
                FROM horarios h
                JOIN zonas z ON h.id_zona = z.id_zona
        """
            cursor.execute(query)
            filas = cursor.fetchall()
            return filas
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def agregar(cls, hora_inicio, duracion, frecuencia, id_zona):
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO horarios (hora_inicio, duracion, frecuencia, id_zona)
                VALUES (%s, %s, %s, %s)
            """
            print(f"Consulta SQL: {query}")
            print(f"Datos enviados: {hora_inicio}, {duracion}, {frecuencia}, {id_zona}")
            cursor.execute(query, (hora_inicio, duracion, frecuencia, id_zona))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar horario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


    @classmethod
    def eliminar(cls, id_horario):
        """
        Elimina un horario de la base de datos.
        """
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM horarios WHERE id_horario = %s"
            print(f"Consulta SQL ejecutada: {query} | ID: {id_horario}")  # Depuración
            cursor.execute(query, (id_horario,))
            conn.commit()
            print("Eliminación completada.")  # Confirmación
            return True
        except Exception as e:
            print(f"Error al eliminar horario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


    @classmethod
    def obtener_ultimo_id_condiciones(cls):
        """
        Obtiene el id_condiciones del último registro en la tabla condiciones_meteorologicas.
        """
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            query = "SELECT id_condiciones FROM condiciones_meteorologicas ORDER BY create_time DESC LIMIT 1"
            cursor.execute(query)
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error al obtener el último id_condiciones: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def regar(cls, id_zona, id_usuario, fecha, hora, duracion, estado="Programado"):
        """
        Registra un evento de riego en la tabla 'eventos'.
        """
        try:
            # Obtener el último id_condiciones
            id_condiciones = cls.obtener_ultimo_id_condiciones()
            if not id_condiciones:
                print("No se encontró un id_condiciones válido.")
                return False

            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO eventos (id_zona, id_usuario, id_condiciones, fecha, hora, duracion, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            print(f"Consulta SQL: {query}")
            print(f"Datos enviados: {id_zona}, {id_usuario}, {id_condiciones}, {fecha}, {hora}, {duracion}, {estado}")
            cursor.execute(query, (id_zona, id_usuario, id_condiciones, fecha, hora, duracion, estado))
            conn.commit()
            print("Evento de riego registrado exitosamente.")
            return True
        except Exception as e:
            print(f"Error al registrar evento de riego: {e}")
            return False
        finally:
            cursor.close()
            conn.close()





