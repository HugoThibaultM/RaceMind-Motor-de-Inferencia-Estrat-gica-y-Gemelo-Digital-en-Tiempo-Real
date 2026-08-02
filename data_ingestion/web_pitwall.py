from flask import Flask, Response
import socket
import json
import threading
import time
import pandas as pd
import fastf1
from sklearn.ensemble import IsolationForest
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)

latest_data = {"speed": 0, "rpm": 0, "gear": 0, "anomaly": False}

def udp_and_ai_worker():
    global latest_data
    print("[IA] Entrenando modelo en segundo plano...")
    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(2023, 'Monaco', 'R')
    session.load(telemetry=True, weather=False, messages=False)
    lap = session.laps.pick_driver('ALO').pick_fastest()
    X_train = lap.get_telemetry()[['Speed', 'RPM', 'Throttle', 'Brake']].fillna(0)
    
    ai_model = IsolationForest(contamination=0.01, random_state=42)
    ai_model.fit(X_train)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 9999))
    print("[IA] Modelo listo. Escuchando UDP 9999...")

    while True:
        try:
            data, _ = sock.recvfrom(1024)
            payload = json.loads(data.decode('utf-8'))
            
            # CHIVATO VISUAL: Imprime en la consola si el dato llega
            print(f"📡 Recibiendo telemetría: {payload['speed']} km/h", end="\r")
            
            live_df = pd.DataFrame([{'Speed': payload['speed'], 'RPM': payload['rpm'], 
                                     'Throttle': payload['throttle'], 'Brake': int(payload['brake'])}])
            is_anomaly = bool(ai_model.predict(live_df)[0] == -1)
            
            latest_data = {
                "speed": payload['speed'],
                "rpm": payload['rpm'],
                "gear": payload['gear'],
                "anomaly": is_anomaly
            }
        except Exception as e:
            # Si la IA explota, ahora nos enteraremos
            print(f"\n❌ ERROR CRÍTICO EN EL HILO: {e}")

threading.Thread(target=udp_and_ai_worker, daemon=True).start()

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RaceMind Pitwall</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { background-color: #121212; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin-top: 20px;}
            .alert { color: #ff4444; font-weight: bold; text-transform: uppercase; animation: blink 1s infinite; }
            @keyframes blink { 50% { opacity: 0; } }
        </style>
    </head>
    <body>
        <h1>🏁 RaceMind Dashboard</h1>
        <h2>Velocidad: <span id="speedVal" style="color: #00ff00;">0</span> km/h | Marcha: <span id="gearVal">0</span></h2>
        <h3 id="aiStatus">✅ Ritmo Óptimo</h3>
        
        <div style="width: 80%; margin: 0 auto;">
            <canvas id="telemetryChart"></canvas>
        </div>

        <script>
            const ctx = document.getElementById('telemetryChart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'line',
                data: { labels: [], datasets: [{ label: 'Velocidad (km/h)', borderColor: '#006F62', data: [], fill: false, tension: 0.1 }] },
                options: { animation: false, scales: { y: { min: 0, max: 350 } } }
            });

            const source = new EventSource('/stream');
            source.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                document.getElementById('speedVal').innerText = data.speed;
                document.getElementById('gearVal').innerText = data.gear;
                
                const aiStatus = document.getElementById('aiStatus');
                if (data.anomaly) {
                    aiStatus.innerHTML = '<span class="alert">🚨 ANOMALÍA DETECTADA</span>';
                } else {
                    aiStatus.innerHTML = '✅ Ritmo Óptimo';
                }

                if (chart.data.labels.length > 50) {
                    chart.data.labels.shift();
                    chart.data.datasets[0].data.shift();
                }
                chart.data.labels.push('');
                chart.data.datasets[0].data.push(data.speed);
                chart.update();
            };
        </script>
    </body>
    </html>
    """
@app.route('/stream')
def stream():
    def generate():
        while True:
            # Enviamos el JSON actualizado
            yield f"data: {json.dumps(latest_data)}\n\n"
            time.sleep(0.1) # Pausa de 100ms
            
    # Forzamos cabeceras HTTP para evitar que el navegador o proxies bloqueen el stream
    response = Response(generate(), mimetype="text/event-stream")
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    response.headers['Connection'] = 'keep-alive'
    return response

if __name__ == '__main__':
    app.run(port=5000, threaded=True, debug=False)