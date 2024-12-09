from flask import Flask
from config import Config
from .controllers import blueprints  # Importar tus Blueprints
from .models import DBConnection  # Importar la clase DBConnection para inicializar el pool

class AplicacionFlask:
    """
    Clase para inicializar y configurar la aplicación Flask.
    """
    def __init__(self):
        # Crea una instancia de Flask
        self.app = Flask(__name__)
        # Carga la configuración desde la clase Config
        self.app.config.from_object(Config)
        # Inicializa el pool de conexiones a la base de datos
        self.inicializar_conexion_db()
        # Registra los Blueprints (controladores)
        self.registrar_blueprints()

    def inicializar_conexion_db(self):
        """
        Inicializa el pool de conexiones a la base de datos.
        """
        DBConnection.init_pool()

    def registrar_blueprints(self):
        """
        Registra todos los Blueprints definidos en el proyecto.
        """
        for blueprint in blueprints:
            self.app.register_blueprint(blueprint)

def create_app():
    """
    Función de fábrica que retorna una instancia de la aplicación Flask.
    """
    return AplicacionFlask().app





