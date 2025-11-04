document.getElementById("spielerForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Seite soll nicht neu geladen werden

    // Formulardaten sammeln
    const spieler = {
        name: document.getElementById("name").value,
        jahrgang: parseInt(document.getElementById("jahrgang").value),
        staerke: parseFloat(document.getElementById("staerke").value),
        torschuss: parseFloat(document.getElementById("staerke").value)
    };

    // Daten an den Server senden
    const response = await fetch("https://literate-happiness-pjp75w97g5j926wxq-12345.app.github.dev/Spieler", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(spieler)
    });

    // Antwort anzeigen
    const ergebnis = await response.json();
    document.getElementById("serverAntwort").textContent = JSON.stringify(ergebnis, null, 2);
});