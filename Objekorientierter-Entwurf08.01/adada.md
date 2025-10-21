
from flask import Flask, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from model.py import Spieler
   

@app.route("/Spieler", methods=["POST"])
def hande_Spieler():
    """Erstellt einen neuen Spieler."""
    try:
        data = request.get_json()
        Spieler = Spieler(**data)
        return jsonify({
            "status": "ok",
            "message": "Spieler erfolgreich erstellt",
            "Spieler": Spieler()
        }), 201
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "message": "Validierung fehlgeschlagen",
            "details": e.errors()
        }), 400

# Hinweis: Zum Starten außerhalb des Notebooks ausführen:
# if __name__ == "__main__":
#     app.run(debug=True)