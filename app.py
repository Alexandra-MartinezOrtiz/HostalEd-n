from flask import Flask, request, jsonify
import pandas as pd
import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")  # Asegúrate de que index.html esté en /templates

if __name__ == "__main__":
    app.run(debug=True)

EXCEL_FILE = "reservas.xlsx"
HOTEL_EMAIL = "hostaleleden3@gmail.com"
GMAIL_USER = "hostaleleden3@gmail.com"  # Tu correo de envío
GMAIL_PASSWORD = "ABCdef80"  # Usa una contraseña de aplicación si usas Gmail



def guardar_reserva(data):
    nueva_reserva = {
        "Fecha de llegada": data["fecha_llegada"],
        "Fecha de salida": data["fecha_salida"],
        "Huéspedes": data["huespedes"]
    }
    
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame(columns=["Fecha de llegada", "Fecha de salida", "Huéspedes"])
    
    df = df.append(nueva_reserva, ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

def enviar_correo_reserva(data):
    msg = EmailMessage()
    msg["Subject"] = "Nueva Reserva en Hostal El Edén"
    msg["From"] = GMAIL_USER
    msg["To"] = HOTEL_EMAIL
    msg.set_content(f"""
    Se ha realizado una nueva reserva:
    
    📅 Fecha de llegada: {data["fecha_llegada"]}
    📅 Fecha de salida: {data["fecha_salida"]}
    🏨 Huéspedes: {data["huespedes"]}
    
    Revisa la información en el sistema de reservas.
    """)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
        print("Correo enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

@app.route("/guardar_reserva", methods=["POST"])
def guardar():
    data = request.json
    guardar_reserva(data)
    enviar_correo_reserva(data)
    return jsonify({"message": "Reserva guardada y correo enviado"}), 200

if __name__ == "__main__":
    app.run(debug=True)
