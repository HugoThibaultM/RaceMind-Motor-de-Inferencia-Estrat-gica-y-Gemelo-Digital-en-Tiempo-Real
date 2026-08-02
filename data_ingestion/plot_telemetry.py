import fastf1
import matplotlib.pyplot as plt

# Mantenemos la caché para no tener que volver a descargar Mónaco
fastf1.Cache.enable_cache('cache')

print("Cargando sesión desde la caché...")
session = fastf1.get_session(2023, 'Monaco', 'R')
session.load(telemetry=True)

print("Obteniendo vuelta rápida de Alonso...")
lap = session.laps.pick_driver('ALO').pick_fastest()
telemetry = lap.get_telemetry()

print("Generando gráfico...")
# Configuramos el tamaño del gráfico
plt.figure(figsize=(12, 5))

# Eje X: Distancia (metros), Eje Y: Velocidad (km/h)
plt.plot(telemetry['Distance'], telemetry['Speed'], label='Velocidad (km/h)', color='#006F62') # Verde Aston Martin

plt.title('Velocidad de Fernando Alonso - Vuelta Rápida (Mónaco 2023)')
plt.xlabel('Distancia recorrida en la vuelta (metros)')
plt.ylabel('Velocidad (km/h)')
plt.legend()
plt.grid(True)

# Esto abrirá una ventana emergente con tu gráfico
plt.show()