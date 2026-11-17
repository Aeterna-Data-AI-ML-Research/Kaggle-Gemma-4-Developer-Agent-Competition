#!/usr/bin/env python3
"""Recompute PAPER.md tables + bootstrap CIs from evidence/*.jsonl only.

Usage:
  pip install -r requirements.txt
  python scripts/reproduce_all_tables.py

Exits non-zero if any pinned claim fails. Laptop CPU; target < 5 seconds.
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "evidence"
BENCH = ROOT / "benchmark"
CUTOFF_S = 420.0
N_BOOT = 10_000
BOOT_SEED = 0

# Pinned claims from PAPER.md (Sections 4–8). Tolerances are absolute.
EXPECTED = {
    "n_phase1": 900,
    "n_phase2": 300,
    "n_phase3": 150,
    "n_calib": 150,
    "n_test": 150,
    "n_train": 426,
    "n_holdout": 4,
    "phase1": {
        "d69": {"wt": 93, "n": 300, "strict": 58},
        "tr20_s0": {"wt": 47, "n": 150, "strict": 27},
        "tr20_s1": {"wt": 48, "n": 150, "strict": 22},
        "scale10": {"wt": 91, "n": 300, "strict": 47},
    },
    "phase2": {
        "P2_A": {"wt": 50, "n": 150, "strict": 35},
        "P2_B": {"wt": 48, "n": 150, "strict": 31},
    },
    "phase3": {
        "a1": {"wt": 48, "n": 150, "strict": 28},
        "delta_vs_tr20_s1": 0.0,
        "flips_up": 9,
        "flips_down": 9,
        "thoughts_gt_1024_a1": 3,
        "thoughts_gt_1024_base": 63,
        "time_budget_a1": 77,
        "time_budget_base": 85,
        "submitted_a1": 45,
        "submitted_base": 34,
    },
    "oracle_pass_at_6_rate": 0.44,  # ~44% reported; allow ±0.02
}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def expand_turn(t: list) -> dict:
    return {
        "turn_idx": t[0],
        "virtual_sec_start": t[1],
        "virtual_sec_end": t[2],
        "reasoning_tokens": t[3],
        "content_tokens": t[4],
        "tool_name": t[5],
        "target_is_gold_file": bool(t[6]),
        "exit_code": t[7],
    }


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_manifest() -> None:
    lines = (EV / "manifest.sha256").read_text().splitlines()
    for line in lines:
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        path = ROOT / rel
        got = sha256_file(path)
        if got != digest:
            raise AssertionError(f"manifest mismatch {rel}: {got} != {digest}")


def boot_ci(diffs: list[float], n: int = N_BOOT, seed: int = BOOT_SEED) -> list[float]:
    rng = random.Random(seed)
    k = len(diffs)
    means = sorted(sum(diffs[rng.randrange(k)] for _ in range(k)) / k for _ in range(n))
    return [round(means[int(0.025 * n)], 4), round(means[int(0.975 * n) - 1], 4)]


def mean_virtual(rows: list[dict]) -> float:
    return sum(r["virtual_seconds"] for r in rows) / len(rows)


def thoughts_over(row: dict, cap: int = 1024) -> bool:
    if "thoughts_gt_1024" in row and cap == 1024:
        return bool(row["thoughts_gt_1024"])
    return any(expand_turn(t)["reasoning_tokens"] > cap for t in row.get("turn_summary") or [])


def failure_bucket(row: dict) -> str | None:
    """Approx of p752_common.failure_bucket using compact fields only."""
    unsubmitted_timeout = row["end_reason"] == "time_budget" and not row.get("patch_submitted")
    if row["pass"] and not unsubmitted_timeout:
        return None
    if unsubmitted_timeout:
        return "timeout_unsubmitted_with_diff" if row.get("patch_chars", 0) > 0 else "timeout_empty_diff"
    return "other"


def main() -> int:
    t0 = time.perf_counter()
    verify_manifest()
    p1 = load_jsonl(EV / "phase1_calibration_900.jsonl")
    p2 = load_jsonl(EV / "phase2_guards_300.jsonl")
    p3 = load_jsonl(EV / "phase3_thinkcap_150.jsonl")
    tasks = load_jsonl(BENCH / "tasks_manifest.jsonl")

    assert len(p1) == EXPECTED["n_phase1"]
    assert len(p2) == EXPECTED["n_phase2"]
    assert len(p3) == EXPECTED["n_phase3"]
    by_split = Counter(t["split"] for t in tasks)
    assert by_split["calib"] == EXPECTED["n_calib"]
    assert by_split["test"] == EXPECTED["n_test"]
    assert by_split["train"] == EXPECTED["n_train"]
    assert by_split["holdout"] == EXPECTED["n_holdout"]

    def sel(rows, **kw):
        out = rows
        for k, v in kw.items():
            out = [r for r in out if r.get(k) == v]
        return out

    d69 = sel(p1, arm="d69")
    tr20_s0 = sel(p1, arm="tr20", seed=0)
    tr20_s1 = sel(p1, arm="tr20", seed=1)
    scale10 = sel(p1, arm="scale10")
    p2a = sel(p2, harness_arm="P2_A")
    p2b = sel(p2, harness_arm="P2_B")

    def check_block(name, rows, exp):
        wt = sum(1 for r in rows if r["pass"])
        strict = sum(1 for r in rows if r["strict_pass"])
        assert len(rows) == exp["n"], (name, len(rows), exp["n"])
        assert wt == exp["wt"], (name, "wt", wt, exp["wt"])
        assert strict == exp["strict"], (name, "strict", strict, exp["strict"])
        rate = 100.0 * wt / len(rows)
        print(f"  {name:12s} WT {wt}/{len(rows)} = {rate:.1f}%  strict {strict}/{len(rows)}")

    print("Section 4 — Phase 1 calibration")
    check_block("d69", d69, EXPECTED["phase1"]["d69"])
    check_block("tr20_s0", tr20_s0, EXPECTED["phase1"]["tr20_s0"])
    check_block("tr20_s1", tr20_s1, EXPECTED["phase1"]["tr20_s1"])
    check_block("scale10", scale10, EXPECTED["phase1"]["scale10"])
    print(f"  mean virtual s: d69={mean_virtual(d69):.1f} tr20_s0={mean_virtual(tr20_s0):.1f} "
          f"tr20_s1={mean_virtual(tr20_s1):.1f} scale10={mean_virtual(scale10):.1f}")

    # Paired task bootstrap: tr20_s1 - d69 mean, tr20 pooled - d69, scale10 - d69
    task_ids = sorted({r["task_id"] for r in p1})
    by = {(r["task_id"], r["arm"], int(r["seed"])): r for r in p1}

    def task_rate(arm_seeds):
        # arm_seeds: list of (arm, seed)
        out = {}
        for tid in task_ids:
            vals = [float(by[(tid, a, s)]["pass"]) for a, s in arm_seeds]
            out[tid] = sum(vals) / len(vals)
        return out

    d69_rate = task_rate([("d69", 0), ("d69", 1)])
    tr20_s1_rate = task_rate([("tr20", 1)])
    tr20_pool = task_rate([("tr20", 0), ("tr20", 1)])
    scale_rate = task_rate([("scale10", 0), ("scale10", 1)])

    def paired(a, b, label):
        diffs = [b[t] - a[t] for t in task_ids]
        delta = sum(diffs) / len(diffs)
        ci = boot_ci(diffs)
        print(f"  {label}: delta={delta*100:+.1f} pp  95% CI [{ci[0]*100:.1f}, {ci[1]*100:.1f}]")
        assert ci[0] <= 0 <= ci[1] or abs(delta) < 0.02  # paper: all include 0 for main pairs
        return delta, ci

    print("Section 4 — paired bootstrap (10k draws)")
    paired(d69_rate, tr20_s1_rate, "tr20_s1 − d69")
    paired(d69_rate, tr20_pool, "tr20_pooled − d69")
    paired(d69_rate, scale_rate, "scale10 − d69")

    # Oracle pass@6: any of 6 rollouts (3 arms × 2 seeds) passes
    oracle = 0
    for tid in task_ids:
        if any(by[(tid, a, s)]["pass"] for a in ("d69", "tr20", "scale10") for s in (0, 1)):
            oracle += 1
    oracle_rate = oracle / len(task_ids)
    print(f"Section 4 — oracle pass@6: {oracle}/{len(task_ids)} = {oracle_rate:.1%}")
    assert abs(oracle_rate - EXPECTED["oracle_pass_at_6_rate"]) <= 0.02

    print("Section 5/6 — timeout forensics on tr20 seed 1")
    timeouts = [r for r in tr20_s1 if failure_bucket(r) in ("timeout_empty_diff", "timeout_unsubmitted_with_diff") and not r["pass"]]
    empty = [r for r in timeouts if failure_bucket(r) == "timeout_empty_diff"]
    with_diff = [r for r in timeouts if failure_bucket(r) == "timeout_unsubmitted_with_diff"]
    print(f"  failing clock-timeouts: {len(timeouts)} (empty_diff={len(empty)}, with_diff={len(with_diff)})")
    assert len(empty) == 52 and len(with_diff) == 22, (len(empty), len(with_diff))
    opened = sum(1 for r in empty if r["opened_gold_file_read"] or r["opened_gold_file_shell"])
    print(f"  empty_diff opened a gold file (read|shell): {opened}/{len(empty)}")
    med_left = sorted(r["fatal_turn_remaining_sec"] for r in empty if r["fatal_turn_remaining_sec"] is not None)
    if med_left:
        mid = med_left[len(med_left) // 2]
        print(f"  median fatal_turn_remaining_sec (empty): {mid}")

    print("Section 7 — Phase 2 guards")
    check_block("P2_A", p2a, EXPECTED["phase2"]["P2_A"])
    check_block("P2_B", p2b, EXPECTED["phase2"]["P2_B"])

    print("Section 8 — Phase 3 thinking cap")
    check_block("think1024", p3, EXPECTED["phase3"]["a1"])
    p3_by = {r["task_id"]: r for r in p3}
    base_by = {r["task_id"]: r for r in tr20_s1}
    ups = downs = 0
    diffs = []
    for tid in task_ids:
        a = float(p3_by[tid]["pass"])
        b = float(base_by[tid]["pass"])
        diffs.append(a - b)
        ups += a > b
        downs += a < b
    delta = sum(diffs) / len(diffs)
    ci = boot_ci(diffs)
    print(f"  paired WT delta={delta*100:+.1f} pp  CI [{ci[0]*100:.1f}, {ci[1]*100:.1f}]  flips +{ups}/-{downs}")
    assert ups == EXPECTED["phase3"]["flips_up"] and downs == EXPECTED["phase3"]["flips_down"]
    assert abs(delta - EXPECTED["phase3"]["delta_vs_tr20_s1"]) < 1e-9
    assert ci[0] <= 0 <= ci[1]

    th_a1 = sum(1 for r in p3 if thoughts_over(r, 1024))
    th_base = sum(1 for r in tr20_s1 if thoughts_over(r, 1024))
    print(f"  thoughts>1024: a1={th_a1} base={th_base}")
    assert th_a1 == EXPECTED["phase3"]["thoughts_gt_1024_a1"]
    assert th_base == EXPECTED["phase3"]["thoughts_gt_1024_base"]

    tb_a1 = sum(1 for r in p3 if r["end_reason"] == "time_budget")
    tb_base = sum(1 for r in tr20_s1 if r["end_reason"] == "time_budget")
    sub_a1 = sum(1 for r in p3 if r["end_reason"] == "submitted" or (r.get("patch_submitted") and r["end_reason"] != "time_budget"))
    # Prefer end_reason counts as in FINAL
    end_a1 = Counter(r["end_reason"] for r in p3)
    end_base = Counter(r["end_reason"] for r in tr20_s1)
    print(f"  end_reason a1={dict(end_a1)} base={dict(end_base)}")
    assert end_a1.get("time_budget", 0) == EXPECTED["phase3"]["time_budget_a1"]
    assert end_base.get("time_budget", 0) == EXPECTED["phase3"]["time_budget_base"]
    assert end_a1.get("submitted", 0) == EXPECTED["phase3"]["submitted_a1"]
    assert end_base.get("submitted", 0) == EXPECTED["phase3"]["submitted_base"]

    # Stratum table phase3
    print("  by stratum (WT passes):")
    for stratum in ("competition_new", "competition_public", "other"):
        ts = [t for t in task_ids if p3_by[t]["stratum"] == stratum]
        a1 = sum(1 for t in ts if p3_by[t]["pass"])
        b = sum(1 for t in ts if base_by[t]["pass"])
        print(f"    {stratum}: think1024={a1}/{len(ts)}  tr20_s1={b}/{len(ts)}")

    elapsed = time.perf_counter() - t0
    print(f"\nALL_PAPER_TABLES_REPRODUCED = True  ({elapsed:.2f}s)")
    if elapsed > 5.0:
        print(f"WARNING: reproduction took {elapsed:.2f}s (>5s target)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as e:
        print(f"REPRO_FAIL: {e}", file=sys.stderr)
        raise SystemExit(1)
