"""Render data/test_menu.csv as a one-page picture: docs/img/test_menu.png.

Usage: python3 tools/plot_test_menu.py
"""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
METHODS = ["pod sensor", "cartridge reader", "handheld analyser", "refer", "out of scope"]
COLOR = {"A": "#2a6fdb", "B": "#7fa8e8", "C": "#c9a227", "-": "#b0b0b0"}
LABEL = {"A": "A: top-10 cause of death in LIC/LMIC (GHE 2021) + WHO EDL non-lab test",
         "B": "B: WHO EDL non-lab test, burden rank pending (GHE DALYs not fetched)",
         "C": "C: top-10 cause, no IVD: pod sensor or referral (Draft)",
         "-": "Out of scope"}


def main():
    with open(ROOT / "data/test_menu.csv", newline="", encoding="utf-8") as f:
        menu = list(csv.DictReader(f))
    n = len(menu)
    fig, ax = plt.subplots(figsize=(11, 0.36 * n + 2.2))
    for y, m in enumerate(menu):
        x = METHODS.index(m["pod_method"])
        ax.scatter(x, y, s=260, color=COLOR[m["priority"]], zorder=3,
                   marker="o" if m["edl5_ids"] else "D")
        if m["edl5_ids"]:
            ax.annotate("EDL " + m["edl5_ids"].replace(";", ","), (x, y), xytext=(14, -3),
                        textcoords="offset points", fontsize=7, color="#444")
    ax.set_yticks(range(n), [m["condition"] for m in menu], fontsize=8.5)
    ax.set_xticks(range(len(METHODS)), METHODS, fontsize=9)
    ax.set_xlim(-0.5, len(METHODS) - 0.2)
    ax.invert_yaxis()
    ax.grid(color="#e5e5e5", zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    handles = [plt.Line2D([], [], marker="o", ls="", color=COLOR[k], markersize=9, label=v)
               for k, v in LABEL.items()]
    handles.append(plt.Line2D([], [], marker="D", ls="", color="#888", markersize=7,
                              label="diamond = no EDL test (Draft or out of scope)"))
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.42, -0.06 - 1.2 / n),
              fontsize=8, frameon=False, ncol=1)
    ax.set_title("MedPod test menu v0.1 (Draft): condition × pod method\n"
                 "Sources: WHO EDL 5 (e-EDL, fetched 2026-11-02); WHO GHE 2021 via WHS 2024 Fig. 1.9",
                 fontsize=10, loc="left")
    fig.tight_layout()
    out = ROOT / "docs/img/test_menu.png"
    fig.savefig(out, dpi=130)
    print(out)


if __name__ == "__main__":
    main()
