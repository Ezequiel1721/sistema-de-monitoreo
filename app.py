from flask import Flask, render_template, jsonify, request, redirect, url_for
import random
from datetime import datetime
import mysql.connector


app = Flask(__name__)

# Configuración de la conexión
db = mysql.connector.connect(
    host="sql3.freemysqlhosting.net",
    user="sql3748146",
    password="HNWn3HFPjP",
    #database="monitoreo",
    port=3306
)

cursor = db.cursor(dictionary=True)

# Lista para almacenar los horarios registrados (temporal en memoria)
horarios = []
# Lista para almacenar los sensores registrados (temporal en memoria)
sensores = []

historial = []  # Lista para almacenar los registros de riego

# Ruta para la página principal
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sensores', methods=['GET', 'POST'])
def registrar_sensor():
    if request.method == 'POST':
        tipo = request.form['tipo']
        modelo = request.form['modelo']
        estado = request.form['estado']

        # Guardar en la base de datos
        cursor.execute(
            "INSERT INTO sensores (tipo, modelo, estado, id_zona) VALUES (%s, %s, %s, 1)",
            (tipo, modelo, estado)
        )
        db.commit()
        return redirect(url_for('registrar_sensor'))

    # Consultar sensores de la base de datos
    cursor.execute("SELECT * FROM sensores")
    sensores = cursor.fetchall()
    return render_template('sensores.html', sensores=sensores)

@app.route('/eliminarSensor/<int:id_sensor>', methods=['POST'])
def eliminar_sensor(id_sensor):
    cursor.execute("DELETE FROM sensores WHERE id_sensor = %s", (id_sensor,))
    db.commit()
    return redirect(url_for('registrar_sensor'))

# Ruta para la página de Monitoreo
@app.route('/monitoreo')
def monitoreo():
    return render_template('monitoreo.html')

@app.route('/horarios', methods=['GET', 'POST'])
def registrar_horario():
    if request.method == 'POST':
        hora_inicio = request.form['hora_inicio']
        duracion = request.form['duracion']
        frecuencia = request.form['frecuencia']

        # Insertar en la base de datos
        cursor.execute(
            "INSERT INTO horarios (hora_inicio, duracion, frecuencia, id_zona) VALUES (%s, %s, %s, 1)",
            (hora_inicio, duracion, frecuencia)
        )
        db.commit()
        return redirect(url_for('registrar_horario'))

    # Consultar horarios desde la base de datos
    cursor.execute("SELECT * FROM horarios")
    horarios = cursor.fetchall()
    return render_template('horarios.html', horarios=horarios)

@app.route('/regar/<int:id_horario>', methods=['POST'])
def registrar_riego(id_horario):
    # Consultar el último id_condiciones de la tabla condiciones_meteorologicas
    cursor.execute("""
        SELECT id_condiciones 
        FROM condiciones_meteorologicas 
        ORDER BY fecha DESC, hora DESC 
        LIMIT 1
    """)
    resultado = cursor.fetchone()
    id_condiciones = resultado['id_condiciones'] if resultado else None

    # Verificar si se encontró un id_condiciones
    if id_condiciones is None:
        return "No hay registros en condiciones_meteorologicas", 400

    # Tomar los valores del formulario
    fecha = request.form['fecha']
    hora = request.form['hora']
    duracion = request.form['duracion']

    # Registrar el nuevo evento
    cursor.execute("""
        INSERT INTO eventos (fecha, hora, duracion, id_zona, id_usuario, estado, id_condiciones)
        VALUES (%s, %s, %s, 1, 1, 'exitoso', %s)
    """, (fecha, hora, duracion, id_condiciones))
    db.commit()

    return redirect(url_for('registrar_horario'))

@app.route('/eliminarHorario/<int:id_horario>', methods=['POST'])
def eliminar_horario(id_horario):
    cursor.execute("DELETE FROM horarios WHERE id_horario = %s", (id_horario,))
    db.commit()
    return redirect(url_for('registrar_horario'))

@app.route('/historial', methods=['GET'])
def ver_historial():
    filtro_fecha = request.args.get('fecha')
    if filtro_fecha:
        cursor.execute("SELECT * FROM eventos WHERE fecha = %s", (filtro_fecha,))
    else:
        cursor.execute("SELECT * FROM eventos")
    historial = cursor.fetchall()
    return render_template('historial.html', historial=historial)


@app.route('/data')
def get_data():
    # Consulta para obtener los últimos 8 registros, formateando la fecha para eliminar la hora
    cursor.execute("""
        SELECT 
            temperatura, 
            hum_relativa, 
            hum_suelo, 
            DATE_FORMAT(fecha, '%Y-%m-%d') AS fecha, 
            hora
        FROM condiciones_meteorologicas
        ORDER BY fecha DESC, hora DESC
        LIMIT 8
    """)
    registros = cursor.fetchall()
    
    # Construir las etiquetas combinando fecha y hora
    etiquetas = [f"{registro['fecha']} {registro['hora']}" for registro in registros]

    # Extraer los datos para cada atributo
    temperaturas = [registro['temperatura'] for registro in registros]
    humedades_relativas = [registro['hum_relativa'] for registro in registros]
    humedades_suelo = [registro['hum_suelo'] for registro in registros]
    
    # Revertimos el orden para que sean cronológicos
    return jsonify({
        "temperatura": temperaturas[::-1],
        "hum_relativa": humedades_relativas[::-1],
        "hum_suelo": humedades_suelo[::-1],
        "etiquetas": etiquetas[::-1]
    })




if __name__ == '__main__':
    app.run(debug=False)