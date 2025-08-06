import numpy as np
import matplotlib.pyplot as plt

# --- Styling for "top academic" look with dark background ---
plt.style.use("dark_background")
plt.rcParams.update({
    "figure.dpi": 160,
    "savefig.dpi": 300,
    "font.size": 12,
    "axes.labelsize": 14,
    "axes.titlesize": 16,
    "legend.fontsize": 10,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "axes.linewidth": 1.0,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "mathtext.fontset": "stix",
    "font.family": "STIXGeneral",
})

# --- Physical constants and model ---
G = 4.302e-6  # kpc * (km/s)^2 / Msun
c = 3.0e5     # km/s

def v_fdft_components(r, M_bar, kappa, lam):
    v_newton = np.sqrt(G * M_bar / r)
    v_psi = np.sqrt((kappa * c**2 * r / 2.0) * (1.0 - np.exp(-r / lam)))
    v_tot = np.sqrt(v_newton**2 + v_psi**2)
    return v_tot, v_newton, v_psi

# --- Radius grid ---
r = np.linspace(0.5, 50, 600)  # kpc

# --- Galaxy parameters ---
galaxies = {
    "DF44":       {"M_bar": 3e8,   "kappa": 0.03, "lambda": 1.5, "color": "#4dabf7"},
    "NGC 1277":   {"M_bar": 1.2e11,"kappa": 0.10, "lambda": 1.5, "color": "#ff6b6b"},
    "Milky Way":  {"M_bar": 6e10,  "kappa": 0.08, "lambda": 1.5, "color": "#69db7c"},
}

# --- Plot ---
fig, ax = plt.subplots(figsize=(9.5, 6.5))

comp_styles = {
    "total":   {"lw": 2.8, "alpha": 0.95},
    "newton":  {"lw": 1.3, "alpha": 0.8, "ls": "--"},
    "psi":     {"lw": 1.6, "alpha": 0.95, "ls": ":"},
}

for name, p in galaxies.items():
    v_tot, v_newt, v_psi = v_fdft_components(r, p["M_bar"], p["kappa"], p["lambda"])
    ax.plot(r, v_tot, color=p["color"], **comp_styles["total"], label=f"{name}: total")
    ax.plot(r, v_newt, color=p["color"], **comp_styles["newton"])
    ax.plot(r, v_psi, color=p["color"], **comp_styles["psi"])

# Axes labels and limits
ax.set_title("Galactic Rotation Curves in FDFT", pad=12)
ax.set_xlabel("Radius  [kpc]")
ax.set_ylabel("Circular velocity  [km s$^{-1}$]")
ax.set_xlim(0, 50)
ax.set_ylim(0, 340)

# Grid and minor ticks
ax.grid(True)
ax.minorticks_on()
ax.tick_params(axis="both", which="both", direction="in", top=True, right=True)

# Legends
gal_legend_lines = [plt.Line2D([0], [0], color=p["color"], lw=2.8) for p in galaxies.values()]
gal_legend_labels = list(galaxies.keys())
leg1 = ax.legend(gal_legend_lines, gal_legend_labels, loc="upper left", frameon=False, title="Galaxies", labelcolor="white")

comp_lines = [
    plt.Line2D([0], [0], color="white", lw=2.8, ls="-"),
    plt.Line2D([0], [0], color="white", lw=1.3, ls="--"),
    plt.Line2D([0], [0], color="white", lw=1.6, ls=":"),
]
leg2 = ax.legend(comp_lines, ["total", "Newtonian", "Ψ-field"], loc="lower right", frameon=False, title="Components", labelcolor="white")
ax.add_artist(leg1)

# Annotations
ax.text(41, 270, "NGC 1277", color=galaxies["NGC 1277"]["color"], fontsize=11)
ax.text(41, 170, "Milky Way", color=galaxies["Milky Way"]["color"], fontsize=11)
ax.text(41, 60,  "DF44",      color=galaxies["DF44"]["color"], fontsize=11)

# Save figure to file
out_path = "section6_fdft_rotation_curves_dark.png"
plt.tight_layout()
plt.savefig(out_path, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()
