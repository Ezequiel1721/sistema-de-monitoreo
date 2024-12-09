from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from werkzeug.security import check_password_hash
from ..models.modelo_usuario import Usuario

class ControladorUsuarios:
    def __init__(self):
        self.blueprint = Blueprint("usuarios", __name__, url_prefix="/usuarios")
        self.registrar_rutas()

    def registrar_rutas(self):
        @self.blueprint.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                nombre_usuario = request.form.get("nombre_usuario")  # Cambia a nombre de usuario
                password = request.form.get("password")

                # Busca al usuario por su nombre de usuario
                usuario = Usuario.obtener_por_nombre_usuario(nombre_usuario)

                if usuario and check_password_hash(usuario.contrasena, password):
                    # Credenciales correctas: guardar usuario en la sesión
                    session["user_id"] = usuario.id_usuario
                    session["nombtre_usuario"] = usuario.nombre_usuario
                    session["role"]  = usuario.rol
                    print("Constraseña correcta")
                    print(f"Sesión actual: {session}")
                    return redirect(url_for("principal.inicio"))  # Redirige a la página principal
                else:
                    print("Constraseña Incorrecta")
                    flash("Credenciales incorrectas. Por favor, intenta de nuevo.", "error")

            return render_template("login.html")


        @self.blueprint.route("/logout", methods=["GET"])
        def logout():
            session.clear()  # Limpia la sesión
            return redirect(url_for("principal.inicio"))


