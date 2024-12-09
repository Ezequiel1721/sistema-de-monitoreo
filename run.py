from app import create_app
from app.models import DBConnection  # Importar DBConnection desde models
from config import Config  # Importar la configuración
from datetime import timedelta  # Importar timedelta para el filtro

# Crea la aplicación Flask
app = create_app()

# Registrar el filtro personalizado
@app.template_filter('format_timedelta')
def format_timedelta(value):
    """
    Convierte un timedelta a un formato legible (HH:MM:SS).
    """
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return value

# Inicializar el pool de conexiones
DBConnection.init_pool()

if __name__ == '__main__':
    # Ejecutar la aplicación
    app.run(debug=False)
