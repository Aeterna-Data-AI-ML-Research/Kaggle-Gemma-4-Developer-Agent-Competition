# OVERNIGHT BREAKTHROUGH REPORT — P6.90

**UTC:** 2026-10-31T15:22:11Z  
**Cloud:** `CLOUD_APPROVAL=NO` · `live_pods: []` · $0.00 this ticket (forensics on P6.89 $1.43 corpus)  
**D36:** `57810851` PENDING · poller undisturbed · Paper frozen P6.75 · G4 holdout clean

## Verdict
Live 31B multi-turn on custom harness produced **1/33** true-sound passes. Dominant empty-patch modes: explore+timeout (**9**) and failed `edit_file` (**7**). Controlled experiment **confirms H_SED_GAP**: disjoint multi-range `sed -n` output is not a file substring → `old_str` no_match. D45 encodes contiguous-window / no-disjoint-sed-splice rule at Δ**335B** (8/8 gates).

## Stage 1 buckets
- A explore+timeout: 9 — fastapi_13786, fastapi_11355, fastapi_14246, fastapi_14448, rich_4075, fastapi_11194, fastapi_13207, fastapi_14419, fastapi_14482
- B failed edits: 7 — fastapi_13920, fastapi_14266, fastapi_14306, rich_3180, rich_3468, rich_3535, requests_6644
- C context: 1 — rich_3105
- Patched fails: 15 (P_live content not checkpointed; sha12+pytest tails only)

## Stage 2 ADK control
- Wave1: 20 group_A + 11 group_B
- Live pass_rate=0.0323 patch_rate=0.4516
- Selection effect + harness contention/timeout + D43 sed/edit behavior jointly explain drop vs ADK sometimes-solved rates.

## D45
- zip `d45_live31b_forensic_hardened_champion.zip` sha12 **bbd403506c83** Δ=335B gates 8/8

## Artifacts
- `<REPO_ROOT>/Projects/kaggle-google-dev-agent/Kaggle-Gemma-4-Developer-Agent-Competition/gemma4-agent/results/p618_clean_frontier/p690_forensic_autopsy_33_live_31b.json`
- `<REPO_ROOT>/Projects/kaggle-google-dev-agent/Kaggle-Gemma-4-Developer-Agent-Competition/gemma4-agent/results/p689_live_gpu/checkpoints/wave2_d44_clean.jsonl` / cleaned `<REPO_ROOT>/Projects/kaggle-google-dev-agent/Kaggle-Gemma-4-Developer-Agent-Competition/gemma4-agent/results/p689_live_gpu/checkpoints/wave2_d44.jsonl`
