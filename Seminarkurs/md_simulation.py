import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ============================================================
# 2D MD Simulation
# Speichert Ergebnis als GIF
# ============================================================

NUM_BALLS = 100
BOX_SIZE = 100
BALL_RADIUS = 1.0
DT = 1.0
FRAMES = 200

np.random.seed(42)

# ------------------------------------------------
# Positionen
# ------------------------------------------------
positions = np.random.uniform(
    BALL_RADIUS,
    BOX_SIZE - BALL_RADIUS,
    (NUM_BALLS, 2)
)

# ------------------------------------------------
# Geschwindigkeiten
# ------------------------------------------------
velocities = np.random.uniform(
    -2,
    2,
    (NUM_BALLS, 2)
)

# ------------------------------------------------
# Massen
# ------------------------------------------------
masses = np.random.uniform(1, 5, NUM_BALLS)

# ============================================================
# Wandkollisionen
# ============================================================

def handle_wall_collisions():

    for i in range(NUM_BALLS):

        # X-Richtung
        if positions[i, 0] <= BALL_RADIUS:
            positions[i, 0] = BALL_RADIUS
            velocities[i, 0] *= -1

        elif positions[i, 0] >= BOX_SIZE - BALL_RADIUS:
            positions[i, 0] = BOX_SIZE - BALL_RADIUS
            velocities[i, 0] *= -1

        # Y-Richtung
        if positions[i, 1] <= BALL_RADIUS:
            positions[i, 1] = BALL_RADIUS
            velocities[i, 1] *= -1

        elif positions[i, 1] >= BOX_SIZE - BALL_RADIUS:
            positions[i, 1] = BOX_SIZE - BALL_RADIUS
            velocities[i, 1] *= -1


# ============================================================
# Elastische Kugelstöße
# ============================================================

def handle_ball_collisions():

    for i in range(NUM_BALLS):

        for j in range(i + 1, NUM_BALLS):

            delta = positions[j] - positions[i]
            distance = np.linalg.norm(delta)

            if distance < 2 * BALL_RADIUS and distance > 0:

                normal = delta / distance

                relative_velocity = velocities[i] - velocities[j]

                velocity_normal = np.dot(relative_velocity, normal)

                if velocity_normal > 0:
                    continue

                m1 = masses[i]
                m2 = masses[j]

                impulse = (2 * velocity_normal) / (m1 + m2)

                velocities[i] -= impulse * m2 * normal
                velocities[j] += impulse * m1 * normal

                # Überlappung korrigieren
                overlap = 2 * BALL_RADIUS - distance

                positions[i] -= normal * overlap / 2
                positions[j] += normal * overlap / 2


# ============================================================
# Simulationsschritt
# ============================================================

def update(frame):

    global positions

    # Positionen aktualisieren
    positions += velocities * DT

    # Kollisionen
    handle_wall_collisions()
    handle_ball_collisions()

    # Neue Positionen zeichnen
    scatter.set_offsets(positions)

    return scatter,


# ============================================================
# Plot
# ============================================================

fig, ax = plt.subplots(figsize=(8, 8))

scatter = ax.scatter(
    positions[:, 0],
    positions[:, 1],
    s=masses * 30,
    c=masses,
    cmap="plasma"
)

ax.set_xlim(0, BOX_SIZE)
ax.set_ylim(0, BOX_SIZE)

ax.set_title("2D MD Simulation")
ax.grid(True)

# ============================================================
# Animation erzeugen
# ============================================================

ani = FuncAnimation(
    fig,
    update,
    frames=FRAMES,
    interval=100
)

# ============================================================
# GIF speichern
# ============================================================

writer = PillowWriter(fps=10)

ani.save("md_simulation.gif", writer=writer)

print("Animation gespeichert als md_simulation.gif")