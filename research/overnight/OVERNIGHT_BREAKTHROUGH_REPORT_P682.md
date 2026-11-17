# P6.82 Overnight Breakthrough Report

**Written:** 2026-10-31T08:47:56Z  
**Guards:** CLOUD_APPROVAL=NO · G4 · paper frozen · poller 89384 undisturbed

## Stage 1 — 51 splice behavioral attribution
- Causes: `{"B_READ_FULL_FUNCTION_SPAN": 24, "B_REPRO_BEFORE_EDIT": 5, "B_UNATTRIBUTED": 19, "B_NO_PANIC_REVERT": 1, "B_READ_EXISTING_TEST_FIRST": 2}`
- D42 primary cover: **0.5882** (30/51)
- Uncovered: `{"B_READ_EXISTING_TEST_FIRST": 2}`

## Stage 2 — Low `P_min*` + fastapi_14186
- Targets: `fastapi_13920, fastapi_14186, fastapi_14492, fastapi_14986, fastapi_15763, rich_3061, rich_3480, rich_3486, rich_3772, rich_4076`
- Miss reasons: `{"localization_never_touched_pmin_file": 7, "horizon_gt150": 3}`
- New flips: `rich_3772`
- Pytest this stage: **95**

## Stage 3 — Champion
- Decision: **certify_D42** → **D42**
- sha12 **c96559cd93b3** · Δ **341B**
- Funnel: **62/85 (72.9%)**
- Cumulative pytest ≥ **9605**

## Artifacts
- `gemma4-agent/results/p618_clean_frontier/p682_51_splices_and_low_pmin_audit.json`
- `docs/MASTER_REALISTIC_FINDINGS_LEDGER.md`
