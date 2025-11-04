from flask import Flask, request, jsonify
from pydantic import ValidationError
from model import Spieler
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Route für die Hauptseite
@app.route('/')
def home():
    daten = attributes()
    return f"Server ist bereit und wartet auf Anfragen. {daten}"

@app.route('/Spieler')
def handle_spieler():
    
    return "Infos über Spieler werden hier Angezeigt" \
    ""

# Route für mein PB
@app.route('/pb')
def handle_pb():
    return "Information: PB-Route erreichbar."

@app.route('/Impressum')
def impressum():
    return "<html><body><h1>Impressum</h1><p>Dies ist das Impressum der Webseite.</p></body></html>"

# Route zum Empfangen von Nachrichten
@app.route('/message', methods=['POST'])
def handle_message():
    data = request.json
    message = data.get('message', '')
    print(f"Empfangen: {message}")
    response_message = f"Echo: {message}"
    attributes()
    return jsonify({"response": response_message})

def attributes():
   return f'''
    method: {request.method }")
    args: {request.args }")
    from: {request.form }")
    data: {request.data }")
    headers: {request.headers }")
    cookies: {request.cookies }")
    files: {request.files }")
    url: {request.url }")
    path: {request.path }")
    remote_addr: {request.remote_addr }")
    '''

spieler_liste = []

# Route zum Spieler
@app.route("/Spieler", methods=["POST"])
def hande_Spieler():
    """Erstellt einen neuen Spieler."""
    try:
        data = request.get_json()
        spieler = Spieler(**data)
        spieler_liste.append(spieler)
        with open("spieler.json", "w", encoding="utf-8") as f:
            json.dump([s.model_dump() for s in spieler_liste], f, ensure_ascii=False, indent=4)

        print("✅ Spieler wurden in 'spieler.json' gespeichert.")
        return jsonify({
            "status": "ok",
            "message": "Spieler erfolgreich erstellt",
            "Spieler": spieler.model_dump()
        }), 201
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "message": "Validierung fehlgeschlagen",
            "details": e.errors()
        }), 400
    

dateiname = "spieler.json"

if os.path.exists(dateiname):
    with open(dateiname, "r", encoding="utf-8") as f:
        daten = json.load(f)
    spieler_liste = [Spieler(**s) for s in daten]
    print("📂 Geladene Spieler:")
    for s in spieler_liste:
        print(s)
else:
    print(f"⚠️ Datei '{dateiname}' wurde nicht gefunden.")
    print("Es wird eine leere Spielerliste erstellt.")
    spieler_liste = []


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)  # Server starten