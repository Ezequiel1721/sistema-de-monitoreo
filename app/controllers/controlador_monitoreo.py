from flask import Blueprint, render_template, jsonify
from ..models.modelo_monitoreo import Monitoreo

class ControladorMonitoreo:
    """
    Controlador para manejar las rutas relacionadas con el monitoreo.
    """
    def __init__(self):
        self.blueprint = Blueprint("monitoreo", __name__, url_prefix="/monitoreo")
        self.registrar_rutas()

    def registrar_rutas(self):
        """
        Registra las rutas para el monitoreo.
        """
        @self.blueprint.route("/", methods=["GET"])
        def pagina_monitoreo():
            """
            Renderiza la página principal de monitoreo.
            """
            return render_template("monitoreo.html")

        @self.blueprint.route("/datos", methods=["GET"])
        def obtener_datos_monitoreo():
            """
            Devuelve datos recientes de monitoreo en formato JSON.
            """
            try:
                datos = Monitoreo.obtener_datos_recientes()
                if not datos:
                    return jsonify({"error": "No se encontraron registros"}), 404

                # Construye etiquetas únicas combinando fecha y hora
                etiquetas = [f"{d.fecha} {d.hora}" for d in datos]

                temperaturas = [d.temperatura for d in datos]
                humedades_suelo = [d.humedad_suelo for d in datos]
                humedades_relativas = [d.humedad_relativa for d in datos]

                return jsonify({
                    "etiquetas": etiquetas,
                    "temperatura": temperaturas,
                    "hum_suelo": humedades_suelo,
                    "hum_relativa": humedades_relativas,
                })
    
            except Exception as e:
                print(f"Error al obtener datos de monitoreo: {e}")
                return jsonify({"error": "Error interno del servidor"}), 500




