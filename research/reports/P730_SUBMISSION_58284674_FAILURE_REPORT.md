# Failure Report — Kaggle `58284674` (P7.30 d100 spectral)

**Queried:** 2026-11-13T14:55Z via Kaggle API · **Verdict:** **DISCARD**

| Field | Value |
| --- | --- |
| ref | **`58284674`** |
| status | `COMPLETE` |
| **publicScore** | **`0.13`** |
| Δ vs standing floor `0.18` | **−0.05** |
| Δ vs prior ForgeSWE `58244433` tr20 `0.17` | **−0.04** |
| submitted | 2026-11-12 20:50:43Z |
| description | `P7.30_ForgeSWE_v3_31B_d100_best_spectral_a16_think4096_out6144_6tools_V2_4of9_bd7d01af700e` |
| vault zip | `gemma4-agent/proprietary_vault/zips/p730_31b_d100_best_forgeswe_v3_spectral_a16_think4096_out6144_6tools.zip` |
| sha12 / sha256 | `bd7d01af700e` / `bd7d01af700e5e315b6fe23341f5499ca447e6c2ec41e9854fdfa3805296a113` |
| zip bytes | 83,937,547 |
| G18 / G19 at submit | PASS / PASS |
| Pre-submit local panel | **4/9** (est band `hold_<=0.18`; unlock≥6/9 **not** met) |

Same public bucket as retired prompt-graft **`57946188` D62b = 0.13**. Do **not** resubmit this zip.

---

## 1. What was shipped

| Knob | Shipped value | D69 `58010294` (0.18) | tr20 `58244433` (0.17) |
| --- | --- | --- | --- |
| Model | `gemma-4-31b-it-qat-w4a16-ct` | same | same |
| Prompt | 7036B / `3693fd62ff40` | same | same |
| Tools | 6T lean | 6T | 6T |
| Adapter | `p726_champion` = **d100 spectral s6** | none / prior | d96 tr20 SurgicalTune |
| Keys | **600** (q/o/gate/up/down ×120) | — | 600-class |
| `lora_alpha` / `r` | **16 / 8 → served scale 2.0** | — | **16 / 8 → 2.0** |
| Attn lock | `max_abs_dq=max_abs_do=0` (meta) | — | SurgicalTune |
| Spectral meta | `η_in=0.05`, `η_ortho=0.45`, `L=60` | — | n/a |
| `temperature` | **0.0** | **0.2** | 0.0 |
| `include_thoughts` | **omitted** (null) | **true** | omitted |
| `thinking_budget` | 4096 | 4096 | 4096 |
| → `enable_thinking` | True (budget>0 branch) | True | True |
| `max_output_tokens` | 6144 | 6144 | 6144 |
| `max_tool_calls` | **28** | 28 | 28 |
| `max_time_minutes` | 7 | 7 | 7 |

Host wiring was correct (`adapter: p726_champion` + weights). This was **not** a silent Base-model miss (contrast D70 `58102947` class).

---

## 2. Pre-submit evidence (why we still shipped)

From `docs/OVERNIGHT_P730_STAGE2_GM.md` + `results/p730_stage2_gm/main_track_submit.json`:

| Arm | 9-task resolved |
| --- | ---: |
| tr20 proxy | 5/9 |
| M1 d98 buggy | 4/9 |
| V1 d98_v2 true-scale | 3/9 |
| **V2 d100_best (shipped)** | **4/9** |

- V2 only flipped **`requests_6644`** vs V1; shared solves: `fastapi_14301`, `rich_2725`, `rich_2943`.
- Still miss: `rich_3676`, `fastapi_14873`, `rich_3052`, `rich_4077`, `rich_3521`.
- Gate said **`unlock_NO_SUBMIT_0 = false`** (need ≥6/9). Operator override submitted anyway after quota note `0 submissions remaining today` post-upload.
- Contrastive Phase1 win% flat **63.6%** for all spectral arms — MAD vs d98 tiny (`~6e-4`); **no Tier-2 unlock signal**.

**Forecast error:** local 4/9 ≈ “hold ≤0.18” assumed noise around the floor. LB realized **0.13** — a **capability regression**, not floor noise.

---

## 3. Post-submit forensics (P7.31 local panels on related arms)

