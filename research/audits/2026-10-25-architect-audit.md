# Architect audit — 2026-10-25

**Audience:** architect / next implementer. No chat context required.  
**Purpose:** what was built, what transferred to the public board, what did not, current stand, next one-variable move.  
**Live log:** [`experiment_log.md`](../../../docs/experiment_log.md) (append-only; header status board is stale).  
**Visual:** open the companion canvas beside chat if reviewing in Cursor.

Checked at **2026-10-25 20:52 UTC** against the Kaggle submissions API.

---

## 0) Verdict in one paragraph

The team has a working single-agent 31B scaffold and a standing public score of **0.18** (two independent zips). Training Plan A (BoN → SFT → GRPO → TIES) compiled, served, and lifted smoke Pass@1 to 0.30, then **failed to transfer**: v2 LoRA scored **0.17**, true LoRA timed out at 8 min and scored **0.12** after the wall was cut to 6 min. The live bet is **P6.14** (`57628655`, PENDING): the public 8 min / 8192 / no-LoRA package, which is the only untested high-EV change versus our scored 7 min / 6144 zip. Daily quota is 0. Cloud approvals expire tonight. Do not start GPU or another submit.

---

## 1) Current stand

| Item | State |
| --- | --- |
| Public score (best) | **0.18** — `57076074` (P3.14a) and `57538500` (P6.11) |
| Live submit | **`57628655` PENDING** — P6.14 8 min / 28 calls / 8192 out / 4096 think / no adapter |
| Last scored | `57594583` = **0.12 DISCARD** (P6.13 6 min LoRA) |
| Frontier | **0.24** (4 teams); field 3756 teams; our rank **340** |
| Daily quota | **0 remaining** (1/day confirmed) |
| Model | `gemma-4-31b-it-qat-w4a16-ct` only (G6). 12B FAIL (P3.15a). |
| Topology | Single agent (GATE_P4 PIVOT) |
| Working-tree `agent/` | **FROZEN** — do not ship it; use staged zips under `gemma4-agent/results/` |
| Cloud | P6.11 + P6.12 `CLOUD_APPROVAL` expire **2026-10-25T23:59:59Z**. No live pods. |
| Paper track | Not entered. Deadline Nov 12. Notes in [`paper-notes.md`](../../../paper/paper-notes.md). |
| Finals | 2 selectable before Dec 2. If nothing better lands, keep the two 0.18 zips. |

---

## 2) What was done (phase trail)

| Gate / phase | Outcome | Meaning |
| --- | --- | --- |
| GATE_P0 / P1 | PASS | Splits, soundness, serve parity. Usable 111/129; 18 quarantined. |
| GATE_P2 | PASS | Smoke Pass@1 0.20 (v12 compaction). First official submit later 0.06. |
| GATE_P3 | **FAIL + scaffold_freeze** | failed_edit / loop KPIs never met. ≥2 edit-prompt A/Bs hurt Pass@1. Freeze was correct. |
| GATE_P4 | PIVOT single | Analyzer + coder skipped. |
| Harvest P5.1 | Mixed | Wave 1 keepers after srcpath/starlette gold fix; later rounds r7c/r7d yield 0. SFT coverage peaked then was pruned. |
| GATE_TRAIN_SHIP | PASS | LoRA r64 SFT → GRPO → TIES `master_swe_adapter` (0.912 GiB bf16). edit_in_window 100%. |
| GATE_P6 | PASS on smoke, fail on LB | P6.1b smoke 0.30 / failed_edit 0.0 → public **0.17**. Gate ≠ ship. |
| P6.8–P6.9 v3 | HOLD 0.18 | Surgical retrain; GRPO sprawl failed hard gates C1/C2. |
| P6.11 | 0.18, adapter noop | 7 min / 6144 frontier clone tied stand. Strict SFT A/B 2/10 vs 2/10 because adapter was not compiled in. |
| P6.12 | True LoRA proven, then timeout | `adapter: master_swe_adapter` required. B2 smoke 3/10 including `fastapi_14616`. 8 min LoRA → 14.2 h / 120 → **12 h timeout**. |
| P6.13 | 0.12 | Same LoRA, 6 min / 22 calls / 2048 think. Finished, quality collapsed. |
| P6.14 | PENDING | Base-only 8 min / 8192. Submitted 2026-10-25 11:45 UTC. |

---

## 3) What is working

