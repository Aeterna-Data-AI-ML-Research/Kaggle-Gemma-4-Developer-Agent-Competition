# P7.30 Stage2-GM — Pure ForgeSWE v3 Joint Train + 9-Task Tournament

**UTC closeout:** 2026-11-12 · **Locks at train time:** `CLOUD_APPROVAL=YES` (A40 ≤$0.65/hr, hard ≤$1.65) · `G4=0` · `G19=PASS` · `7036B` · Stage2 orch `NO_SUBMIT=1` until operator override.

## MEASURED results

### Phase1 (in-VRAM 31B, PyTorch)
- Mount `d98_v2_forgeswe_smooth_midband_true_scale_a16` (`r=8`, `α=16`, attn-lock → `Δq=Δo=0`).
- Joint 6-step GapDPO-AnchorCached + DAgger-SFT; grad spikes skipped/resampled when `grad_norm≥5`.
- Spectral synth `d100_s{3,6}` vs `W_anchor=d98_v2` (`η_in=0.05`, `η_ortho=0.45`).
- Contrastive gate (22 pairs): all arms **win%=63.636**; `d100_s6` slightly better `tier2_6_margin` (−0.160 vs −0.190); `MAD_vs_d98≈6e-4`.
- Winner: **`d100_best_forgeswe_v3_spectral_a16`** ← `d100_s6`.

### Phase2 (vLLM multi-LoRA, concurrency=1, ≥21 tok/s)
| arm | 9-task |
| --- | ---: |
| tr20 proxy | 5/9 (0.17 LB) |
| M1_d98_buggy | 4/9 |
| **V1** `d98_v2_true_scale` | **3/9** |
| **V2** `d100_best` | **4/9** |

V2 flips vs V1: **`requests_6644`**. Shared: `fastapi_14301`, `rich_2725`, `rich_2943`. Still miss: `rich_3676`, `fastapi_14873`, `rich_3052`, `rich_4077`, `rich_3521`.

**Verdict:** best **4/9** → `hold_<=0.18`; `unlock_NO_SUBMIT_0=false` (need ≥6/9).

### Phase3
- Pods terminated (`live_pods=[]`, ~$0.00/hr).
- Local 5-gate on packaged zips: G1/G3/G4 PASS; G2 FAIL (spectral blend threshold); G5 FAIL under forced `NO_SUBMIT` during orch.
- Artifacts: `gemma4-agent/results/p730_stage2_gm/`, vault zips `p730_31b_d{98_v2,100_best}_*_6tools.zip`.

## Main-track submit (operator override 2026-11-12T20:50Z)

| field | value |
| --- | --- |
| ref | **`58284674`** |
| status | PENDING (at submit) |
| sha12 | `bd7d01af700e` |
| arm | V2 `d100_best_forgeswe_v3_spectral_a16` |
| G19 | PASS |
| message | `P7.30_ForgeSWE_v3_31B_d100_best_spectral_a16_think4096_out6144_6tools_V2_4of9_bd7d01af700e` |

Record: `gemma4-agent/results/p730_stage2_gm/main_track_submit.json`.

## Dead ends (do not re-burn)

1. **vLLM install without `--ignore-installed`** fails on Debian PyJWT (no RECORD) → empty module; always mirror p729 install flags.
2. **Missing `litellm` + `wheels_harness/*.whl`** → panels exit instantly (`ModuleNotFoundError`); ensure eval deps even when vLLM already present.
3. **Snapshot sync of dirs ≠ `{tid}.tgz`** → all tasks `Snapshot file not found`; pull from `s3://…/competition/full/snapshots/{tid}.tgz`.
4. **Agent `model:` = filesystem path** → `Model alias … not found in registry`; use short `gemma-4-31b-it-qat-w4a16-ct` + `WARM_SERVED_MODEL=<lora_name>` (p729 parity).
5. **`P726_DIFFGUARD_ONESHOT=1`** with tools.py lacking `install_into_swegemma` → abort before meta; set `=0` (p729).
6. **Joint batch OOM / grad_norm spikes ≥5** on A40 — use microbatch-1, shorter seq, spike skip/retry; do not raise LR blindly.
7. **In-VRAM win% flat at 63.6%** after 6 MLP steps — spectral gate alone did not unlock ≥6/9; do not expect contrastive MAD≪1 to imply live Tier-2 flips.
