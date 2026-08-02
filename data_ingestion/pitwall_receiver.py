import socket
import json
import fastf1
import pandas as pd
from sklearn.ensemble import IsolationForest
import warnings

# Ocultar warnings de la librería para mantener la consola limpia
warnings.filterwarnings("ignore")

print("[IA] Inicializando Motor RaceMind AI...")

# 1. FASE DE ENTRENAMIENTO (Histórico)
fastf1.Cache.enable_cache('cache')
session = fastf1.get_session(2023, 'Monaco', 'R')
session.load(telemetry=True, weather=False, messages=False)

print("[IA] Entrenando modelo con telemetría histórica de Alonso...")
lap = session.laps.pick_driver('ALO').pick_fastest()
hist_telemetry = lap.get_telemetry()

# Preparamos los datos de entrenamiento (Velocidad, RPM, Acelerador, Freno)
X_train = hist_telemetry[['Speed', 'RPM', 'Throttle', 'Brake']].fillna(0)

# Entrenamos el Bosque de Aislamiento (asumimos un 1% de datos anómalos/errores)
ai_model = IsolationForest(contamination=0.01, random_state=42)
ai_model.fit(X_train)
print("[IA] ¡Modelo entrenado y listo!")
print("-" * 50)

# 2. FASE DE STREAMING EN VIVO
UDP_IP = "127.0.0.1"
UDP_PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"[MURO DE BOXES] Escuchando telemetría en vivo en puerto {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024) 
    payload = json.loads(data.decode('utf-8'))
    
    # Preparamos el paquete exacto como lo requiere la IA
    live_data = pd.DataFrame([{
        'Speed': payload['speed'],
        'RPM': payload['rpm'],
        'Throttle': payload['throttle'],
        'Brake': int(payload['brake']) # Convertimos True/False a 1/0
    }])
    
    # La IA predice: 1 es normal, -1 es anomalía
    prediction = ai_model.predict(live_data)[0]
    
    if prediction == -1:
        print(f"🚨 [IA ALERTA ANOMALÍA] Comportamiento inusual -> Vel: {payload['speed']} km/h | Acelerador: {payload['throttle']}% | Freno: {payload['brake']}")
    else:
        print(f"✅ [IA OK] Vel: {payload['speed']} km/h | RPM: {payload['rpm']} - Ritmo óptimo")