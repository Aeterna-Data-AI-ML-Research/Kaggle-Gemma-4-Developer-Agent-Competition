# P6.84 Overnight Breakthrough Report

**Written:** 2026-10-31T09:52:38Z  
**Guards:** CLOUD_APPROVAL=NO · G4 · paper frozen · poller 89384 undisturbed

## Stage 1 — rich_3486 autopsy + final 17 inventory
- **Why P6.83 missed:** `find_candidate_patches` returned empty; helper subsets 1–3/4 fail; full $P_{\min}^*$ was `pmin_pass=true` but not recorded as a flip.
- **Agent conflict:** cached rollout patches `Frame.colno/end_colno` (wrong) instead of `last_instruction`.
- **Condition for TRUE_SOUND_PASS:** revert agent edit; apply **all 4** $P_{\min}^*$ hunks on `rich/traceback.py`.
- Final 17 inventory in artifact (`|F|`, `|H|`, change-lines, `|U|`, compression ratio).

## Stage 2 — Unique Hunk Template compression + live grafts
- **U≤3 among final 17:** **0** tasks.
- **Best compression:** `fastapi_14605` H=16 U=5 primary×11 — `allow_multiple` can apply the repeated deprecation-warning rename; top-3 templates (14/16) still fail without support hunks.
- **Template-only probe flips:** **0** (besides rich_3486 full-pmin autopsy).
- **Gold-$P_{\min}^*$ reachable:** **14/17**; pmin-fail: `fastapi_14953, rich_3052, rich_3675`.
- **New overnight flip:** `rich_3486` only.

## Stage 3 — D44 vs D43
- Decision: **certify_D43** · sha12 **54144a1791bf** · Δ **326** ≤335
- D44 twin-sites micro would be Δ328 — deferred (no measured splice/policy edge).
- Splice **0.9608** · policy **0.9924** · gates 8/8
- Funnel **69/85** · pytest cum ≥**10371**

## Artifacts
- `gemma4-agent/results/p618_clean_frontier/p684_final_17_template_compression_and_flips.json`
- vault champion remains `d43_compressed_helper_bridge_champion.zip`
