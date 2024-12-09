# Importamos los controladores principales
from .controlador_principal import ControladorPrincipal
from .controlador_usuarios import ControladorUsuarios
from .controlador_sensores import ControladorSensores
from .controlador_horarios import ControladorHorarios
from .controlador_historial import ControladorHistorial
from .controlador_monitoreo import ControladorMonitoreo

# Lista de Blueprints de todos los controladores
# Estos serán registrados en la aplicación principal Flask
blueprints = [
    ControladorPrincipal().blueprint,
    ControladorUsuarios().blueprint,
    ControladorSensores().blueprint,
    ControladorHorarios().blueprint,
    ControladorHistorial().blueprint,
    ControladorMonitoreo().blueprint,
]
