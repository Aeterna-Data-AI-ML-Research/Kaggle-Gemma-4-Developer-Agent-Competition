# P6.87 Overnight Breakthrough Report

**Written:** 2026-10-31T12:00:00Z  
**Guards:** Operator `CLOUD_APPROVAL=YES` ≤$0.80 → spent ≈$0.109 → reset **NO** · G4 · paper frozen P6.75 · D36 `57810851` PENDING · `live_pods: []`

## Phase 1 — Local CPU ($0.00)
- Staged `p687_gpu_payload/`: panel10, D43 + E4B-D1 extracts, `mssft_43.jsonl`, `budget_watchdog.py`, train scripts.
- Final-14 `docs_src` strip+ddmin: **partial** (6 pmin diffs; `fastapi_14609` in progress) → funnel stays **71/85**.

## Phase 2 — Live GPU Sprint
- **Pod:** `eixsgp9u0srmwo` Secure A40 $0.59/hr CA-MTL-1; watchdog cap $0.75.
- **Spend:** ≈**$0.109** (elapsed ≈0.185 h); terminated; API `live_pods: []`.
- **Exp A — E4B live generate (proxy):** model `google/gemma-4-E4B-it` (public; competition QAT not on volume).
  - Panel10: `sed_n_compliance=1.0`, mean_gen_s=2.579, tok/s≈17.7, **$W_{\mathrm{edit1}}$ proxy=5.054s**.
  - Note: not full ADK/two-sided pytest; D43 31B not loaded under cap.
- **Exp B — MS-SFT LoRA:** adapter saved (`e4b_lora_adapter`, r=16, 12 steps, 13.13s train after ClippableLinear unwrap). D1 vs D2 smoke → **D2 not superior** → **not vaulted**. Keep **E4B-D1**.

## Decisions
- Champions: **D43** + **E4B-D1** unchanged.
- `CLOUD_APPROVAL=NO`.
- Next: finish final-14 ddmin (funnel 71+/85); await D36 LB.

## Artifacts
- `gemma4-agent/results/p618_clean_frontier/p687_live_gpu_verification.json`
- `gemma4-agent/results/p618_clean_frontier/p687_gpu_out/` (gpu_results, lora_meta, d1_vs_d2_smoke, adapter)
- `gemma4-agent/results/p618_clean_frontier/p687_gpu_payload/`
