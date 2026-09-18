"""Génère les figures de la partie 03 - Classification et séparations linéaires.
Usage: uv run --with matplotlib --with numpy python scripts/generer_figures_03.py
Sorties: assets/03-geometrie-hyperplan.png, 03-exemple-OU.png, 03-exemple-ET.png, 03-exemple-XOR.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "assets")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3})

# 1. Lecture géométrique : hyperplan, w normal, exemple (2,0)
fig, ax = plt.subplots(figsize=(5.5, 4.5))
xs = np.linspace(-0.5, 2.5, 100)
ax.plot(xs, xs, "k-", linewidth=2, label="frontière $w^Tx+b=0$")
xx, yy = np.meshgrid(np.linspace(-0.5, 2.5, 200), np.linspace(-0.5, 2.5, 200))
Z = 1 * xx - 1 * yy
ax.contourf(xx, yy, Z, levels=[-10, 0, 10], colors=["#cfe0ff", "#ffd9c9"], alpha=0.5)
ax.text(0.0, 1.9, "côté −1\n($h<0$)", fontsize=9)
ax.text(1.7, 0.55, "côté +1\n($h>0$)", fontsize=9)
ax.annotate("", xy=(1.5, 0.8), xytext=(1.15, 1.15),
            arrowprops=dict(facecolor="black", shrink=0.05, width=1.5, headwidth=7))
ax.text(1.55, 0.65, "$w$ (normal)", fontsize=10)
ax.plot(2.0, 0.0, "o", color="red", markersize=8)
ax.text(1.55, -0.3, "$(2,0)$ → +1", fontsize=9)
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.5, 2.5)
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.set_title("Séparation linéaire : $w=(1,-1)$, $b=0$")
ax.legend(loc="upper left", fontsize=8)
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "03-geometrie-hyperplan.png"), dpi=150)
print("ok 03-geometrie-hyperplan.png")


def plot_logic(points, labels, w, b, title, fname, note=""):
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    pts = np.array(points)
    labs = np.array(labels)
    pos = pts[labs == 1]
    neg = pts[labs == -1]
    ax.scatter(pos[:, 0], pos[:, 1], s=120, marker="o", label="classe +1",
               edgecolors="k", color="#e67e22", zorder=3)
    ax.scatter(neg[:, 0], neg[:, 1], s=120, marker="s", label="classe −1",
               edgecolors="k", color="#3498db", zorder=3)
    for (x1, x2), y in zip(points, labels):
        ax.text(x1 + 0.06, x2 + 0.06, f"({x1},{x2})", fontsize=8)
    xs = np.linspace(-0.6, 1.6, 100)
    if abs(w[1]) > 1e-9:
        ys = -(w[0] * xs + b) / w[1]
        ax.plot(xs, ys, "k--", linewidth=2, label=f"frontière $w={tuple(w)}, b={b}$")
    xx, yy = np.meshgrid(np.linspace(-0.6, 1.6, 200), np.linspace(-0.6, 1.6, 200))
    Z = w[0] * xx + w[1] * yy + b
    ax.contourf(xx, yy, Z, levels=[-10, 0, 10], colors=["#cfe0ff", "#ffd9c9"], alpha=0.35)
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title(title)
    if note:
        ax.text(0.5, -0.35, note, ha="center", fontsize=8, style="italic")
    ax.legend(fontsize=8, loc="best")
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=150)
    print("ok", fname)


plot_logic([(0, 0), (0, 1), (1, 0), (1, 1)], [-1, 1, 1, 1],
           w=(1, 1), b=-0.5, title="OU logique : séparable",
           fname="03-exemple-OU.png")
plot_logic([(0, 0), (0, 1), (1, 0), (1, 1)], [-1, -1, -1, 1],
           w=(1, 1), b=-1.5, title="ET logique : séparable",
           fname="03-exemple-ET.png")
plot_logic([(0, 0), (1, 1), (0, 1), (1, 0)], [-1, -1, 1, 1],
           w=(1, 1), b=-0.5, title="XOR : non séparable (droite en échec)",
           fname="03-exemple-XOR.png",
           note="aucune droite ne sépare ○ et ■")