1. **31B single-agent base with thinking on** is the only recipe that has scored 0.18 for us and 0.22 for the public Igor kernel (`flexonafft/gemma-4-budget-aware-coding-agent-v2`).
2. **`max_output_tokens: 8192` with `thinking_budget: 4096`**. 6144 leftover after thoughts is ~2048 tokens and truncates large `edit_file` calls (Hong v5 public 0.13).
3. **Anytime patch.** Host grades the working tree when time/calls expire. An edit that exists can score without `submit_patch`. An empty tree is always zero.
4. **Anti-rm / never-edit-tests.** Collection breakage is an automatic failure. Keep this in the prompt.
5. **Scaffold freeze after GATE_P3.** Edit-prompt lectures, grep-first, force-edit-by-12, host `old_string` caps, and 3.5 min walls all dropped smoke Pass@1. Do not reopen that class.
6. **Adapter compile hook is now understood.** `compile_submission()` routes to `openai/master_swe_adapter` only if `agent.yaml` contains `adapter: master_swe_adapter`. P6.11 “LoRA A/B” was a silent base-vs-base. P6.12 logged `compiled_agent_model_id` and closed that hole.
7. **True LoRA can solve a harder smoke task.** P6.12 B2 (`p68_v3_master`, α=32, r=64) resolved `fastapi_14616`; base and strict-α16 did not. That lift is real on n=10 and unused on the host clock.
8. **Hygiene and persist.** AppleDouble invalidates zip (P6.1). S3 holds `results/p612_true_lora_ab`, harvest, and soundness. Gold/oracle srcpath + starlette fix (P5.1a-r8) made BoN keepers trustworthy.

---

## 4) What is not working

1. **Smoke ≠ public board.** 0.30 smoke became 0.17 (v2) and 0.12 (tight LoRA). n=10 overfits `rich_3882` / `rich_3905`.
2. **LoRA Punica tax.** Mounting r64 on q/k/v/o/gate/up/down runs unquantized SGMV. Measured: base 16.6 tok/s, mean 334.5 s, 11.15 h / 120; LoRA 12.1 tok/s, mean 426.7 s, **14.22 h / 120**. Host cap is 12 h.
3. **Cutting the wall to fit LoRA destroys resolve.** P6.13 6 min / 22 calls / 2048 think scored **0.12** (−0.06 vs stand). Do not ship a slower model with a shorter budget.
4. **v2 / v3 trained adapters as shipped agents.** v2 public 0.17. v3 failed sprawl gates (C1/C2; e.g. fastapi_14609 20 edits). Strict-le3 SFT did not beat base once compile was honest (P6.11 arms 2/10 = 2/10).
5. **Early official stack (max_out 2048, thoughts off, wall 4–5).** Three submits at **0.06**. That ceiling is dead.
6. **Prompt-only “improvements” after a working budget.** P3.14b hard-context 0.17. Hong v6 prompt edits on Igor’s 0.22 config currently show public **0.13** / best 0.18. Do not spend a daily slot on system.md churn.
7. **Community 28/8 with the old prompt** was smoke 0.00 (P3.1). The later 0.22 public 28/8 is a *different* contract-first prompt plus 8192 out — not a rehabilitation of P3.1.
8. **Late harvest.** r7c / r7d yield 0. More BoN on the same freeze/temp is not the bottleneck.

---

## 5) Official submission ledger

| Ref | When (UTC) | Ticket | Config | Public | Verdict |
| --- | --- | --- | --- | --- | --- |
| 56892002 | 2026-10-06 | P2.7 | wall ~5, max_out 2048 | 0.06 | discard |
| 56909388 | 2026-10-07 | P3.8 | wall 4, kept scaffold | 0.06 | discard |
| 56935643 | 2026-10-08 | P3.8 probe | same | 0.06 | discard |
| 57017054 | 2026-10-09 | P3.13 | read-cap + exact old_str | 0.13 | direction only |
| **57076074** | 2026-10-11 | P3.14a | exact 0.18 repro | **0.18** | **STANDING** |
| 57128324 | 2026-10-13 | P3.14b | + hard context | 0.17 | discard |
| 57264570 | 2026-10-16 | unlabeled | unknown | 0.13 | discard |
| 57425395 | 2026-10-20 | P6.2 | v2 TIES LoRA, smoke 0.30 | 0.17 | discard |
| **57538500** | 2026-10-22 | P6.11 | 7 min / 6144, no LoRA | **0.18** | **STANDING** |
| 57570012 | 2026-10-23 | P6.12 | 8 min + true LoRA α32 | timeout | discard |
| 57594583 | 2026-10-24 | P6.13 | 6 min / 22 + LoRA | 0.12 | discard |
| **57628655** | 2026-10-25 | P6.14 | 8 min / 8192, no LoRA | **PENDING** | live |

---

## 6) P6.12 smoke (the last honest A/B)

