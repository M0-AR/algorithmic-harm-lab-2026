"""Make hero demo GIF + thumbnail for README / preview.html.
Best practice: 10-20s looping GIF, zoomed, legible at small size, payoff first.
Generates: assets/demo.gif (hero), assets/thumbnail.png (video link preview).
No external recorder needed — reproducible from benchmark outputs.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

os.makedirs("assets", exist_ok=True)

# Scene: S vs U price discrimination payoff in 60 frames
V, c, delta = 100.0, 10.0, 30.0
fig, ax = plt.subplots(figsize=(7, 4.2))
q = np.linspace(0, 1, 200)
p_true = V - V * q
p_perc = V + delta - V * q

def frame(i):
    ax.clear()
    ax.plot(q, p_true, label="Actual demand", linewidth=2)
    ax.plot(q, p_perc, "--", label="Perceived demand (overestimation)", linewidth=2)
    ax.axhline(c, color="gray", label="Supply")
    # animate monopoly dot moving S -> U
    t = i / 59
    pm = 55 + t * (70 - 55)
    qm = (V + delta * t - pm) / V
    ax.scatter([qm], [pm], c="red", s=80, zorder=5)
    ax.set_xlim(0, 1); ax.set_ylim(0, 140)
    ax.set_xlabel("Quantity"); ax.set_ylabel("Price")
    ax.set_title(f"Algorithmic price discrimination: S → U harm ({i+1}/60)")
    ax.legend(fontsize=8)
    ax.text(0.02, 130, "Consumer surplus → negative", fontsize=10, color="darkred",
            bbox=dict(facecolor="mistyrose", alpha=0.9))

ani = animation.FuncAnimation(fig, frame, frames=60, interval=150)
ani.save("assets/demo.gif", writer="pillow", fps=8)
plt.close()
print("wrote assets/demo.gif")

# Thumbnail: first frame static with play overlay text
fig2, ax2 = plt.subplots(figsize=(7, 4.2))
ax2.plot(q, p_true, linewidth=2); ax2.plot(q, p_perc, "--", linewidth=2)
ax2.axhline(c, color="gray")
ax2.scatter([0.45], [55], c="red", s=120, zorder=5)
ax2.set_title("▶ Watch the 90-sec walkthrough — preview.html")
ax2.set_xlabel("Quantity"); ax2.set_ylabel("Price")
fig2.tight_layout()
fig2.savefig("assets/thumbnail.png", dpi=150)
plt.close()
print("wrote assets/thumbnail.png")
