"""2D-MD-Simulation harter Scheiben.

Dieses Skript simuliert elastische Kollisionen zwischen vielen identischen,
starren Scheiben in einer quadratischen Box. Jeder Teilchen besitzt eine 2D-
Position, eine 2D-Geschwindigkeit und einen Radius. Die Wandkollisionen und
die paarweisen Zusammenstöße werden elastisch behandelt.
"""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle


@dataclass
class Particle:
    position: np.ndarray
    velocity: np.ndarray
    radius: float

    def move(self, dt: float) -> None:
        self.position += self.velocity * dt


class MDSimulation2D:
    def __init__(
        self,
        num_particles: int = 20,
        radius: float = 0.3,
        width: float = 12.0,
        height: float = 8.0,
        temperature: float = 1.0,
    ):
        self.num_particles = num_particles
        self.radius = radius
        self.width = width
        self.height = height
        self.temperature = temperature
        self.particles: List[Particle] = []
        self._initialize_particles()

    def _initialize_particles(self) -> None:
        max_attempts = 2000
        for _ in range(self.num_particles):
            for attempt in range(max_attempts):
                position = np.array(
                    [
                        random.uniform(self.radius, self.width - self.radius),
                        random.uniform(self.radius, self.height - self.radius),
                    ],
                    dtype=float,
                )
                if self._is_valid_position(position):
                    speed = math.sqrt(self.temperature)
                    velocity = np.array(
                        [random.uniform(-1.0, 1.0) for _ in range(2)],
                        dtype=float,
                    )
                    norm = np.linalg.norm(velocity)
                    if norm == 0:
                        velocity = np.array([1.0, 0.0], dtype=float)
                        norm = 1.0
                    velocity = speed * velocity / norm
                    self.particles.append(Particle(position, velocity, self.radius))
                    break
            else:
                raise RuntimeError(
                    "Konnte keine freie Startposition für alle Teilchen finden."
                )

    def _is_valid_position(self, position: np.ndarray) -> bool:
        for particle in self.particles:
            distance = np.linalg.norm(position - particle.position)
            if distance < 2 * self.radius:
                return False
        return True

    def step(self, dt: float) -> None:
        for particle in self.particles:
            particle.move(dt)
            self._handle_wall_collision(particle)
        self._handle_particle_collisions()

    def _handle_wall_collision(self, particle: Particle) -> None:
        if particle.position[0] - particle.radius < 0:
            particle.position[0] = particle.radius
            particle.velocity[0] *= -1
        elif particle.position[0] + particle.radius > self.width:
            particle.position[0] = self.width - particle.radius
            particle.velocity[0] *= -1

        if particle.position[1] - particle.radius < 0:
            particle.position[1] = particle.radius
            particle.velocity[1] *= -1
        elif particle.position[1] + particle.radius > self.height:
            particle.position[1] = self.height - particle.radius
            particle.velocity[1] *= -1

    def _handle_particle_collisions(self) -> None:
        for i in range(self.num_particles):
            for j in range(i + 1, self.num_particles):
                self._resolve_collision(self.particles[i], self.particles[j])

    def _resolve_collision(self, p1: Particle, p2: Particle) -> None:
        delta = p2.position - p1.position
        distance = np.linalg.norm(delta)
        min_dist = p1.radius + p2.radius
        if distance == 0 or distance >= min_dist:
            return

        normal = delta / distance
        relative_velocity = p1.velocity - p2.velocity
        speed_along_normal = np.dot(relative_velocity, normal)
        if speed_along_normal >= 0:
            return

        impulse = -2 * speed_along_normal / 2.0
        p1.velocity += impulse * normal
        p2.velocity -= impulse * normal

        overlap = min_dist - distance
        correction = normal * (overlap / 2.0)
        p1.position -= correction
        p2.position += correction

    def positions(self) -> np.ndarray:
        return np.array([particle.position for particle in self.particles])

    def kinetic_energy(self) -> float:
        return 0.5 * sum(np.dot(p.velocity, p.velocity) for p in self.particles)

    def run(self, dt: float, steps: int, animate: bool = False) -> None:
        if animate:
            self._animate(dt, steps)
            return
        for _ in range(steps):
            self.step(dt)

    def _animate(self, dt: float, steps: int) -> None:
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor("black")
        ax.set_facecolor("black")
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect("equal")
        ax.set_xlabel("x", color="white")
        ax.set_ylabel("y", color="white")
        ax.tick_params(colors="white")
        border = Rectangle((0, 0), self.width, self.height, edgecolor="white", facecolor="black", lw=2)
        ax.add_patch(border)
        scatter = ax.scatter([], [], s=(self.radius * 1500), c="white")

        def update(frame: int):
            self.step(dt)
            pos = self.positions()
            scatter.set_offsets(pos)
            ax.set_title(f"Frame {frame + 1}/{steps}", color="white")
            return scatter,

        FuncAnimation(fig, update, frames=steps, interval=25, blit=True)
        plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="2D MD-Simulation harter Scheiben in einem schwarzen Rechteck"
    )
    parser.add_argument("--num", type=int, default=20, help="Anzahl der Teilchen")
    parser.add_argument("--radius", type=float, default=0.3, help="Radius jeder Scheibe")
    parser.add_argument("--width", type=float, default=12.0, help="Breite des Rechtecks")
    parser.add_argument("--height", type=float, default=8.0, help="Höhe des Rechtecks")
    parser.add_argument("--dt", type=float, default=0.01, help="Zeitschrittweite")
    parser.add_argument("--steps", type=int, default=500, help="Anzahl der Simulationsschritte")
    parser.add_argument("--animate", action="store_true", help="Zeige die Simulation als Animation")
    parser.add_argument("--seed", type=int, default=None, help="Zufallsseed für reproduzierbare Ergebnisse")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    sim = MDSimulation2D(
        num_particles=args.num,
        radius=args.radius,
        width=args.width,
        height=args.height,
        temperature=1.0,
    )
    sim.run(dt=args.dt, steps=args.steps, animate=args.animate)

    if not args.animate:
        print(f"Simulation abgeschlossen: {args.steps} Schritte")
        print(f"Kinetische Energie: {sim.kinetic_energy():.3f}")
        print("Letzte Positionen und Geschwindigkeiten der ersten 5 Teilchen:")
        for idx, particle in enumerate(sim.particles[:5], start=1):
            print(
                f"Teilchen {idx}: pos={particle.position.round(3)} vel={particle.velocity.round(3)}"
            )


if __name__ == "__main__":
    main()
