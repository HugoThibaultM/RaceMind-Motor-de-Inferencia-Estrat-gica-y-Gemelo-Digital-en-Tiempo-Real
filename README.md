# 🏁 RaceMind: Real-Time Telemetry & AI Inference Engine

RaceMind es una plataforma *Full-Stack* de procesamiento de telemetría de Fórmula 1 en tiempo real. El sistema simula la ingesta de datos de un monoplaza, los transmite mediante protocolos de baja latencia y utiliza Inteligencia Artificial para detectar anomalías de conducción en el acto.

## 🏗️ Arquitectura del Sistema

El proyecto está diseñado bajo una arquitectura de microservicios desacoplados:

1. **Event Emitter (Coche):** Simulador de streaming que lee datos históricos y los emite en paquetes JSON a través de **UDP** respetando los deltas de tiempo reales (milisegundo a milisegundo).
2. **AI Inference Engine (Backend):** Hilo de procesamiento en segundo plano que consume el flujo UDP. Utiliza un modelo de Machine Learning (**Isolation Forest** de *Scikit-Learn*) entrenado con telemetría histórica para detectar anomalías (bloqueos de frenos, pérdidas de tracción) en tiempo real.
3. **Web Dashboard (Frontend):** Servidor **Flask** que sirve una interfaz reactiva. Utiliza **Server-Sent Events (SSE)** para actualizar gráficos de *Chart.js* a alta frecuencia sin sobrecargar el navegador.

## 🚀 Tecnologías Clave

* **Data Engineering:** Python, FastF1, Pandas, Sockets UDP.
* **Machine Learning:** Scikit-Learn (Detección de Anomalías / Isolation Forest).
* **Backend & API:** Flask, Multi-threading, Server-Sent Events (SSE).
* **Frontend:** HTML5, CSS3, JavaScript, Chart.js.

## ⚙️ Cómo ejecutarlo localmente

El sistema requiere la ejecución de dos microservicios en paralelo:

1. Iniciar el Muro de Boxes (Servidor Web + IA):
   `python web_pitwall.py`
2. Iniciar el Monoplaza (Emisor UDP):
   `python stream_simulator.py`
3. Abrir el navegador en `http://localhost:5000`