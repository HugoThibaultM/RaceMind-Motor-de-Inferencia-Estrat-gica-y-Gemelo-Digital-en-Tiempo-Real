import fastf1
import matplotlib.pyplot as plt

# Activamos la caché
fastf1.Cache.enable_cache('cache')

print("Cargando sesión Mónaco 2023 (Carrera)...")
session = fastf1.get_session(2023, 'Monaco', 'R')
session.load(telemetry=True)

print("Obteniendo vueltas rápidas de ALO y VER...")
# Extraemos los datos de ambos pilotos
lap_alo = session.laps.pick_driver('ALO').pick_fastest()
lap_ver = session.laps.pick_driver('VER').pick_fastest()

telemetry_alo = lap_alo.get_telemetry()
telemetry_ver = lap_ver.get_telemetry()

print("Generando gráfico comparativo...")
# Hacemos el gráfico un poco más ancho
plt.figure(figsize=(14, 6))

# Graficamos la línea de Alonso en verde
plt.plot(telemetry_alo['Distance'], telemetry_alo['Speed'], 
         label='Alonso (Aston Martin)', color='#006F62', linewidth=2)
         
# Graficamos la línea de Verstappen en azul oscuro
plt.plot(telemetry_ver['Distance'], telemetry_ver['Speed'], 
         label='Verstappen (Red Bull)', color='#3671C6', linewidth=2, alpha=0.8)

plt.title('Comparativa de Velocidad: Alonso vs Verstappen (Vuelta Rápida - Mónaco 2023)')
plt.xlabel('Distancia (metros)')
plt.ylabel('Velocidad (km/h)')

# Añadimos la leyenda y la cuadrícula
plt.legend()
plt.grid(True)

# Mostramos el gráfico
plt.show()