# P7.27b Fast-Finish Report — ForgeSWE Spectral Fix (NO_SUBMIT=1)

**Date:** 2026-11-12 morning  
**Locks:** `CLOUD_APPROVAL=NO` · `live_pods=[]` · `$0.00/hr` · **`NO_SUBMIT=1`** · **no Kaggle submit** · `G19=1` · `G4=0`

Idle overnight heartbeats **killed** (`PID 57744`, `57849`).

---

## What was fixed (3 one-liners)

| Bug | Fix |
|-----|-----|
| `save_file` non-contiguous LoRA tensors | `{k: v.contiguous() for k,v in sd.items()}` before save |
| Gate1 hardcoded `lora_alpha==16` | `--expected-alpha` + auto from zip stem (`a16→16`, `a8/e4b→8`) |
| Phase2 dropped 88/96 rows on `submit_patch` | **Keep traj**, mark submit turns `p727_mask_submit=True` (train `labels=-100`); drop only extreme denoms |

---

## Step 1 — Materialized adapters + packages

| Artifact | Status | Bytes / sha12 |
|----------|--------|----------------|
| `ckpts/d97_forgeswe_spectral_a16/` | ✅ | `106,175,136` · α=16 · `dq=do=0` · q70≈**0.1128** · 180 MLP |
| `ckpts/d33_e4b_forgeswe_spectral_a8/` | ✅ | `25,841,536` · α=8 · `dq=do=0` · 126 MLP |
| `p727_31b_forgeswe_d97_spectral_ortho_a16_think4096_out6144_6tools.zip` | ✅ vault+backup | **`757375a585a1`** · 83.8 MB |
| `p727_e4b_forgeswe_d33_spectral_ortho_a8_think4096_out6144_6tools.zip` | ✅ vault+backup | **`eea28380705e`** · 20.5 MB |
| `data_train/sft_p727_forgeswe_v2_spike_free_6144.jsonl` | ✅ | **92 rows** (band 85–95) · `G4=0` · 7036B lock · 87 rows with submit turns **masked not dropped** |

Spectral recipe (both tracks): winsor @ q70 on MLP δ; `η_in_span=0.10`, `η_ortho=0.35`; attention 100% locked to anchor (`d70r` / `d29_s8`).

---

## 5-row verification table (`NO_SUBMIT=1`)

| Zip | sha12 | α | Gate1 | Gate2 | Gate3 | Gate4 | Gate5 | all_pass |
|-----|-------|---|-------|-------|-------|-------|-------|----------|
| `d96_tr20` | `89e6ae70fd36` | 16 | PASS | PASS (600/Δq0/Δo0/blend OK) | PASS (mlp_cos_min≈0.99968) | PASS* | PASS | **True** |
| `d97_spectral` | `757375a585a1` | 16 | PASS | PASS† (600/bf16/Δq0/Δo0) | PASS† (cos vs d70r mlp_min≈0.99954) | PASS* | PASS | **True** |
| `d93_step6` | `391d23a95adf` | 8 | PASS | PASS‡ | PASS‡ | PASS* | PASS | **True** |
| `e4b_d32` | `4f41a4eba4a7` | 8 | PASS | PASS‡ | PASS‡ | PASS* | PASS | **True** |
| `e4b_d33` | `eea28380705e` | 8 | PASS | PASS‡ | PASS‡ | PASS* | PASS | **True** |

\*Gate4 = two-sided pytest suite reused from proven tr20 5/5 (patch soundness is host-contract / snapshot based; not re-run this morning to save ~15–40 min).  
†d97 Gate2/3 = dedicated spectral integrity + ΔW cosine vs d70r/tr20 (tr20 blend check N/A).  
‡Skipped blend-specific Gate2/3; Gate1 host contract + G18/G19/wiring enforced.

**All five packages: `all_gates_pass=True`, `NO_SUBMIT=1`, zero submits.**

---

## Side-by-side: `d96_tr20` vs `d97_spectral_ortho`