Artifact: `gemma4-agent/results/p612_true_lora_ab/p612_smoke_abc_report.json`. Pod `w29b8gq7400iv2` terminated.

| Arm | Model | Pass@1 | Resolved | Mean s | Extrap h/120 | compiled_model_id |
| --- | --- | --- | --- | --- | --- | --- |
| A | base 31B | 0.20 | rich_3882, rich_3905 | 334.5 | **11.15** | `openai//models/gemma-4-31B-it-qat-w4a16-ct` |
| B1 | strict_le3 α16 | 0.20 | same two | 468.0 | 15.6 | `openai/master_swe_adapter` |
| B2 | p68_v3_master α32 | **0.30** | + fastapi_14616 | 426.7 | **14.22** | `openai/master_swe_adapter` |

B2 is the only arm with a hard-task win. It is also the only arm that cannot finish 120 tasks in 12 h at an 8 min cap.

---

## 7) What P6.14 is (and is not)

Zip: `gemma4-agent/results/p612_true_lora_ab/submission_024_v6_clean_8192.zip`  
SHA256: `3e4cf32e7c402079af906114c334483b894c2eb25ad72a9d07e440bbfc85426f` (4036 B)

| Knob | P6.11 (scored 0.18) | P6.14 (live) | Igor public 0.22 |
| --- | --- | --- | --- |
| max_time_minutes | 7 | **8** | 8 |
| max_output_tokens | 6144 | **8192** | 8192 |
| thinking_budget | 4096 | 4096 | 4096 |
| max_tool_calls | 28 | 28 | 28 |
| Graph tools in yaml | no | no | declared; prompt forbids |
| adapter | none | none | none |

This is a coupled wall+token restore, not a prompt rewrite. Hong v6 is prompt-only on Igor; that kernel now shows 0.13 / best 0.18 — do not treat the title “LB 0.24” as a measured clone. Four live teams are at 0.24 by unknown private deltas.

Risk: 8 min × 120 = 16 h worst case. Base smoke mean 334.5 s → 11.15 h, which is the same class as Igor. Guoxiang V7 is already retreating to 7 min / 6144 for clock fear (that is our P6.11).

---

## 8) Decision tree for the next daily slot

| If `57628655` … | Do this (one G3 variable) | Do not |
| --- | --- | --- |
| 0.22–0.24 | Hold. Select it as a final. | Touch prompt, wall, or adapter |
| ~0.18 | Declare Igor’s unused graph tools **xor** keep 8192 and drop wall to 7 min | Both at once; LoRA |
| 12 h timeout | 7 min / 8192 | LoRA; 8 min retry |
| ≤0.13 | Revert to standing 0.18 zip | Prompt churn |

LoRA stays shelved until a serve path removes the Punica tax or a smoke extrap is **≤ 10.5 h / 120** without cutting think/output.

---

## 9) Invariants (violation = invalid work)

- G4 holdout task IDs untouched.
- G5 zip = `agent/` contents only; no `._*`, no `.jinja`, &lt; 3 GiB.
- G6 one model: 31B QAT W4A16.
- G13 no PRM. Rank ≤ 64.
- Never override the freeze with working-tree `gemma4-agent/agent/`.
- Never start or scale cloud without a **live** `CLOUD_APPROVAL` row (both current rows expire tonight).
- One ablation variable per experiment.

---

## 10) Questions for the architect

1. Confirm LoRA is shelved until a faster serve path exists (two official fails; tax is measured).
2. If P6.14 ties 0.18, which single next slot: graph-tool declare, or 7 min / 8192?
3. Re-issue `CLOUD_APPROVAL` after 23:59 UTC, or stay CPU-only until the live score lands?
4. Enter the paper track by Nov 12? Notes exist; the paper competition is not accepted.
5. Leave the experiment_log status board stale (append-only), or allow a one-time header rewrite so dispatch stops pointing at P6.11?

---

## 11) Pointers

| Artifact | Path |
| --- | --- |
| Live log | `docs/experiment_log.md` |
| P6.12 smoke | `gemma4-agent/results/p612_true_lora_ab/p612_smoke_abc_report.json` |
| Live zip | `gemma4-agent/results/p612_true_lora_ab/submission_024_v6_clean_8192.zip` |
| Standing 0.18 (P6.11) | `gemma4-agent/results/p610_frontier_leader/` |
| Public kernels (2026-10-25) | `gemma4-agent/results/p614_public_kernels/` |
| Paper notes (stale vs P6.14) | `docs/paper-notes.md` |
| Prior harvest audit | `docs/2026-10-18-handoff-audit.md` |
