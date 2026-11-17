# P6.86 Overnight Breakthrough Report

**Written:** 2026-10-31T11:14:43Z  
**Guards:** CLOUD_APPROVAL=NO · G4 · paper frozen · poller 89384 undisturbed

## Stage 1 — Reduced $P_{\min}^*$ grafts
- `rich_3675` H=1 · `fastapi_14953` H=3
- Flips: `['rich_3675', 'fastapi_14953']` → funnel **71/85 (83.5%)**
- Miss reasons in artifact

## Stage 2 — 917-trace Find-to-First-Edit
- Files scanned: **917** · trace rows: **834**
- Solved $t_{\mathrm{edit1}}$={'n': 194, 'mean': 9.196, 'median': 9.0} · $W_{\mathrm{edit1}}$={'n': 194, 'mean': 127.781, 'median': 101.332}
- Failed $t_{\mathrm{edit1}}$={'n': 540, 'mean': 14.059, 'median': 11.0} · $W_{\mathrm{edit1}}$={'n': 540, 'mean': 150.519, 'median': 103.127}
- Pass@1 by bucket: `{'2-4': {'n': 116, 'n_resolved': 44, 'pass_at_1': 0.3793}, '5-7': {'n': 145, 'n_resolved': 42, 'pass_at_1': 0.2897}, '8-12': {'n': 176, 'n_resolved': 60, 'pass_at_1': 0.3409}, '>12': {'n': 297, 'n_resolved': 48, 'pass_at_1': 0.1616}, 'missing': {'n': 100, 'n_resolved': 0, 'pass_at_1': 0.0}}`
- D43 config estimate: failed 183s → ~**101.8s**

## Stage 3 — E4B Dual-Track
- **E4B-D1** sha12 **dd8fdae18e5f** · model `gemma-4-e4b-it-qat-w4a16-ct` · gates 8/8 · Δprompt=326B
- MS-SFT jsonl: `43` tasks
- Slot1=31B D43 ladder · Slot2=E4B-D1 · Paper=P6.75 frozen

## Artifacts
- `gemma4-agent/results/p618_clean_frontier/p686_reduced_pmin_latency_and_e4b_track.json`
- `gemma4-agent/results/p618_clean_frontier/p686_e4b_mssft_distillation_43tasks.jsonl`
- vault `e4b_d1_horizon_small_model_champion.zip`