Later clean 2-phase benches (Hard-34, often with drifted WT prompt / thinking-off harvest) showed the same hard tasks keep failing:

| Failure mode | Tasks (examples) |
| --- | --- |
| Tool-call budget exhaustion (28→34 still hit) | `rich_3676`, `rich_3052` (0-patch or empty edit) |
| Wrong / incomplete patch (pytest FAIL) | `requests_6644`, `fastapi_14873`, `rich_4077` (`isatty`), `rich_3521` (emoji split), `rich_3052` (prompt case_sensitive) |
| Fuse / schema bugs on edit args | `rich_2943` backtick → missing `old_string` (V2 fuse autopsy) |
| Thought channel silent in local harvest | `thought_pct≈0` when `include_thoughts:false` forced; median completion ~35–37 tok (tool-only) |

P7.31 Gate2 later **banned served scale >1.0** and **L30_59 / mlp_only strips** after 600-key scale≤1.0 twins hit **68.2%** win while strips collapsed to ~50–54%. The **shipped d100 zip used scale 2.0** — same α packaging as tr20 (0.17), so scale alone does not explain 0.13; the **spectral weight update** is the differentiating variable vs tr20.

---

## 4. Causal ranking (most → least likely)

1. **Spectral d100 weights hurt hidden-set generalization** vs tr20 SurgicalTune (0.17) and vs bare D69 (0.18). Panel +1 task was not a reliable uplift signal; contrastive MAD≪1 did not predict live Tier-2 flips.
2. **Served scale 2.0** amplifies whatever is in the adapter — safe-ish for tr20, toxic for spectral d100. Post-hoc P7.31 ship law: prefer **α≤8 (scale≤1.0)** / `d98_v2_scale075_a6`.
3. **Pre-unlock submit** (4/9 < 6/9) — process failure; forecast band was optimistic.
4. **temp=0.0** vs D69 **0.2** — secondary; tr20 also used 0.0 at 0.17.
5. **Soft-28 only** — secondary; standing 0.18 packs also Soft-28.
6. **`include_thoughts` omitted** — still `enable_thinking=True` via budget; not the primary differentiator vs D69 (`include_thoughts:true`).
7. **Not** host LoRA wiring failure; **not** wrong prompt bytes (7036 confirmed).

---

## 5. Score ladder context (team Moran Zavdi)

| ref | public | note |
| --- | ---: | --- |
| **57538500 / 57076074 / 58010294** | **0.18** | Standing floor / D69 |
| 58244433 tr20 | 0.17 | Best ForgeSWE-main so far |
| 58102947 / 58068476 D70 | 0.17 | GapDPO |
| **58284674 d100 spectral** | **0.13** | **This failure** |
| 57946188 D62b prompt graft | 0.13 | Retired Hard Graveyard |
| 58174836 soup | 0.12 | Soup ban |
| E4B recent | ≤0.06 | Small-model track |

---

## 6. Do / Don't

**Do**
- Treat **`58284674` / `bd7d01af700e` as DISCARD** (−0.05 vs floor).
- Keep **`NO_SUBMIT=1`** until a ForgeSWE-main zip clears local ship gate with **scale≤1.0**, D69 **7036** prompt, **`include_thoughts: true`**, and panel **≥6/9** (or stronger Tier-2 evidence).
- Prefer staged **Cand A** `d98_v2_scale075_a6` (600-key, scale 0.75) over spectral a16.
- Prefer continuing SurgicalTune / DAgger on strong bases over spectral ortho blends sold as ship adapters.

**Don't**
- Resubmit `p730_…d100_best_…spectral_a16…zip`.
- Ship served **scale 2.0** spectral / midband experiments as main.
- Override `unlock_NO_SUBMIT_0` on 4/9 again.
- Confuse this with prompt-graft D62b — same score, different mechanism (LoRA spectral vs prompt).

---

## 7. Artifacts

- Submit record: `gemma4-agent/results/p730_stage2_gm/main_track_submit.json`
- Overnight GM: `docs/OVERNIGHT_P730_STAGE2_GM.md`
- Vault zip (immutable): `…/p730_31b_d100_best_forgeswe_v3_spectral_a16_think4096_out6144_6tools.zip`
- Follow-on forensics: `gemma4-agent/results/p731_gpu_clean_2phase/p731{b,c,d,e}_*.json`
