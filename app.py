from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Configurações Z-API
ZAPI_INSTANCE = os.environ.get("ZAPI_INSTANCE")
ZAPI_TOKEN = os.environ.get("ZAPI_TOKEN")
ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"

@app.route("/", methods=["GET"])
def home():
    return "AYRA está online! 🤖"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # Pega a mensagem recebida
    if data and "text" in data and "message" in data["text"]:
        telefone = data["phone"]
        mensagem = data["text"]["message"]

        # Resposta da AYRA
        resposta = gerar_resposta(mensagem)

        # Envia resposta pelo WhatsApp
        payload = {
            "phone": telefone,
            "message": resposta
        }
        requests.post(ZAPI_URL, json=payload)

    return "OK", 200

def gerar_resposta(mensagem):
    mensagem = mensagem.lower()
    if "bom dia" in mensagem:
        return "Bom dia! ☀️ Eu sou a AYRA, sua assistente. Como posso te ajudar hoje?"
    elif "agenda" in mensagem:
        return "📅 Vou verificar sua agenda! (em breve integrado com Google Calendar)"
    elif "email" in mensagem:
        return "📧 Vou checar seus e-mails! (em breve integrado com Gmail)"
    else:
        return f"Entendi: '{mensagem}'. Em breve vou responder com IA! 🤖"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
