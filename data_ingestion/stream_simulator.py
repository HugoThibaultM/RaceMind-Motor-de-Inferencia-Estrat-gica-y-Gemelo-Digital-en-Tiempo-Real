import fastf1
import time
import json
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fastf1.Cache.enable_cache('cache')
print("Cargando sesión...")
session = fastf1.get_session(2023, 'Monaco', 'R')
session.load(telemetry=True)

lap = session.laps.pick_driver('ALO').pick_fastest()
telemetry = lap.get_telemetry()

print(f"\n[COCHE] Emitiendo telemetría por radio (UDP {UDP_IP}:{UDP_PORT})...")

# Bucle infinito: el coche dará vueltas sin parar
while True:
    print("\n--- ¡NUEVA VUELTA INICIADA! ---")
    previous_time = telemetry['Time'].iloc[0]

    for index, row in telemetry.iterrows():
        current_time = row['Time']
        wait_time = (current_time - previous_time).total_seconds()
        
        if wait_time > 0:
            time.sleep(wait_time)
            
        payload = {
            "timestamp": str(current_time),
            "driver": "ALO",
            "speed": int(row['Speed']),
            "rpm": int(row['RPM']),
            "gear": int(row['nGear']),
            "throttle": int(row['Throttle']),
            "brake": bool(row['Brake'])
        }
        
        mensaje = json.dumps(payload).encode('utf-8')
        sock.sendto(mensaje, (UDP_IP, UDP_PORT))
        
        previous_time = current_time