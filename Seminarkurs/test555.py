from vpython import (
    canvas,      # Erstellt das Visualisierungsfenster
    box,         # Zeichnet eine Box/Würfel
    sphere,      # Zeichnet eine Kugel
    vector,      # Vektor-Klasse für 3D-Koordinaten
    color,       # Farb-Objekt
    rate,        # Kontrolliert die Simulationsgeschwindigkeit
    mag,         # Berechnet die Magnitude eines Vektors
    norm,        # Normalisiert einen Vektor
    dot          # Berechnet das Skalarprodukt zweier Vektoren
)
import random  # Für zufällige Zahlen
import math    # Mathematische Funktionen
# %%
import logging
logging.getLogger("tornado.access").setLevel(logging.ERROR)

# -------------------------------
# Einstellungen
# -------------------------------
NUM_BALLS = 15          # Anzahl der Kugeln in der Simulation
RADIUS = 0.5            # Radius jeder Kugel
BOX_SIZE = 10           # Größe der simulierten Box in jeder Dimension
DT = 0.01               # Zeitschrittweite für die Simulation

# Szene
scene = canvas(title="3D Molekulardynamik", width=800, height=600)

# Box (Grenzen)
box_frame = box(pos=vector(0,0,0), size=vector(BOX_SIZE, BOX_SIZE, BOX_SIZE), opacity=0.1)

# -------------------------------
# Kugel-Klasse
# -------------------------------

class Ball:
    """
    Repräsentiert eine Kugel in der 3D-Simulation.
    Jede Kugel hat eine Position, Geschwindigkeit und eine visuelle Darstellung.
    """
    
    def __init__(self):
        """Initialisiert eine neue Kugel mit zufälliger Position und Geschwindigkeit"""
        # Position: zufällig innerhalb der Box verteilt
        self.pos = vector(
            random.uniform(-BOX_SIZE/2, BOX_SIZE/2),
            random.uniform(-BOX_SIZE/2, BOX_SIZE/2),
            random.uniform(-BOX_SIZE/2, BOX_SIZE/2)
        )
        
        # Geschwindigkeit: zufällige Richtung und Betrag
        self.vel = vector(
            random.uniform(-2, 2),
            random.uniform(-2, 2),
            random.uniform(-2, 2)
        )
        
        # Visuelle Darstellung als weiße Kugel
        self.sphere = sphere(pos=self.pos, radius=RADIUS, color=color.white)

    def move(self):
        """Aktualisiert die Position basierend auf Geschwindigkeit und Zeitschritt"""
        self.pos += self.vel * DT
        self.sphere.pos = self.pos

    def wall_collision(self):
        """
        Prüft und behandelt Kollisionen mit den Begrenzungswänden.
        Bei Kontakt wird die entsprechende Geschwindigkeitskomponente negiert.
        """
        if abs(self.pos.x) >= BOX_SIZE/2 - RADIUS:
            self.vel.x *= -1
        if abs(self.pos.y) >= BOX_SIZE/2 - RADIUS:
            self.vel.y *= -1
        if abs(self.pos.z) >= BOX_SIZE/2 - RADIUS:
            self.vel.z *= -1

# -------------------------------
# Kollision zwischen Kugeln
# -------------------------------

def collide(b1, b2):
    """
    Verarbeitet die elastische Kollision zwischen zwei Kugeln.
    
    Parameter:
        b1: Erste Kugel (Ball-Objekt)
        b2: Zweite Kugel (Ball-Objekt)
    """
    # Abstand zwischen den beiden Kugeln
    dist = mag(b1.pos - b2.pos)
    
    # Prüfe, ob Kugeln sich berühren und nicht am gleichen Ort sind
    if dist < 2 * RADIUS and dist > 0:
        # Richtungsvektor von b2 zu b1 (normalisiert)
        normal = norm(b1.pos - b2.pos)
        
        # Geschwindigkeitsdifferenz
        rel_vel = b1.vel - b2.vel
        
        # Komponente der Relativgeschwindigkeit in Kollisionsrichtung
        vel_along_normal = dot(rel_vel, normal)
        
        # Wenn Kugeln sich already trennen, nicht kollision verarbeiten
        if vel_along_normal > 0:
            return
        
        # Impulsebtrag (elastische Kollision mit gleicher Masse)
        impulse = normal * vel_along_normal
        
        # Geschwindigkeiten tauschen
        b1.vel -= impulse
        b2.vel += impulse

# -------------------------------
# Kugeln erzeugen
# -------------------------------

balls = [Ball() for _ in range(NUM_BALLS)]  # Liste mit NUM_BALLS Kugel-Objekten

# -------------------------------
# Simulation
# -------------------------------

try:
    while True:
        rate(100)  # 100 Frames pro Sekunde (Simulationsgeschwindigkeit)
        
        # Bewegung: Aktualisiere Position jeder Kugel
        for b in balls:
            b.move()
            b.wall_collision()
        
        # Kollisionen: Prüfe alle Kugel-Paare
        for i in range(NUM_BALLS):
            for j in range(i+1, NUM_BALLS):
                collide(balls[i], balls[j])
except KeyboardInterrupt:
    # Beende die Simulation graceful mit Ctrl+C
    pass