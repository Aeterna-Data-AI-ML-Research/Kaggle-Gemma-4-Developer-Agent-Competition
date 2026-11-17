# P6.77 Overnight Breakthrough Report

**Written:** 2026-10-30T23:58:29Z  
**Guards:** CLOUD_APPROVAL=NO · G4 holdout sealed · paper/`swe-horizon-bench` frozen at P6.75 · poller 89384 undisturbed  
**D36 live:** `57810851,submission.zip,2026-10-30 16:11:48.877000,P6.68_D36_hong024_8m_8192_240s_think2048_calls40_allow_mult_inline_repro,SubmissionStatus.PENDING,,`

## Executive summary

Overnight local CPU compute (pics volume worktrees; Data disk ~7 Gi free) ran three deep stages:

1. **Live pytest repair** on the **41 unsolved** usable non-holdout tasks (snapshot unpack + `/tmp/p657_py312_venv` → pics venv).
2. **Full deconstruction** of **56** vaulted competitor notebooks.
3. **85-task compound horizon-read** simulation (1-call multi-window `sed`/`run_command` vs 150-line `read_file`).

Staged proprietary **D38** `None` (`d38_horizon_compound_champion.zip`) on D37 base — **7/7** gates, **not submitted**.

## Stage 1 — Minimal-sufficient gold subsets (live pytest)

| Metric | Value |
| --- | ---: |
| Tasks completed (checkpointed) | 41 |
| Any MS-subset pass | **37** |
| MS-subset ≤2 hunks | **19** |
| Export-bridge flips | 0 |
| Sibling-bridge flips | 0 |

MS≤2 IDs: `fastapi_11355, fastapi_13920, fastapi_14246, fastapi_14266, fastapi_14479, fastapi_14487, fastapi_14492, fastapi_15661, fastapi_15763, rich_3105, rich_3180, rich_3468, rich_3480, rich_3521, rich_3535, rich_3934, rich_3938, rich_3944, rich_4076`

**Implication:** Unsolved ≠ “needs full 8–15 hunk gold”. Where MS≤2 holds, prompts should push **companion-hunk completion** after first verify fail (encoded in D38 §3c).

## Stage 2 — Competitor notebook forensics

- Notebooks deconstructed: **56**
- Architectural families: `{"igor_budget_lineage": 9, "lora_finetune_notebook": 19, "other_or_analysis": 12, "idris_018_lineage": 4, "hong_024_lineage": 10, "autonomous_swe_prompt": 2}`
- Callbacks seen: `{}`
- Notebooks with `tools.py`-style mutations: **3**

**Host rule (decision):** Custom notebook `tools.py` (raised `max_lines`, `git add -N`, auto-pytest in `submit_patch`, `count_tool_call=False`) is treated as **non-portable** unless the live host is proven to import submission-local tools. Keep LB candidates **prompt/YAML-only** (D36→D38).

Novel candidates: [{"path": "gemma4-agent/external_notebooks/radar_20261030/navyaminocha_gemma4-pipeline/gemma4-pipeline.ipynb", "family": "lora_finetune_notebook", "mods": [{"kind": "submit_patch_git_add_N"}]}, {"path": "gemma4-agent/external_notebooks/radar_20261030/leoprovorov_gemma-4-the-complete-guide-expanded-full/gemma-4-the-complete-guide-expanded-full.ipynb", "family": "idris_018_lineage", "mods": [{"kind": "submit_patch_git_add_N"}]}, {"path": "gemma4-agent/results/p614_public_kernels/robina_loop/gemma-4-loop-breaker-adk-agent.ipynb", "family": "autonomous_swe_prompt", "mods": [{"kind": "submit_patch_git_add_N"}]}]

## Stage 3 — Compound 1-call horizon read

Caps: `read_file` **150 lines/file/call**; `run_command` output **~5000 chars** across multi-file windows.

| Stratum | n | mean B1 cover | mean compound cover | mean calls saved |
| --- | ---: | ---: | ---: | ---: |
| all | 85 | 0.3161 | 0.7254 | 0.9529 |
| S1 deep | 0 | 0.0 | 0.0 | 0.0 |
| S2 | 18 | 0.3515 | 0.7622 | 1.5 |
| S3 | 28 | 0.1479 | 0.3606 | 1.9286 |

## D38 specification

- Base: `None` (D37 export/branch retained)
- Added clause (NoneB): compound multi-window read + MS-subset retry
- Knobs unchanged: timeout 240 / think 2048 / calls 40 / 8m / 8192 / temp 0.2 / 9 tools
- SHA256: `6be60c40ecc08ce1845926e3226338168539dd0b3d607992f6dc3e50615edd31`
- Gates: **7/7** · check_pass=None
- **Submit:** NO (await D36 `57810851` terminal)

## Decision matrix once D36 scores

| D36 public score | Action |
| --- | --- |
| ≥ 0.24 | HOLD finals floor; keep D33/D36; evaluate D38 offline only |
| 0.18 ≤ score < 0.24 | Consider **D38** vs **D37** as next G3 single-axis submit (operator pick) |
| < 0.18 or ERROR | Poller autosubmits **D33** exact hong; then queue D38 offline validation |

## Artifacts & resume

- Checkpoints: `<REPO_ROOT>/kaggle/p677_overnight/checkpoints/` (`stage{1,2,3}_progress.jsonl`)
- Ledgers: `p677_stage1_…json`, `p677_stage2_…json`, `p677_stage3_…json` under `results/p618_clean_frontier/`
- Re-run any stage safely — completed task/notebook IDs are skipped.

## Resources

```json
{
  "utc": "2026-10-30T23:58:29Z",
  "tag": "report",
  "rss_mb": 26.8,
  "pics_free_gi": 1471.3,
  "data_free_gi": 80.45,
  "tmp_free_gi": 80.45
}
```
