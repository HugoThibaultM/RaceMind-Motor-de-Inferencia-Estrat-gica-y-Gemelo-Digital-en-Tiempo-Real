import fastf1
import time
import json

# 1. Configuración y Carga
fastf1.Cache.enable_cache('cache')
print("Cargando sesión...")
session = fastf1.get_session(2023, 'Monaco', 'R')
session.load(telemetry=True)

lap = session.laps.pick_driver('ALO').pick_fastest()
telemetry = lap.get_telemetry()

print("\n[START] Iniciando transmisión en tiempo real desde el coche de ALO...")
print("------------------------------------------------------------------\n")

# Guardamos el tiempo de la primera fila para calcular las diferencias
previous_time = telemetry['Time'].iloc[0]

# 2. Bucle de Emisión (Streaming)
for index, row in telemetry.iterrows():
    current_time = row['Time']
    
    # Calculamos los milisegundos que pasaron entre el dato anterior y este
    wait_time = (current_time - previous_time).total_seconds()
    
    # Simulamos la latencia real de la pista pausando el código
    if wait_time > 0:
        time.sleep(wait_time)
        
    # 3. Empaquetamos el "Payload" en formato JSON (Estándar de la industria)
    payload = {
        "timestamp": str(current_time),
        "driver": "ALO",
        "speed": int(row['Speed']),
        "rpm": int(row['RPM']),
        "gear": int(row['nGear']),
        "throttle": int(row['Throttle']), # Porcentaje de acelerador
        "brake": bool(row['Brake'])       # Freno pisado (True/False)
    }
    
    # Emitimos el evento (Por ahora a la consola, luego irá a un servidor)
    print(f"[LIVE] {json.dumps(payload)}")
    
    previous_time = current_time