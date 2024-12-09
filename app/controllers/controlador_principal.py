from flask import Blueprint, render_template

class ControladorPrincipal:
    """
    Controlador para manejar las rutas principales de la aplicación.
    """
    def __init__(self):
        self.blueprint = Blueprint("principal", __name__)
        self.registrar_rutas()

    def registrar_rutas(self):
        """
        Registra las rutas principales de la aplicación.
        """
        @self.blueprint.route("/")
        def inicio():
            """
            Página de inicio de la aplicación.
            """
            return render_template("index.html")

