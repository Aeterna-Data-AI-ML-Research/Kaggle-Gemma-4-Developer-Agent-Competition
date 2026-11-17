#!/usr/bin/env python3
"""Build turn-level compact evidence + benchmark manifest from private monorepo results.

Run from the private competition monorepo (or pass --monorepo). Writes into the OSS
export tree. Researchers do not need this to reproduce PAPER.md tables — use
reproduce_all_tables.py on the shipped evidence/*.jsonl instead.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

EDIT_TOOLS = ("edit_file", "write_file")
CUTOFF_S = 420.0
CPT = 4.197  # chars per completion token (measured)


def patch_files(patch: str) -> list[str]:
    out: list[str] = []
    for line in (patch or "").splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                b = parts[3]
                if b.startswith("b/"):
                    b = b[2:]
                out.append(b)
    return out


def norm(path: str) -> str:
    p = str(path or "")
    if p.startswith("/workspace/"):
        p = p[len("/workspace/") :]
    return p.lstrip("./")


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, separators=(",", ":"), ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pr_number(task_id: str) -> int | None:
    m = re.search(r"_(\d+)$", task_id or "")
    return int(m.group(1)) if m else None


def thinking_budget(row: dict) -> int | None:
    th = row.get("thinking") or {}
    if isinstance(th, dict):
        for k in ("thinking_token_budget", "thinking_budget"):
            if th.get(k) is not None:
                return int(th[k])
    if row.get("thinking_budget") is not None:
        return int(row["thinking_budget"])
    return None


def compact_episode(row: dict, *, phase: str, harness_arm: str | None = None) -> dict:
    gold = [norm(g) for g in (row.get("gold_files") or [])]
    gold_py = [g for g in gold if g.endswith(".py")]
    gold_use = gold_py or gold
    gold_set = set(gold_use)

    turns = row.get("turns") or []
    trace = row.get("tool_trace") or []
    by_turn: dict[int, list[dict]] = {}
    for t in trace:
        by_turn.setdefault(int(t.get("turn", -1)), []).append(t)

    turn_summary = []
    for t in turns:
        idx = int(t.get("i", len(turn_summary)))
        tools = by_turn.get(idx, [])
        tool_name = tools[0]["name"] if tools else None
        exit_code = None
        target_is_gold = False
        if tools:
            ok = tools[0].get("ok")
            exit_code = 0 if ok else (1 if ok is False else None)
            for tool in tools:
                args = tool.get("args") or {}
                blob = json.dumps(args, ensure_ascii=False)
                fp = norm(str(args.get("filepath") or args.get("path") or ""))
                if fp and fp in gold_set:
                    target_is_gold = True
                elif any(g in blob for g in gold_set):
                    target_is_gold = True
        ct = float(t.get("completion_tokens") or 0)
        rc = float(t.get("reasoning_chars") or 0)
        reasoning_tokens = min(ct, rc / CPT) if ct else 0.0
        content_tokens = max(0.0, ct - reasoning_tokens)
        t_end = float(t.get("t_virtual") or 0.0)
        r_gen = float(row.get("r_gen") or 14.0) or 14.0
        t_start = t_end - (ct / r_gen if r_gen else 0.0)
        # Dense tuple (see evidence/SCHEMA.md):
        # [turn_idx, v_start, v_end, reasoning_tok, content_tok, tool_name, gold_target, exit_code]
        turn_summary.append(
            [
                idx,
                round(t_start, 2),
                round(t_end, 2),
                int(round(reasoning_tokens)),
                int(round(content_tokens)),
                tool_name,
                1 if target_is_gold else 0,
                exit_code,
            ]
        )

    first_edit_turn = None
    first_edit_virtual_sec = None
    for t in trace:
        if t.get("name") in EDIT_TOOLS and t.get("ok"):
            first_edit_turn = int(t["turn"])
            first_edit_virtual_sec = float(t.get("t_virtual") or 0.0)
            break

    read_gold, shell_gold, opened = set(), set(), set()
    for t in trace:
        args = t.get("args") or {}
        name = t.get("name")
        blob = json.dumps(args, ensure_ascii=False)
        for g in gold_use:
            if name == "read_file" and t.get("ok") and norm(str(args.get("filepath") or "")) == g:
                read_gold.add(g)
                opened.add(g)
            if name in ("read_file", "run_command") and g in blob:
                if name == "run_command":
                    shell_gold.add(g)
                opened.add(g)

    fatal_remaining = None
    fatal_reasoning = None
    if turns and row.get("end_reason") == "time_budget":
        last = turns[-1]
        ct = float(last.get("completion_tokens") or 0)
        r_gen = float(row.get("r_gen") or 14.0) or 14.0
        start = float(last.get("t_virtual") or 0.0) - ct / r_gen
        fatal_remaining = round(CUTOFF_S - start, 3)
        rc = float(last.get("reasoning_chars") or 0)
        fatal_reasoning = round(min(ct, rc / CPT) if ct else 0.0, 2)

    # Exact forensic predicate used in P753 FINAL (float, not rounded ints).
    thoughts_gt_1024 = any(
        min(float(t.get("completion_tokens") or 0), float(t.get("reasoning_chars") or 0) / CPT) > 1024
        for t in turns
    )

    patch = row.get("final_patch") or row.get("patch_at_submit") or ""
    patch_sha12 = hashlib.sha256(patch.encode()).hexdigest()[:12] if patch else None

    out = {
        "phase": phase,
        "task_id": row["task_id"],
        "arm": row.get("arm"),
        "harness_arm": harness_arm or row.get("harness_arm"),
        "seed": int(row.get("seed") or 0),
        "stratum": row.get("stratum"),
        "pass": bool(row.get("pass")),
        "strict_pass": bool(row.get("pass") and row.get("patch_submitted")),
        "end_reason": row.get("end_reason"),
        "failure_mode": row.get("failure_mode"),
        "virtual_seconds": round(float(row.get("virtual_seconds") or 0.0), 2),
        "tool_s": round(float(row.get("tool_s") or 0.0), 3),
        "gen_tokens": int(row.get("gen_tokens") or 0),
        "tool_calls": int(row.get("tool_calls") or 0),
        "thinking_budget": thinking_budget(row),
        "temperature": row.get("temperature"),
        "r_gen": row.get("r_gen"),
        "patch_chars": int(row.get("patch_chars") or len(patch)),
        "patch_sha12": patch_sha12,
        "patch_submitted": bool(row.get("patch_submitted")),
        "n_gold_files": len(gold_use),
        "turn_summary": turn_summary,
        "first_edit_turn": first_edit_turn,
        "first_edit_virtual_sec": None if first_edit_virtual_sec is None else round(first_edit_virtual_sec, 2),
        "opened_gold_file_read": bool(read_gold),
        "opened_gold_file_shell": bool(shell_gold),
        "opened_all_gold_files": bool(gold_use) and len(opened) == len(gold_use),
        "fatal_turn_remaining_sec": fatal_remaining,
        "fatal_turn_reasoning_tokens": fatal_reasoning,
        "thoughts_gt_1024": bool(thoughts_gt_1024),
    }
    return out


def build_manifest(monorepo: Path) -> list[dict]:
    splits = json.loads((monorepo / "gemma4-agent/configs/p750_pool_splits.json").read_text())
    stratum_map = splits.get("stratum") or {}
    meta: dict[str, dict] = {}
    pool = monorepo / "gemma4-agent/data/p750_pool"
    for path in list(pool.glob("candidates_*.jsonl")) + [pool / "public_tasks.jsonl", pool / "calib_150_tasks.jsonl"]:
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            tid = r.get("instance_id") or r.get("task_id")
            if tid:
                meta[tid] = r

    rows = []
    for split_name in ("calib", "test", "train", "reserve_eval"):
        for tid in splits[split_name]:
            r = meta.get(tid) or {}
            gold = patch_files(r.get("patch") or "")
            test_files = patch_files(r.get("test_patch") or "")
            test_cmd = None
            if test_files:
                test_cmd = "python -m pytest " + " ".join(test_files) + " -q"
            rows.append(
                {
                    "task_id": tid,
                    "repo": r.get("repo"),
                    "repo_short": r.get("repo_short") or (tid.split("_")[0] if "_" in tid else None),
                    "base_commit": r.get("base_commit"),
                    "pr_number": pr_number(tid),
                    "stratum": stratum_map.get(tid) or r.get("stratum") or "unknown",
                    "split": "holdout" if split_name == "reserve_eval" else split_name,
                    "gold_files": gold,
                    "test_files": test_files,
                    "test_cmd": test_cmd,
                    "license": r.get("license"),
                }
            )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--monorepo",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "Kaggle-Gemma-4-Developer-Agent-Competition",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = ap.parse_args()
    mono = args.monorepo.resolve()
    out = args.out.resolve()
    if not (mono / "gemma4-agent").is_dir():
        # try sibling layout: this file lives inside export, monorepo is sibling
        alt = Path(__file__).resolve().parents[2] / "Kaggle-Gemma-4-Developer-Agent-Competition"
        if (alt / "gemma4-agent").is_dir():
            mono = alt
        else:
            print(f"monorepo not found: {mono}", file=sys.stderr)
            return 2

    ckpt = mono / "gemma4-agent/results/p751_phase1/checkpoints"
    p1, p2 = [], []
    for i in range(5):
        p1 += load_jsonl(ckpt / f"pod{i}/results/pod{i}_episodes.jsonl")
        p2 += load_jsonl(ckpt / f"pod{i}/results/p752_phase2/pod{i}_p2_episodes.jsonl")
    p1 = [r for r in p1 if r.get("verdict_valid") is True]
    p2 = [r for r in p2 if r.get("verdict_valid") is True]
    assert len(p1) == 900 and len(p2) == 300, (len(p1), len(p2))

    p3 = []
    for i in range(5):
        matches = list((mono / f"gemma4-agent/results/p753_thinkcap/checkpoints/pod{i}").rglob("*a1_think1024*episodes.jsonl"))
        assert matches, f"missing p753 episodes for pod{i}"
        p3 += load_jsonl(matches[0])
    assert len(p3) == 150, len(p3)

    phase1 = [compact_episode(r, phase="phase1") for r in p1]
    phase2 = [compact_episode(r, phase="phase2", harness_arm=r.get("harness_arm")) for r in p2]
    phase3 = [compact_episode(r, phase="phase3") for r in p3]
    # phase3 thinking budget was the experiment variable
    for r in phase3:
        if r["thinking_budget"] is None:
            r["thinking_budget"] = 1024

    ev = out / "evidence"
    write_jsonl(ev / "phase1_calibration_900.jsonl", phase1)
    write_jsonl(ev / "phase2_guards_300.jsonl", phase2)
    write_jsonl(ev / "phase3_thinkcap_150.jsonl", phase3)

    manifest = build_manifest(mono)
    write_jsonl(out / "benchmark/tasks_manifest.jsonl", manifest)

    lines = []
    for rel in (
        "evidence/phase1_calibration_900.jsonl",
        "evidence/phase2_guards_300.jsonl",
        "evidence/phase3_thinkcap_150.jsonl",
        "benchmark/tasks_manifest.jsonl",
    ):
        p = out / rel
        digest = sha256_file(p)
        lines.append(f"{digest}  {rel}")
        print(f"{rel}: rows={sum(1 for _ in p.open())} bytes={p.stat().st_size} sha256={digest[:12]}")
    (ev / "manifest.sha256").write_text("\n".join(lines) + "\n")
    total = sum((out / r.split()[-1]).stat().st_size for r in lines)
    print(f"evidence+manifest bytes={total} (<3MB target for evidence only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
