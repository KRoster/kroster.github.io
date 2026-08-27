#!/usr/bin/env python3
"""
Generates the About-page banner for kroster.github.io.

The picture is Kirstin's own subject matter rather than stock decoration: an
ensemble of stochastic epidemic trajectories, simulated with a tau-leaping SIR
model, with a drug-resistant strain seeded later and drawn in the site's accent
red. Dark blue curves are the wild type; red curves are resistance emerging and
spreading through a fraction of the runs.

Output: 2400x600 JPEG on a faint grey ground, quiet on the left where the
profile photo sits.
"""
import pathlib

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

W, H = 2400, 600
DPI = 100

BG_TOP = "#f7f8f9"
BG_BOTTOM = "#e9ebed"
WILD = "#1b3a5c"
RESISTANT = "#f44336"

rng = np.random.default_rng(20260827)


def sir_incidence(beta, gamma, n=20000, i0=8, steps=460, dt=0.25):
    """Tau-leaping stochastic SIR; returns the incidence curve."""
    s, i = n - i0, i0
    out = np.zeros(steps)
    for t in range(steps):
        if i <= 0:
            break
        lam = beta * s * i / n * dt
        rec = gamma * i * dt
        new_inf = min(s, rng.poisson(max(lam, 0)))
        new_rec = min(i, rng.poisson(max(rec, 0)))
        s -= new_inf
        i += new_inf - new_rec
        out[t] = new_inf
    # light smoothing so the lines read as curves, not noise
    k = np.ones(9) / 9
    return np.convolve(out, k, mode="same")


fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()

# --- background gradient ---------------------------------------------------
grad = LinearSegmentedColormap.from_list("bg", [BG_TOP, BG_BOTTOM])
ax.imshow(
    np.linspace(0, 1, 256).reshape(-1, 1),
    aspect="auto",
    cmap=grad,
    extent=[0, 1, 0, 1],
    zorder=0,
)

# --- wild-type ensemble ----------------------------------------------------
curves = []
for _ in range(150):
    beta = rng.uniform(0.30, 0.52)
    gamma = rng.uniform(0.11, 0.17)
    if beta / gamma < 1.6:
        continue
    c = sir_incidence(beta, gamma)
    if c.max() < 20:
        continue
    curves.append(c)

BASE, AMP = 0.16, 0.66
STEPS = 460
x = np.linspace(0, 1, STEPS)
peak = np.percentile([c.max() for c in curves], 97)


def place(c, delay, scale=1.0):
    """Shift a curve right by `delay` steps; nothing is drawn before it starts."""
    y = np.full(STEPS, np.nan)
    seg = c[: STEPS - delay] / peak * scale
    y[delay:] = BASE + np.clip(seg, 0, 1.25) * AMP
    return y


for c in curves:
    ax.plot(
        x,
        place(c, rng.integers(60, 130)),
        color=WILD,
        linewidth=1.0,
        alpha=rng.uniform(0.09, 0.22),
        solid_capstyle="round",
        zorder=2,
    )

# --- resistant strain, seeded later ---------------------------------------
for _ in range(9):
    beta = rng.uniform(0.34, 0.46)
    gamma = rng.uniform(0.12, 0.16)
    c = sir_incidence(beta, gamma, n=20000, i0=3, steps=STEPS)
    if c.max() < 20:
        continue
    ax.plot(
        x,
        place(c, rng.integers(215, 290), scale=rng.uniform(0.45, 0.72)),
        color=RESISTANT,
        linewidth=1.4,
        alpha=rng.uniform(0.30, 0.52),
        solid_capstyle="round",
        zorder=3,
    )

# --- baseline --------------------------------------------------------------
ax.plot([0, 1], [BASE, BASE], color=WILD, linewidth=1.0, alpha=0.20, zorder=4)

# --- calm the left, where the photo and name sit --------------------------
veil = np.linspace(1, 0, 256).reshape(1, -1) ** 1.9
ax.imshow(
    veil,
    aspect="auto",
    cmap=LinearSegmentedColormap.from_list("v", [BG_TOP + "00", BG_TOP]),
    extent=[0, 0.30, 0, 1],
    alpha=0.72,
    zorder=5,
)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
out = pathlib.Path(__file__).resolve().parent.parent / "assets/images/banner.jpg"
fig.savefig(
    out,
    dpi=DPI,
    pil_kwargs={"quality": 90, "optimize": True},
)
print(f"banner written to {out}")
