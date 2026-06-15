import pygame
import numpy as np
import sys              #sys = system

# --- 1. CONFIGURATION / PARAMETER ---
WIDTH = 800
HEIGHT = 600
NUM_PARTICLES = 30
RADIUS = 15
SPEED_SCALE = 3.0  # Multiplikator für die Startgeschwindigkeit

# Farben (RGB)
BACKGROUND_COLOR = (240, 240, 240)  # Hellgrau
PARTICLE_COLOR = (74, 144, 226)     # Blau
BORDER_COLOR = (53, 122, 189)       # Dunkelblau für den Rand der Kreise

class Simulation2D:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2D Molecular Dynamics Simulation (Pygame & NumPy)")
        self.clock = pygame.time.Clock()
        
        # --- 2. NUMPY ARRAYS INITIALISIEREN ---
        # Positionen: Zufällige X und Y Werte innerhalb der Wände (N, 2) Array
        self.positions = np.random.uniform(RADIUS, [WIDTH - RADIUS, HEIGHT - RADIUS], size=(NUM_PARTICLES, 2))
        
        # Geschwindigkeiten: Zufällige Vektoren zwischen -1 und 1, skaliert (N, 2) Array
        self.velocities = np.random.uniform(-1.0, 1.0, size=(NUM_PARTICLES, 2)) * SPEED_SCALE
        
        self.radius = RADIUS

    def update(self):
        # 3.2 & 3.5 Translationsphase mittels NumPy Vektoraddition
        self.positions += self.velocities

        # 3.3 Wandkollisionen über NumPy Masken (hocheffizient)
        # Linke und rechte Wand
        out_of_bounds_x = (self.positions[:, 0] - self.radius <= 0) | (self.positions[:, 0] + self.radius >= WIDTH)
        self.velocities[out_of_bounds_x, 0] *= -1
        # Korrektur, damit Teilchen nicht außerhalb der Wand zittern
        self.positions[self.positions[:, 0] - self.radius < 0, 0] = self.radius
        self.positions[self.positions[:, 0] + self.radius > WIDTH, 0] = WIDTH - self.radius

        # Obere und untere Wand
        out_of_bounds_y = (self.positions[:, 1] - self.radius <= 0) | (self.positions[:, 1] + self.radius >= HEIGHT)
        self.velocities[out_of_bounds_y, 1] *= -1
        # Korrektur
        self.positions[self.positions[:, 1] - self.radius < 0, 1] = self.radius
        self.positions[self.positions[:, 1] + self.radius > HEIGHT, 1] = HEIGHT - self.radius

        # 3.4 Teilchenkollisionen paarweise prüfen
        for i in range(NUM_PARTICLES):
            for j in range(i + 1, NUM_PARTICLES):
                # Vektor zwischen zwei Teilchen berechnen
                delta = self.positions[i] - self.positions[j]
                # Euklidischen Abstand berechnen mit NumPy (Satz des Pythagoras)
                distance = np.linalg.norm(delta)
                
                # Wenn der Abstand kleiner als der doppelte Radius ist -> Kollision!
                if distance <= (2 * self.radius):
                    # Überlappung korrigieren, um Festkleben zu verhindern
                    overlap = (2 * self.radius) - distance
                    if distance == 0:
                        distance = 0.1
                    direction = delta / distance
                    self.positions[i] += direction * (overlap / 2)
                    self.positions[j] -= direction * (overlap / 2)
                    
                    # --- DER ALGORITHMISCHE GESCHWINDIGKEITSAUSTAUSCH ---
                    # Wie im Dokument definiert: Vektoren der beiden Teilchen tauschen
                    # NumPy erlaubt das gleichzeitige Tauschen in einer Zeile:
                    self.velocities[i], self.velocities[j] = self.velocities[j].copy(), self.velocities[i].copy()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Alle Teilchen auf das Pygame-Fenster zeichnen [1]
        for i in range(NUM_PARTICLES):
            pos_x = int(self.positions[i, 0])
            pos_y = int(self.positions[i, 1])
            
            # Hauptkreis (Blau) [1]
            pygame.draw.circle(self.screen, PARTICLE_COLOR, (pos_x, pos_y), self.radius)
            # Rand des Kreises (Dunkelblau für bessere Optik) [1]
            pygame.draw.circle(self.screen, BORDER_COLOR, (pos_x, pos_y), self.radius, 1)
            
        pygame.display.flip()

    def run(self):
        # Hauptschleife von Pygame [1]
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            self.update()
            self.draw()
            self.clock.tick(60)  # Begrenzt die Simulation auf flüssige 60 Bilder pro Sekunde [1]
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    sim = Simulation2D()
    sim.run()