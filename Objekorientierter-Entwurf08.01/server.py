from flask import Flask, request, jsonify

app = Flask(__name__)

# Route für die Hauptseite
@app.route('/')
def home():
    daten = attributes()
    return f"Server ist bereit und wartet auf Anfragen. {daten}"

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
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)  # Server starten