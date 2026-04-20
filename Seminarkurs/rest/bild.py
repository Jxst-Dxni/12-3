from PIL import Image, ImageDraw
import random

# Bildgröße
WIDTH, HEIGHT = 800, 600

# Neues schwarzes Bild
image = Image.new("RGB", (WIDTH, HEIGHT), "black")
draw = ImageDraw.Draw(image)

# Kugeln zeichnen
NUM_BALLS = 15

for _ in range(NUM_BALLS):
    radius = random.randint(8, 15)
    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)

    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="white")

# Bild speichern
image.save("md_simulation.png")

print("Bild gespeichert als md_simulation.png")