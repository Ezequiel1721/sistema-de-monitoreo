from flask import Blueprint, render_template
from ..models.modelo_evento import Evento


class ControladorHistorial:
    """
    Controlador que maneja las rutas relacionadas con el historial de eventos.
    """
    def __init__(self):
        self.blueprint = Blueprint("historial", __name__, url_prefix="/historial")
        self.registrar_rutas()

    def registrar_rutas(self):
        """
        Registra todas las rutas relacionadas con el historial.
        """
        @self.blueprint.route("/")
        def ver_historial():
            """
            Página para ver el historial de eventos registrados.
            """
            eventos = Evento.obtener_historial()
            return render_template("historial.html", eventos=eventos)
    
