from flask import Flask, request, jsonify

app = Flask(__name__)

# Route für die Hauptseite
@app.route('/')
def home():
    return "Server ist bereit und wartet auf Anfragen."

# Route für mein PB
@app.route('/pb')
def handle_pb():
    return "Lukas hat dicke Beine."

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
    return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)  # Server starten

