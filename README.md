# gemma4-swe-agent-study

Evidence-first study of a Gemma 4 code-repair agent for the Kaggle Gemma 4
Developer Agent Competition. Aimed at ML / DS researchers who want to extend the
analysis, not at replaying private competition ops.

**License:** Apache-2.0

## Key findings (calib, 150 tasks)

1. Three configs with different Kaggle scores (`d69` 0.18, `tr20` 0.17, `scale10` 0.13)
   were statistically tied offline (WT ≈ 30–32%; paired CIs include 0).
2. Oracle pass@6 ≈ 44% — stochastic headroom without a deployable selector.
3. Most clock-killed empty-diff episodes had already opened a gold file; failures
   were late edits / long reasoning / weak patches, not pure localization.
4. Cutting `thinking_budget` 4096 → 1024 changed behavior (long thoughts nearly
   vanished; more submits) but **not** accuracy (48/150 vs 48/150).

Read the full narrative in [`PAPER.md`](PAPER.md).

## One-command reproduce

```bash
git clone https://github.com/Aeterna-Data-AI-ML-Research/Kaggle-Gemma-4-Developer-Agent-Competition.git
cd gemma4-swe-agent-study
pip install -r requirements.txt
python scripts/reproduce_all_tables.py
python scripts/plot_figures.py   # optional figures → figures/
```

`reproduce_all_tables.py` verifies `evidence/manifest.sha256`, loads 1,350 compact
episodes, runs 10,000-draw paired bootstraps, and checks every pinned table from
PAPER.md Sections 4–8 (≈1–2 s on a laptop CPU).

## Layout

```text
benchmark/     tasks_manifest.jsonl + PROTOCOL.md
evidence/      phase1/2/3 compact JSONL + SCHEMA.md
configs/       stripped D69-shaped declarative baseline (no proprietary prompts)
scripts/       reproduce_all_tables.py, plot_figures.py, build_compact_evidence.py
reports/       appendices + RESEARCH ticket map
PAPER.md       retrospective article
```

## What is included / excluded

| Included | Excluded |
| --- | --- |
| Compact episodes with turn-level summaries | Raw tool args, reasoning text, git diffs |
| 730-task split manifest (calib/test/train/holdout) | Adapter weights / submission zips |
| Virtual-clock protocol | Graded sealed-test trajectories |
| Stripped baseline config shape | Proprietary ops playbooks |

Base model weights and the competition host are **out of band** (see `NOTICE`).

## Kaggle timing

This repository is the public research release for the Aeterna org. Configs are a stripped D69-shaped baseline only (no proprietary prompt grafts).

## Citation

See `CITATION.cff`.
