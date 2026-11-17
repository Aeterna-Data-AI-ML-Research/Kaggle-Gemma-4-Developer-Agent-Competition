# OVERNIGHT P7.25 GPU REPORT

- written_utc: `2026-11-10T23:20:00Z` (approx)
- ticket: `P7.25-GM-DS-Hardened`
- CLOUD_APPROVAL: `YES`
- NO_SUBMIT / NO_SOUPS / G4: `1` / `1` / `0`
- SKU: `1x NVIDIA A40 48GB` @ `$0.59/hr` (≤ `$0.65/hr`)
- pod_id: `ngxjy99aeyq531` · host `63.141.33.115:22053`
- terminate_policy: **SUCCESS-only** (errors kept warm + resume)
- local SSD backup: `~/p725_overnight_backup/`
- S3: `s3://gemma4-dev-agent-data-650825122703/results/p725_overnight_gpu/`

## Outcome

| Stage | Status | Notes |
|------|--------|-------|
| 1 Bootstrap + compact | **DONE** | 129 snaps staged; `sft_p725_master_compacted.jsonl` 61 rows; max_tokens **8162 ≤ 8192**; G4=0 / 7036B |
| 2 31B SurgicalTune mlp3 | **DONE** | `d90` steps 2–12; OOM@8192 fixed via resume@4864; tensor surgery → `d91` **240 keys**, `d92` **180 keys** |
| 3 31B multi-LoRA tournament | **PARTIAL** | vLLM multi-LoRA healthy (base+d90+d91+d92); speed probes OK; full 13-task harness **not available on lean pod payload** — zip packaged + host-wiring **PASS** |
| 4 E4B EdgeDistill d32 | **DONE** | HF `google/gemma-4-E4B-it` (QAT absent on S3); MLP-only **252 keys / 0 attn**; train to step_12; E4B vLLM ~**21.6 tok/s** probe; zip host-wiring **PASS** |
| 5 Sync + terminate | **DONE on SUCCESS** | Local SSD + vault + S3 synced; pod terminated |

## Proprietary IP pillars exercised

1. **ForgeGym** — snapshot staging / on-policy recovery path (builder blocked initially by missing `tasks.jsonl`; compacted master still produced)
2. **DAgger-Recover** — compacted master merge + warm-harvest hook (harvest script absent → empty harvest)
3. **SurgicalTune** — attention-frozen MLP LoRA (`gate/up/down` only) on 31B + E4B; zero-train subspace surgery d91/d92
4. **DiffGuard / EdgeDistill** — host-wired packages; E4B distilled from compacted 31B-era master

## Artifacts (verified)

| Artifact | Verify | Path |
|----------|--------|------|
| 31B Main Track zip | `ADAPTER_HOST_WIRING_PASS=True` | `gemma4-agent/proprietary_vault/zips/p725_31b_d90_dagger_mlp_a8_think4096_out6144_6tools.zip` (+ `~/p725_overnight_backup/zips/`) |
| E4B Small Track zip | `ADAPTER_HOST_WIRING_PASS=True` | `gemma4-agent/proprietary_vault/zips/p725_e4b_d32_dagger_mlp_v2_a8_think4096_6tools.zip` |
| 31B ckpts | local SSD | `~/p725_overnight_backup/ckpts/d90_31b_mlp3*` / `d91*` / `d92*` |
| E4B ckpts | local SSD | `~/p725_overnight_backup/ckpts/d32_e4b_dagger_mlp_v2*` |
| Compacted SFT | local SSD | `~/p725_overnight_backup/data_train/sft_p725_master_compacted.jsonl` |

## Kaggle `58210261`

```
58210261  submission.zip  2026-11-10 17:59:10  P7.23_E4B_D29_dagger_mlp_step8…  SubmissionStatus.PENDING
```

**UPDATE:** status flipped to **COMPLETE** · publicScore **`0.06`** (see `docs/OVERNIGHT_P723_KAGGLE_58210261_RESULT.md`).

## Spend / ops notes

- A40 Secure `$0.59/hr`; hard cap `$3.20` / 280 min.
- 31B train OOM at `max_seq=8192` → resumed at `4864`.
- E4B train OOM at `8192` → resumed at `4096` from `checkpoint-4`.
- vLLM 0.33 required clean GPU + `setsid` launcher; multi-`--lora-modules` duplicate-key pitfall fixed by single flag with multiple `name=path` pairs.
- Lean SSD stage payload used because `gemma4-agent` lives on slow ExFAT `<REPO_ROOT>`.

## Honest gaps / next wake-up actions

1. Re-run **13-task Gate1+remain8** with full eval harness (`rejection_sample` / panel runner) against packaged adapters (harness was not in lean payload).
2. Unlock true **42/42** on-policy recoveries (push `data/tasks.jsonl` + `forgeswe/dagger_recover.py` full loop) and rebuild compacted master if needed.
3. Real in-VRAM Tier-1 (current stage2 used proxy scores when `p725_tier1_in_vram.py` missing).
4. Upload E4B QAT to S3 when available (tonight used HF IT weights).

*NO_SUBMIT=1 throughout — no Kaggle upload from this run.*
