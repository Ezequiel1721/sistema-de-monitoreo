import mysql.connector
from mysql.connector import pooling
from config import Config  # Importar configuración

class DBConnection:
    """
    Clase para gestionar la conexión a la base de datos utilizando un pool de conexiones.
    """
    _connection_pool = None

    @classmethod
    def init_pool(cls):
        """
        Inicializa el pool de conexiones usando las variables de configuración.
        """
        cls._connection_pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=10,  # Ajusta según tus necesidades
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

    @classmethod
    def get_connection(cls):
        """
        Obtiene una conexión del pool.
        """
        if cls._connection_pool is None:
            raise Exception("El pool de conexiones no ha sido inicializado.")
        try:
            return cls._connection_pool.get_connection()
        except Exception as e:
            print(f"Error al obtener conexión del pool: {e}")
            raise




    @staticmethod
    def close_connection():
        """
        Cierra la conexión a la base de datos si está activa.
        """
        if DBConnection._connection:
            try:
                DBConnection._connection.close()
                print("Conexión a la base de datos cerrada.")
            except mysql.connector.Error as e:
                print(f"Error al cerrar la conexión: {e}")
            finally:
                DBConnection._connection = None


