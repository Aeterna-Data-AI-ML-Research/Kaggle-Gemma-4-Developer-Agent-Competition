# P7.53 pod-run report — 2026-11-17T06:50:44Z

Spend **$6.56 / $14.00** · burn **$0.00/hr** · `live_pods=[]` · `NO_SUBMIT=1` · `NO_G3=1`

## Fleet

| pod | id | $/hr | state | reason | hours | cost | Arm1 | WT | strict |
|---|---|---|---|---|---|---|---|---|---|
| pod0 | `x1d0y4x8q7a7cc` | 0.59 | terminated | stage_done | 1.74 | $1.02 | 30/30 | 8 | 3 |
| pod1 | `sczbnryiwb376f` | 0.59 | terminated | stage_done | 1.70 | $1.00 | 30/30 | 12 | 6 |
| pod2 | `j6xnrm2jwb33lt` | 0.59 | terminated | stage_done | 1.66 | $0.98 | 30/30 | 8 | 8 |
| pod3 | `05n2g1fk8yin1w` | 0.59 | terminated | stage_done | 1.66 | $0.98 | 30/30 | 12 | 8 |
| pod4 | `yr2wlzobsdr7ne` | 0.59 | terminated | stage_done | 1.83 | $1.08 | 30/30 | 8 | 3 |
| train | `m6hw4qons319rj` | 3.19 | terminated | vanished @ step 4 | 0.47 | $1.50 | — | — | — |

## Arm1 — `a1_think1024` (tr20, seed 1, thinking_budget=1024)

- **150/150** · WT **48/150 (0.320)** · strict **28/150 (0.187)**
- vs Phase 1 **tr20_s1**: 48 vs 48 · Δ **0** (+0.000) · up/down 9/9 · 95% CI **[-0.060, +0.053]**
- vs Phase 1 **d69 mean**: 48 vs 46.5 · Δ **+1.5** (+0.010) · 95% CI **[-0.037, +0.057]**

| stratum | a1 | tr20_s1 | d69 mean |
|---|---|---|---|
| competition_new | 14/35 | 11/35 | 10.0/35 |
| competition_public | 7/23 | 7/23 | 8.0/23 |
| other | 27/92 | 30/92 | 28.5/92 |

- End reasons a1: `{'time_budget': 77, 'submitted': 45, 'tool_budget': 28}`
- End reasons tr20_s1: `{'time_budget': 85, 'submitted': 34, 'tool_budget': 31}`
- Thinking cap: turns with est. thought >1024 → a1 **3/150** vs base **63/150**

## Arm2 — ForgeSWE train (incomplete)

- H100 NVL `m6hw4qons319rj` vanished after step **4/25** (no volume). Not recreated.
- step_0 eval: dev loss_token 0.0985 · compnew 0.0740
- steps 1–4 train loss: 0.057 → 0.099 → 0.057 → 0.172
- On disk: `step_0` only. No step_12/25 · no `rel_frob` / `mlp_cos_min`

## Verdict

- **`thinking_budget=1024` does not beat uncapped tr20_s1 on calib** (Δ=0, CI includes 0).
- Slightly above d69 mean (+1.0 pp) but CI includes 0.
- Auto-termination: all 5 Arm1 pods `stage_done`. Cap held ($6.56 ≪ $14).
- **No G3. No submit.** Waiting for operator.
