from . import DBConnection

class Usuario:
    def __init__(self, id_usuario, nombre_usuario, rol, contrasena):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.rol = rol
        self.contrasena = contrasena

    @classmethod
    def obtener_por_nombre_usuario(cls, nombre_usuario):
        """
        Busca un usuario por su nombre de usuario en la base de datos.
        """
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id_usuario, nombre_usuario, rol, contrasena
                FROM usuarios
                WHERE nombre_usuario = %s
                LIMIT 1
            """, (nombre_usuario,))
            fila = cursor.fetchone()
            return cls(**fila) if fila else None
        except Exception as e:
            print(f"Error al buscar usuario por nombre de usuario: {e}")
            return None
        finally:
            cursor.close()


