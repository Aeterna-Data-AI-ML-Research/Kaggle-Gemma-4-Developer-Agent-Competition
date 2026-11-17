# P6.85 Overnight Breakthrough Report

**Written:** 2026-10-31T10:45:48Z  
**Guards:** CLOUD_APPROVAL=NO · G4 · paper frozen · poller 89384 undisturbed

## Stage 1 — Invariant ddmin repair
- Targets: `fastapi_14953`, `rich_3052`, `rich_3675`
- Harness: tutorial `+def` targets · `filterwarnings=ignore` · `COLUMNS=80`/`NO_COLOR` · rich_3675 tight `-k`
- Result: **16/16** `pmin_pass=True` (repaired idxs/hunks in artifact)

- Extra: gold-as-pmin for `fastapi_14262`, `fastapi_14962`, `fastapi_15030` → **16/16**.

## Stage 2 — Bottlenecks + 1-call batch
- Classifications in artifact
- Batch flips: `['fastapi_13786', 'fastapi_14099', 'fastapi_14306', 'fastapi_14482', 'fastapi_14605', 'fastapi_14609', 'fastapi_14953', 'fastapi_14986', 'fastapi_15800', 'rich_3052', 'rich_3675', 'rich_3930']` · mean calls saved **9.12**
- Pytest this stage: **43**

## Stage 3 — Call-budget sim + D44
- Survival: `{'D33_seq': 0.875, 'D36_seq': 1.0, 'D43_seq': 1.0, 'D44_batch': 1.0}`
- Scores: D43=0.9924 D44=0.9924
- Decision: **retain_D43** · champion **D43** · sha12 **54144a1791bf**
- Funnel remains **69/85** overnight flips; gold-reachable **16/16** final
- Pytest cum ≥**10520**

## Artifacts
- `gemma4-agent/results/p618_clean_frontier/p685_repaired_pmin_and_batch_edit_final16.json`
- repaired pmin: `<REPO_ROOT>/kaggle/p685_research/checkpoints/pmin_repaired/`
