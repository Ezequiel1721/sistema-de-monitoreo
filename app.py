from flask import Flask, render_template, jsonify, request, redirect, url_for
import random
from datetime import datetime
import mysql.connector


app = Flask(__name__)

def connection():
    db = mysql.connector.connect(
        pool_name='s',
        pool_size=5,  # Puedes ajustar el tamaño del pool
        host="sql3.freemysqlhosting.net",
    	user="sql3748146",
    	password="HNWn3HFPjP",
    	database="sql3748146",
    	port=3306
    )
    return db, db.cursor(dictionary=True)
#cursor = db.cursor(dictionary=True)

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
    conn, cursor = connection()
    if request.method == 'POST':
        tipo = request.form['tipo']
        modelo = request.form['modelo']
        estado = request.form['estado']
        try:
            cursor.execute(
                "INSERT INTO sensores (tipo, modelo, estado, id_zona) VALUES (%s, %s, %s, 1)",
                (tipo, modelo, estado)
            )
            conn.commit()
        except Exception as e:
            print(f"Error al registrar sensor: {e}")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('registrar_sensor'))

    try:
        cursor.execute("SELECT * FROM sensores")
        sensores = cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener sensores: {e}")
        sensores = []
    finally:
        cursor.close()
        conn.close()
    return render_template('sensores.html', sensores=sensores)

@app.route('/eliminarSensor/<int:id_sensor>', methods=['POST'])
def eliminar_sensor(id_sensor):
    conn, cursor = connection()
    try:
        cursor.execute("DELETE FROM sensores WHERE id_sensor = %s", (id_sensor,))
        conn.commit()
    except Exception as e:
        print(f"Error al eliminar sensor: {e}")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('registrar_sensor'))

@app.route('/monitoreo')
def monitoreo():
    return render_template('monitoreo.html')

@app.route('/horarios', methods=['GET', 'POST'])
def registrar_horario():
    conn, cursor = connection()
    if request.method == 'POST':
        hora_inicio = request.form['hora_inicio']
        duracion = request.form['duracion']
        frecuencia = request.form['frecuencia']
        try:
            cursor.execute(
                "INSERT INTO horarios (hora_inicio, duracion, frecuencia, id_zona) VALUES (%s, %s, %s, 1)",
                (hora_inicio, duracion, frecuencia)
            )
            conn.commit()
        except Exception as e:
            print(f"Error al registrar horario: {e}")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('registrar_horario'))

    try:
        cursor.execute("SELECT * FROM horarios")
        horarios = cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener horarios: {e}")
        horarios = []
    finally:
        cursor.close()
        conn.close()
    return render_template('horarios.html', horarios=horarios)

@app.route('/regar/<int:id_horario>', methods=['POST'])
def registrar_riego(id_horario):
    conn, cursor = connection()
    try:
        cursor.execute("""
            SELECT id_condiciones 
            FROM condiciones_meteorologicas 
            ORDER BY fecha DESC, hora DESC 
            LIMIT 1
        """)
        resultado = cursor.fetchone()
        id_condiciones = resultado['id_condiciones'] if resultado else None

        if id_condiciones is None:
            return "No hay registros en condiciones_meteorologicas", 400

        fecha = request.form['fecha']
        hora = request.form['hora']
        duracion = request.form['duracion']

        cursor.execute("""
            INSERT INTO eventos (fecha, hora, duracion, id_zona, id_usuario, estado, id_condiciones)
            VALUES (%s, %s, %s, 1, 1, 'exitoso', %s)
        """, (fecha, hora, duracion, id_condiciones))
        conn.commit()
    except Exception as e:
        print(f"Error al registrar riego: {e}")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('registrar_horario'))

@app.route('/eliminarHorario/<int:id_horario>', methods=['POST'])
def eliminar_horario(id_horario):
    conn, cursor = connection()
    try:
        cursor.execute("DELETE FROM horarios WHERE id_horario = %s", (id_horario,))
        conn.commit()
    except Exception as e:
        print(f"Error al eliminar horario: {e}")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('registrar_horario'))

@app.route('/historial', methods=['GET'])
def ver_historial():
    conn, cursor = connection()
    filtro_fecha = request.args.get('fecha')
    try:
        if filtro_fecha:
            cursor.execute("SELECT * FROM eventos WHERE fecha = %s", (filtro_fecha,))
        else:
            cursor.execute("SELECT * FROM eventos")
        historial = cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener historial: {e}")
        historial = []
    finally:
        cursor.close()
        conn.close()
    return render_template('historial.html', historial=historial)

@app.route('/data')
def get_data():
    conn, cursor = connection()
    try:
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

        etiquetas = [f"{registro['fecha']} {registro['hora']}" for registro in registros]
        temperaturas = [registro['temperatura'] for registro in registros]
        humedades_relativas = [registro['hum_relativa'] for registro in registros]
        humedades_suelo = [registro['hum_suelo'] for registro in registros]
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return jsonify({"error": "Error al obtener datos"}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({
        "temperatura": temperaturas[::-1],
        "hum_relativa": humedades_relativas[::-1],
        "hum_suelo": humedades_suelo[::-1],
        "etiquetas": etiquetas[::-1]
    })

if __name__ == '__main__':
    app.run(debug=True)