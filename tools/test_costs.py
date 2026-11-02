"""Consumable cost per person for the D-008 test panel, from data/test_costs.csv.

Usage: python3 tools/test_costs.py   (prints a markdown table)

The panel is built up in stages so the cost driver is visible. Each stage adds items; an item with
only a point value uses it as both low and high. Excludes: devices, staff, shipping, duties, waste,
quality control, pod capital. shortcut: sums prices from different years and price bases (procurement
vs. prices paid vs. study cost); upgrade when one official price list for all items is reachable.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Stage name -> cost row ids added at that stage (one finger-prick lancet per person in the base).
# Dual HIV/syphilis RDT covers both HIV and syphilis (D-008). BP consumables are negligible (C-12).
PANEL = [
    ("RDTs: malaria, dual HIV/syphilis, HBsAg, anti-HCV, + 1 lancet", ["C-01", "C-03", "C-04", "C-05", "C-09"]),
    ("+ blood glucose strip", ["C-07"]),
    ("+ HbA1c POC", ["C-10"]),
    ("+ cholesterol POC", ["C-11"]),
]
WAGES = ["W-01", "W-02"]


def load(path=ROOT / "data/test_costs.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def low_high(r):
    if r["low_usd"] and r["high_usd"]:
        return float(r["low_usd"]), float(r["high_usd"])
    if r["point_usd"]:
        p = float(r["point_usd"])
        return p, p
    raise ValueError(f"{r['id']} has no price")  # never treat a missing price as zero


def stages(rows):
    """Cumulative (stage, low, high) in USD per person."""
    out, lo, hi = [], 0.0, 0.0
    for name, ids in PANEL:
        for i in ids:
            a, b = low_high(rows[i])
            lo, hi = lo + a, hi + b
        out.append((name, lo, hi))
    return out


def main():
    rows = load()
    wages = [(rows[w]["item"].split(", ")[-1], float(rows[w]["point_usd"])) for w in WAGES]
    head = "| Panel (cumulative) | USD per person | " + " | ".join(f"Days' wages, {c}" for c, _ in wages) + " |"
    print(head)
    print("|" + "---|" * (2 + len(wages)))
    for name, lo, hi in stages(rows):
        days = " | ".join(f"{lo / w:.1f}–{hi / w:.1f}" for _, w in wages)
        print(f"| {name} | {lo:.2f}–{hi:.2f} | {days} |")


def plot(out=ROOT / "docs/img/test_costs.png"):
    """Per-item low–high cost per person for the panel, with the lowest day's wages marked."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = load()
    items = [rows[i] for _, ids in PANEL for i in ids]
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    for y, r in enumerate(items):
        lo, hi = low_high(r)
        ax.plot([lo, hi], [y, y], color="#2a6fdb", lw=6, solid_capstyle="round")
        if r["point_usd"]:
            ax.plot(float(r["point_usd"]), y, "o", color="#11366e", ms=6)
        ax.annotate(f"{r['source']}, {r['year']}", (hi, y), xytext=(8, -3), textcoords="offset points",
                    fontsize=7, color="#555")
    for k, w in enumerate(WAGES):
        v = float(rows[w]["point_usd"])
        ax.axvline(v, color="#c9a227", ls="--", lw=1)
        ax.text(v, -0.75 - 0.45 * k, f"1 day's wage, {rows[w]['item'].split(', ')[-1]} (${v})",
                fontsize=7.5, color="#8a6d10", ha="left" if k == 0 else "right")
    ax.set_yticks(range(len(items)), [f"{r['id']} {r['item']}" for r in items], fontsize=8.5)
    ax.set_xscale("log")
    ax.set_xlabel("USD per test (log scale); bar = low–high, dot = median/average/point value")
    lo, hi = stages(rows)[-1][1:]
    ax.set_title(f"MedPod D-008 panel: consumables {lo:.2f}–{hi:.2f} USD per person (Draft)\n"
                 "WHO reports (IRIS) and peer-reviewed papers (PMC); mixed years and price bases",
                 fontsize=10, loc="left")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xlim(0.005, 200)
    ax.set_ylim(len(items) - 0.5, -1.4)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(out)


if __name__ == "__main__":
    main()
    plot()
