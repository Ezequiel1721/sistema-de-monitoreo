from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from ..models.modelo_horario import Horario

class ControladorHorarios:
    """
    Controlador que maneja las rutas relacionadas con los horarios de riego.
    """
    def __init__(self):
        self.blueprint = Blueprint("horarios", __name__, url_prefix="/horarios")
        self.registrar_rutas()

    def registrar_rutas(self):
        """
        Registra todas las rutas relacionadas con la gestión de horarios.
        """
        @self.blueprint.route("/", methods=["GET", "POST"])
        def gestionar_horarios():
            """
            Página principal para gestionar horarios de riego.
            """
            if request.method == "POST":
                hora_inicio = request.form.get("hora_inicio")
                duracion = request.form.get("duracion")
                frecuencia = request.form.get("frecuencia")
                id_zona = request.form.get("id_zona")

                # Imprime los datos recibidos
                print(f"Datos recibidos: hora_inicio={hora_inicio}, duracion={duracion}, frecuencia={frecuencia}, id_zona={id_zona}")

                if not hora_inicio or not duracion or not frecuencia or not id_zona:
                    flash("Todos los campos son obligatorios.", "danger")
                    return redirect("/horarios/")


                if Horario.agregar(hora_inicio, duracion, frecuencia, id_zona):
                    flash("Horario registrado con éxito.", "success")
                else:
                    flash("Error al registrar horario.", "danger")

            horarios = Horario.obtener_todos()
            print("Datos enviados a la vista:", horarios)  # Depuración
            return render_template("horarios.html", horarios=horarios)

        @self.blueprint.route("/eliminar/<int:id_horario>", methods=["POST"])
        def eliminar_horario(id_horario):
            """
            Elimina un horario de la base de datos.
            """
            print(f"ID recibido para eliminar: {id_horario}")  # Depuración

            if session.get("role") != "profesor":
                flash("No tienes permiso para eliminar horarios.", "danger")
                return redirect("/horarios")

            if Horario.eliminar(id_horario):
                flash("Horario eliminado con éxito.", "success")
            else:
                flash("Error al eliminar horario.", "danger")

            return redirect("/horarios")  # Asegúrate de redirigir al listado actualizado
        




        @self.blueprint.route("/regar/<int:id_zona>", methods=["POST"])
        def regar(id_zona):
            """
            Registra un evento de riego en la tabla 'eventos'.
            """
            id_usuario = session.get("user_id")  # Usuario actual
            fecha = request.form.get("fecha")  # Fecha del evento
            hora = request.form.get("hora")  # Hora del evento
            duracion = request.form.get("duracion")  # Duración en minutos

            print(f"ID de zona: {id_zona}")  # Depuración
            print(f"Datos recibidos: fecha={fecha}, hora={hora}, duracion={duracion}, id_usuario={id_usuario}")  # Depuración

            if not id_usuario or not fecha or not hora or not duracion:
                flash("Todos los campos son obligatorios para iniciar el riego.", "danger")
                return redirect("/horarios")

            if Horario.regar(id_zona, id_usuario, fecha, hora, duracion):
                flash("Evento de riego registrado con éxito.", "success")
            else:
                flash("Error al registrar el evento de riego. Inténtalo de nuevo.", "danger")

            return redirect("/horarios")




