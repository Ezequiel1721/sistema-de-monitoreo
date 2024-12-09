from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from ..models.modelo_sensor import Sensor

class ControladorSensores:
    """
    Controlador que maneja las rutas relacionadas con los sensores.
    """
    def __init__(self):
        self.blueprint = Blueprint("sensores", __name__, url_prefix="/sensores")
        self.registrar_rutas()

    def registrar_rutas(self):
        """
        Registra todas las rutas relacionadas con la gestión de sensores.
        """
        @self.blueprint.route("/", methods=["GET", "POST"])
        def gestionar_sensores():
            if request.method == "POST":
                id_zona = request.form.get("id_zona")
                tipo = request.form.get("tipo")
                modelo = request.form.get("modelo")
                estado = request.form.get("estado")

                # Imprime los datos recibidos
                print(f"Datos recibidos para registro: id_zona={id_zona}, tipo={tipo}, modelo={modelo}, estado={estado}")

                if not id_zona or not tipo or not modelo or not estado:
                    flash("Todos los campos son obligatorios.", "warning")
                    return redirect("/sensores/")

                if Sensor.agregar(id_zona, tipo, modelo, estado):
                    flash("Sensor registrado con éxito.", "success")
                else:
                    flash("Error al registrar el sensor. Revisa los datos e inténtalo nuevamente.", "danger")

            # Obtiene todos los sensores registrados
            sensores = Sensor.obtener_todos()
            return render_template("sensores.html", sensores=sensores)


        
        @self.blueprint.route("/eliminar/<int:id_sensor>", methods=["POST"])
        def eliminar_sensor(id_sensor):
            """
            Elimina un sensor de la base de datos.
            """
            try:
                if Sensor.eliminar(id_sensor):
                    flash("Sensor eliminado con éxito.", "success")
                else:
                    flash("Error al eliminar el sensor. Inténtalo de nuevo.", "danger")
            except Exception as e:
                flash(f"Error interno al intentar eliminar el sensor: {e}", "danger")
            return redirect(url_for("sensores.gestionar_sensores"))

