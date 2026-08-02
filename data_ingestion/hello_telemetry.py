import fastf1
import pandas as pd

# Configurar el directorio de caché (vital para no saturar los servidores de la F1)
fastf1.Cache.enable_cache('cache') 

print("Cargando sesión...")
# Cargamos la carrera de Mónaco 2023 (o cambia el año y circuito)
session = fastf1.get_session(2023, 'Monaco', 'R')
session.load(telemetry=True)

print("Buscando la vuelta rápida de Alonso (ALO)...")
alonso_lap = session.laps.pick_driver('ALO').pick_fastest()

print("Extrayendo telemetría...")
telemetry = alonso_lap.get_telemetry()

# Mostramos las primeras 5 filas con datos de Velocidad, RPM y Marcha
df_preview = telemetry[['Time', 'Speed', 'RPM', 'nGear']].head()
print("\n--- DATOS DE TELEMETRÍA (Primeros milisegundos) ---")
print(df_preview)