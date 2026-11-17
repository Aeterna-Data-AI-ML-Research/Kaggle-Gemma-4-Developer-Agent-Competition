# P7.26 Stage0 — Local CPU Audit & Bundle Prep

**Flags:** `CLOUD_APPROVAL=NO` · `live_pods=[]` · `$0.00/hr` · `NO_SUBMIT=1` · `NO_SOUPS=1` · `G4=0`

## Task 1 — Truncation & Loss Audit (P7.25)

### `sft_p725_master_compacted.jsonl` (61 rows) `actual_tokens`

| min | median | p75 | p90 | max |
|----:|-------:|----:|----:|----:|
| 1750 | 4894 | 5781 | 6424 | 8162 |

- **`<=4864` (tail intact during d90 resume):** **29 / 61**
- **`>4864` (tail `edit_file` truncated at Stage2 4864):** **32 / 61**
- `<=6144`: 50 · `>6144`: 11

### `d90_31b_mlp3` loss curve (checkpoint-12)

| step | loss | lr |
|-----:|-----:|---:|
| 1 | 1.7060 | 0 |
| 2 | 1.3674 | 0.0001 |
| 3 | 0.9903 | 9.79746e-05 |
| 4 | 2.0290 | 9.20627e-05 |
| 5 | 1.3690 | 8.2743e-05 |
| 6 | 0.7652 | 7.07708e-05 |
| 7 | 0.5949 | 5.71157e-05 |
| 8 | 0.6046 | 4.28843e-05 |
| 9 | 0.4802 | 2.92292e-05 |
| 10 | 0.6811 | 1.7257e-05 |
| 11 | 0.4538 | 7.93732e-06 |
| 12 | 1.1050 | 2.02535e-06 |

**Verdict:** Partial convergence — clean descent through step 11 (loss **0.454**), then step-12 spike to **1.105**. Combined with **32/61** truncated tails, **`d93_31b_mlp3_tail6144` retrain is warranted**.

### `d32_e4b_dagger_mlp_v2` loss (ref)

| step | loss | lr |
|-----:|-----:|---:|
| 1 | 1.7263 | 0 |
| 2 | 1.5750 | 0.0001 |
| 3 | 0.9215 | 9.79746e-05 |
| 4 | 2.2865 | 9.20627e-05 |
| 5 | 1.8806 | 8.2743e-05 |
| 6 | 2.2122 | 7.07708e-05 |
| 7 | 0.7825 | 5.71157e-05 |
| 8 | 1.2242 | 4.28843e-05 |
| 9 | 0.5821 | 2.92292e-05 |
| 10 | 1.3942 | 1.7257e-05 |
| 11 | 0.4928 | 7.93732e-06 |
| 12 | 0.8492 | 2.02535e-06 |

## Task 2 — 42 On-Policy Recoveries + Tail-Intact Mix + OOM Fix

- On-policy DAgger-Recover: **42/42 OK** (Gate-A 1-turn: 6 · 2-turn: 36)
- `sft_p726_tail_intact_6144.jsonl`: **96 rows**, d29 **51/51**, recoveries **42**, max_tokens **6141**, min_active **98**, recovery_weight **0.25**
- OOM root-cause fix: `install_selective_lm_head_loss` — `lm_head` only on `labels!=-100` (~17.2GB→~0.4GB)

## Task 3 — `d70r_31b_mlp3_a8`

- Source: `d70r_31b_gapdpo_v1_r8_6tools_adapter_wired_champion.zip` (6/13 champ)
- **360 MLP keys · 0 attention keys** · `r=8` · `α=8` · targets `gate/up/down_proj`

## Task 4 — `~/p725_overnight_backup/pod_bundle/`

Self-contained eval+train staging bundle (see `BUNDLE_MANIFEST.json`). Candidates vs Base_31B_D69 (0.18):
1. `d70r_31b_mlp3_a8`
2. `d90_31b_mlp3`
3. `d93_31b_mlp3_tail6144` (PENDING_GPU)