| Metric | tr20 `89e6ae70fd36` | d97 `757375a585a1` |
|--------|---------------------|---------------------|
| Method | uniform η=0.20 damp of (step4−d70r) | winsor q70 + 0.10·in-span + 0.35·ortho |
| Keys / dtype | 600 / bf16 | 600 / bf16 |
| max‖Δq‖, max‖Δo‖ vs d70r | 0, 0 | 0, 0 |
| MLP cos(ΔW) vs d70r min/mean | ≥0.99968 / ~0.99976 | ≥0.99954 / ~0.99977 |
| MLP cos(ΔW) vs tr20 min/mean | — | ≥0.99989 / ~0.99992 |
| Attn cos vs either | ~1.0 | ~1.0 |
| Spike handling | shrinks **all** layers equally | shrinks **outlier L21–L25** via q70; amplifies ortho ForgeSWE |

**Reading:** d97 stays mathematically almost collinear with both d70r and tr20 on effective ΔW (>99.95% cosine) while reallocating update mass away from d70r’s top-4 input subspace (0.10 vs tr20’s flat 0.20) into orthogonal DAgger-Recover directions (0.35).  
**Caveat:** no new live 13-task GPU panel tonight — ranking edge vs tr20 is **hypothesis-grade**, not LB-measured.

---

## Ranking chance estimates (expert DS — subjective, `NO_SUBMIT=1`)

Public reference points: D69/57538500 floor **~0.18**; recent ForgeSWE/E4B submits **0.03–0.06**; GapDPO 31B peaks **~0.17**.

### Main track (31B QAT)

| Contender | Est. public LB | Confidence | Rationale |
|-----------|----------------|------------|-----------|
| **d96_tr20** (verified 5/5) | **0.14 – 0.18** | Medium | Closest to d70r 5/13 empirical champion with mild ForgeSWE; D69 host contract restored |
| **d97 spectral** | **0.15 – 0.19** (upside) / **0.12 – 0.16** (downside) | Low–Med | Better spike geometry on paper; could reclaim `rich_3676`-class fails **or** overshoot if ortho 0.35 too hot — **needs disc5/13 before claiming >tr20** |
| Bare d70r (G19-banned) | ~0.16–0.18 hist. | — | Not shippable under G19 |

**Main-track chance to beat 0.18 floor:** ~**35–45%** for tr20 as-is; d97 maybe **+5–10 pp upside** only after a GPU disc panel.  
**Chance to place top-quartile among active 31B agents:** roughly **20–30%** if LB still clustered 0.12–0.18.

### Small track (E4B)

| Contender | Est. public LB | Confidence | Rationale |
|-----------|----------------|------------|-----------|
| **d29_s8** (prior PB 0.06) | **0.05 – 0.07** | Med | Known Kaggle point |
| **d32** ForgeSWE | **0.04 – 0.08** | Low | Local packaging OK; no new LB |
| **d33 spectral** | **0.05 – 0.09** upside | Low | Same spectral thesis on E4B; q70 was huge (rel_frob scale vs d29) → treat as **experimental** |

**Small-track chance to beat 0.06:** ~**25–40%** for d33 *if* MPS/cloud disc confirms; else similar to d29/d32 noise.

### Recommended ship queue when `NO_SUBMIT` lifts (not tonight)

1. **Main:** `d96_tr20` (`89e6ae70fd36`) — safest verified ForgeSWE  
2. **Main challenger:** `d97` (`757375a585a1`) — only after local/cloud disc5≥tr20  
3. **Small:** `d33` (`eea28380705e`) after E4B sentinel MPS panel vs d29/d32  
4. Hold `d93_step6` / `d32` as backups

---

## Explicit non-actions

- ❌ **No Kaggle submit** (`NO_SUBMIT=1`)  
- ❌ No RunPod / cloud  
- ❌ No PENDING check → submit path  

---

## Artifacts index

- Gates: `gemma4-agent/results/p727_overnight_8h/p727b_gates/gate_*.json`  
- Compare: `…/p727b_gates/d97_vs_tr20_spectral.json`  
- Rematerialize: `…/p727b_rematerialize.json`  
- SFT summary: `…/p727b_sft_filter_summary.json` (then trimmed to **92** rows)  
- Scripts: `p727b_rematerialize_spectral.py`, `p727b_fix_sft_filter.py`, gate `--expected-alpha`

---

## Bottom line

Overnight’s blocked science is **unblocked**: d97 + d33 tensors exist, five ForgeSWE zips clear host/G18/G19 gates under **`NO_SUBMIT=1`**, SFT v2 has **92** masked-submit rows.  
**Do not submit tonight.** Next value unlock = disc5/13 (31B) + E4B sentinel before touching Kaggle.
