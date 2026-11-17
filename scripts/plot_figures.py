#!/usr/bin/env python3
"""Generate figures for PAPER.md from evidence/*.jsonl (CPU only)."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "evidence"
FIG = ROOT / "figures"


def load(name: str) -> list[dict]:
    return [json.loads(x) for x in (EV / name).read_text().splitlines() if x.strip()]


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    p1 = load("phase1_calibration_900.jsonl")
    p3 = load("phase3_thinkcap_150.jsonl")
    tr20_s1 = [r for r in p1 if r["arm"] == "tr20" and r["seed"] == 1]

    # Figure 1: Phase 1 WT rates
    blocks = [
        ("d69", [r for r in p1 if r["arm"] == "d69"]),
        ("tr20 s0", [r for r in p1 if r["arm"] == "tr20" and r["seed"] == 0]),
        ("tr20 s1", tr20_s1),
        ("scale10", [r for r in p1 if r["arm"] == "scale10"]),
    ]
    labels = [b[0] for b in blocks]
    rates = [100 * sum(r["pass"] for r in rows) / len(rows) for _, rows in blocks]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar(labels, rates, color="#4C78A8")
    ax.set_ylabel("Working-tree pass (%)")
    ax.set_ylim(0, 40)
    ax.set_title("Phase 1 calibration (150 tasks)")
    ax.axhline(31, color="#333", lw=0.8, ls="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(FIG / "fig1_phase1_wt_rates.png", dpi=150)
    plt.close(fig)

    # Figure 2: thinking over 1024
    fig, ax = plt.subplots(figsize=(5, 3.2))
    ax.bar(
        ["think-1024", "tr20 s1 (4096)"],
        [sum(1 for r in p3 if r.get("thoughts_gt_1024")), sum(1 for r in tr20_s1 if r.get("thoughts_gt_1024"))],
        color=["#F58518", "#4C78A8"],
    )
    ax.set_ylabel("Episodes with a turn >1024 reasoning tokens")
    ax.set_title("Phase 3 behavioral change")
    fig.tight_layout()
    fig.savefig(FIG / "fig2_thoughts_over_1024.png", dpi=150)
    plt.close(fig)

    # Figure 3: paired flip matrix counts
    base = {r["task_id"]: r["pass"] for r in tr20_s1}
    a1 = {r["task_id"]: r["pass"] for r in p3}
    mat = np.zeros((2, 2), dtype=int)
    for tid in base:
        mat[int(base[tid]), int(a1[tid])] += 1
    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    im = ax.imshow(mat, cmap="Blues")
    ax.set_xticks([0, 1], ["fail@1024", "pass@1024"])
    ax.set_yticks([0, 1], ["fail@4096", "pass@4096"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(mat[i, j]), ha="center", va="center", color="black")
    ax.set_title("Phase 3 paired outcomes")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_phase3_paired.png", dpi=150)
    plt.close(fig)

    print(f"wrote figures to {FIG}")


if __name__ == "__main__":
    main()
