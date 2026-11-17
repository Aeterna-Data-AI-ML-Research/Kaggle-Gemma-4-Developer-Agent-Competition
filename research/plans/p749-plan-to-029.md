# P7.49 — Plan to 0.29 (PROPOSED, not approved)

**Status:** Phase 0 approved and running on local CPU ($0) · Phases 1–4 still proposed · `NO_SUBMIT=1` · `CLOUD_APPROVAL=NO` · no GPU started
**Revised 2026-11-16** with three operator corrections (marked C1–C3 below). Where this revision and §7 disagree, this revision wins.
**Evidence base:** [`P748_DS_SCORE_DIAGNOSIS.md`](../../../gemma4-agent/results/p748_ds_score_diagnosis/P748_DS_SCORE_DIAGNOSIS.md)

## 1. The target in task counts

| Fact | Value | Source |
| --- | --- | --- |
| Hidden tasks | about 120 (score lattice allows 77–78 or 93+) | competition-roadmap §2, P7.48 |
| Our best | 0.18 ≈ 22 of 120 | `58010294` and three others |
| Target | 0.29 ≈ 35 of 120, so **+13 tasks** | — |
| Modified packs | 0.13 ≈ 16 of 120, so 6 tasks below base | P7.48 |
| Final ranking | private half (about 60 tasks) | competition-roadmap §2 |
| Time budget | 12 h for all tasks, so about 5.25 min mean per task with margin | P7.06 extrapolation rule |
| Host speed | about 14 tok/s per episode, so about 4,400 generated tokens per task on average | playbook P7.31 |
| Deadline | final submit 2026-12-02 23:59 UTC; 1 submit/day; 2 final picks | competition-roadmap §3 |

One leaderboard run on 60 private tasks has a standard error of about 0.05. Public 0.24s that are lucky draws will fall back there;
a pack that is really better holds its gain. The plan therefore optimises true solve rate, not the public number.

## 2. Why the last two months did not move the score

- Ideas were judged on 9–13 local tasks (error about ±0.16) or on one leaderboard run per day.
- Each submission changed several things at once, with no control.
- Training used 96 rows and 8 optimizer steps; every scored adapter is within 2% of its parent.

Fixing the measurement comes first. Everything after it is decided by gates.

## 3. Phases

### Phase 0 — Build the instrument (Nov 16–18, $0, this Mac + Docker)

| Step | Output |
| --- | --- |
| 0.1 Verifier check | Re-grade stored patches from past runs in the 4 GiB / 2 vCPU sandbox; verdicts must reproduce. |
| 0.2 Task pool ≥ 300 **(C3)** | 98 non-holdout public tasks plus ≥ 200 mined from merged PRs of an 11-repo allow-list of fast-building pure-Python projects: `fastapi`, `starlette`, `pydantic`, `rich`, `requests`, `httpx`, `click`, `flask`, `pytest`, `attrs`, `urllib3`. No C-extension compilation. Same recipe as the public set (PR number, first-parent base commit, source diff, test diff, PR title + body). Two-sided soundness on local CPU: `empty_patch == FAIL` and `gold_patch == PASS`; target under 4 hours for the whole pool. PR numbers already in the public file, holdout included, are excluded. |
| 0.3 Budget emulation | Episode ends at 28 tool calls or a completion-token cap equal to the host's 7 min at 14 tok/s. No wall-clock dependence, so GPU type and batching do not change results. |
| 0.4 Protocol, frozen before any run | Paired arms on identical tasks; 2 seeds per arm at ship temperature **(C2)**; paired bootstrap over tasks; results reported per stratum (competition repos vs other repos). |
| 0.5 Splits | `calib` (150 stratified tasks, Phase 1), `test` (the other ≥ 150, opened only for go/no-go), `train` (harvest only), existing 31-task holdout untouched (G4). No PR appears in two splits. Newly mined tasks from the four competition repos are eval-only by default, because they may coincide with hidden tasks. |

Sensitivity: the error on a paired difference is about sqrt(d / n), where d is the share of tasks whose verdict differs
between the two arms. At n = 150 that is 1.8 points if d is 5% and 2.6 points if d is 10%; at n = 300 it is 1.3 and 1.8.
d is unknown until Phase 1 measures it.

### Phase 1 — Calibrate against the leaderboard (Nov 19–20, GPU)

**Design (C2):** 3 arms × 2 seeds × 150 stratified tasks = **900 episodes**, instead of 5 packs × 3 seeds × 300 = 4,500.

| Arm | Vault zip | Leaderboard |
| --- | --- | --- |
| D69 base, the floor | `376e932c75dd` | 0.18 (`58010294`) |
| ForgeSWE tr20 | `89e6ae70fd36` | 0.17 (`58244433`) |
| ForgeSWE scale10 | `e2c6e9c807a5` | 0.13 (`58320693`) |

- The ForgeSWE 0.17 arm is `58244433` only. `58372147` scored 0.13, so it is not a 0.17-class pack.
- Operator estimate: about 18 GPU-hours for the 900 episodes (about 50 episodes per GPU-hour). Unmeasured; the first
  GPU hour restates it.
- Harvest by-product: the D69 and tr20 arms give 600 real episodes. At a 17–18% solve rate about 100 of them pass
  two-sided verification and are usable as training rows; the failures feed DAgger-Recover (Phase 3A).
- **Gate G1 — pass:** D69 beats scale10 with a paired interval that excludes zero.
- **Extension rule:** if that interval still includes zero after 150 tasks, run D69 and scale10 on the remaining ≥ 150
  tasks (+600 episodes) before calling G1 failed. At 10% discordance, 150 tasks detect a 5-point gap only about half the time.
- **Gate G1 — fail:** spend at most two days finding the mismatch (budget emulation first). If it stays unexplained,
  stop: the instrument does not see what the host sees, and we hold the current standing.

This phase also answers the open P7.48 question (are the adapter packs really worse than base, or was it the host) without
using a submission.

### Phase 2 — Map the headroom (Nov 20–22, GPU)

Each arm changes one thing against D69 (G3). The result is an upper bound on what that lever can gain.

| Arm | Question it answers |
| --- | --- |
| Gold file given | How many failures are localization failures? |
| Token budget doubled | How many failures are just running out of budget? |
| Best of 4, oracle pick | How much is sampling variance (ceiling for any multi-attempt scheme)? |
| Best of 4, pick by the task's own failing test | How much of that ceiling is reachable without the oracle? |
| Failure census | Empty patch at budget end / wrong file / right file wrong fix / breaks other tests. |

- **Gate G2:** fund only levers that show at least +8 tasks per 100. If none does, scaffold changes cannot reach the
  target and only training remains.

### Phase 3 — Pull the funded lever (Nov 20–26, GPU)

Listed in order of prior odds. Data generation for 3A starts as soon as G1 passes, because it is the long pole.

**3A. Self-distillation at scale (BoN + STaR), ForgeSWE continuation.**

- **Data rule (C1): on-policy only.** Every row used for multi-hundred-step SFT or GapDPO comes from a real 31B rollout
  (D69 or a ForgeSWE adapter) under the exact ship prompt and budget that passed two-sided verification.
  Trajectories compiled backward from gold patches (`forgeswe/causal_compiler.py`) are **not** training data: they teach
  jumping straight to the right file and submitting after one edit, which the model cannot do without the gold patch.
- **Repairs: causal DAgger-Recover at real branch points only.** A repair row is spliced into a real failed rollout at
  the turn where it actually went wrong: right after a failing `pytest` result, or where a companion edit was missed.
  The prefix up to that turn is the model's own; only the continuation is corrected, and the spliced episode must pass
  two-sided verification. No synthetic prefixes, no marker faults.
- Tasks: the `train` split of the mined pool plus the existing 40-task train pool. `source=` and `license=` recorded
  per row (G10); closed-model teachers stay blocked.
- Volume: Phase 1 supplies about 100 passing rollouts. The rest comes from best-of-4 rollouts on the `train` split,
  cap 2 kept per task. The target is at least 1,000 verified rows; whether the pool is large enough is a Phase 0 output.
- Training: one continuous adapter from the ForgeSWE lineage, real optimization (hundreds of steps, not 8). Rank 8 vs 16
  and attention-lock on vs off are separate arms.
- Throughput guard: a candidate must keep episode speed within 10% of base. Recorded cost: rank 8 about 7% slower,
  rank 64 about 45% slower, and a slow adapter loses tokens under the 12 h wall.

**3B. Budget shaping (only if the doubled-budget arm shows headroom).** The limit is the 12 h total, not the per-task cap.
Cut what failed episodes burn and give it to the rest, as a single budget variable.

**3C. Multi-attempt (only if best-of-4 by own test shows headroom).** Must be budget-neutral under the 12 h wall; the
previous sequential pack went blank on time.

- **Gate G3:** a candidate beats D69 on the untouched `test` split by at least +4 tasks per 100, interval excluding zero,
  in both strata.

### Phase 4 — Confirm and select (Nov 27 – Dec 2)

- No submission before a candidate passes G3. At most 4 confirmation submits; last one by Nov 30 so the score lands in time.
- Final picks: the best G3 candidate, plus an already-scored submission as the floor (`58010294` at 0.18 or `58244433`
  at 0.17). The floor needs no new submit, so the downside is the current standing.

## 4. What this plan will not do

Soups or blends, retired prompt-graft packages, temperature lotteries, edits to `gemma4-agent/agent/`, training on
`sft_p747_dagger_v7_surgical_7036b.jsonl` (synthetic placeholders), tuning on the holdout, or any submit that is not ForgeSWE-main.

## 5. Cost and odds

| Phase | GPU-hours (estimate, 48 GB card) |
| --- | --- |
| 0 | 0 |
| 1 | about 18 (operator estimate for 900 episodes; +12 if the extension rule fires) |
| 2 | 15–30 |
| 3 | 100–140 (on-policy generation, training 20–40, candidate evals 20–30) |

These are estimates from recorded per-row training time and an assumed batched serving rate. The first GPU hour measures the
real rate, and the numbers get restated before continuing. Nothing starts without `CLOUD_APPROVAL=YES` in the experiment log.

Odds (judgment, not measurement): reaching the calibrated instrument is likely. A real gain of 3–6 tasks from 3A is plausible
and is what the published 32B-class fine-tuning results suggest is possible with thousands of trajectories; our own writeup
review found nothing below 1,000 trajectories that moved a 31B. Reaching +13 needs 3A and one of 3B/3C to both land. One team
in 4,378 is there.

## 6. Open items to confirm in Phase 0

- Whether hidden tasks come from the four public repos or from others (decides the stratum weights).
- Whether the rules allow training on PRs from the four competition repos that are not in the public file. Until that is
  confirmed, those tasks are eval-only.
- Native macOS verdicts must be re-checked once on the Linux pod before Phase 1 counts them.
- Licences and sizes of the open task sets, and how many environments build inside the sandbox limits.
- Batched serving rate for the 31B on the chosen card.

## 7. Fast track using ForgeSWE (added 2026-11-16) — PARTLY SUPERSEDED

> **Superseded by C1:** the `causal_compiler.py` row of the table, the "compile ForgeSWE rows" and "train on the
> compiled rows" steps of the schedule, and the Nov 20 first-submit date. Compiled gold-patch trajectories are not used
> for training. What survives: reuse of the existing harness, the SurgicalTune trainer with a lifted step count, and
> DAgger-Recover in the restricted form defined in Phase 3A. Generation is back on the GPU, so the first confirmation
> submit returns to the Phase 4 window (Nov 27 onward) unless Phase 1 rollouts arrive faster than estimated.

What already exists and what it removes from the plan above:

| ForgeSWE asset | What it is | Effect on the plan |
| --- | --- | --- |
| `scripts/p692_live_gpu_harness.py` (2,529 lines) | Multi-turn agent loop, tool-call cap, two-sided pytest, resumable, threaded | Phase 0 shrinks to adding the token cap and paired statistics: about 1 day instead of 3. |
| `forgeswe/causal_compiler.py`, `dagger_recover.py` | Turn a gold patch into a DiffGuard-checked training trajectory on CPU, no model | Replaces the BoN generation step (about 55 GPU-hours and 4 days). Thousands of rows in hours on this Mac. |
| `forgeswe/forge_gym.py` | AST fault injection (OP1–OP3) | Not usable as-is: faults carry literal markers (`forgeswe_missing_attr`, `orphan_remnant_forgeswe`). Needs realistic operators before it counts as a task source. |
| `p726_train_d96_forgeswe.py` + yaml | SurgicalTune trainer | Reused, but the 8-step / lr 1.5e-5 contract must be lifted to real optimization or the adapter again stays within 2% of its parent. |

Compressed schedule:

| When | Work | Cost |
| --- | --- | --- |
| Nov 16–17 | Token cap + paired stats on the existing harness; compile ForgeSWE rows from every non-holdout gold patch and from open task sets with gold patches. | $0 |
| Nov 18–19 | Two pods in parallel. Pod A: calibration on the five known packs. Pod B: train 2–3 ForgeSWE candidates on the compiled rows, then evaluate each paired against D69. | 60–90 GPU-hours (estimate) |
| Nov 20 | Gate G3 on the untouched test split. First confirmation submit if a candidate passes. | — |
| Nov 21–Dec 2 | About 8 remaining slots for iteration instead of 4. Headroom arms (old Phase 2) run alongside, not as a blocker. | — |

Trade-offs of the fast track:

- Compiled rows are built with knowledge of the gold patch (search → read → exact edit). Whether training on them at
  real strength teaches the model to solve tasks has never been measured here; every adapter so far took 8 steps.
  The P7.31 writeup review lists short teacher-style trajectories as a default ban, so this is a real risk.
- Hedge at no extra cost: the calibration runs of D69 (300 tasks × 3 seeds) produce real passing trajectories as a
  by-product. If compiled rows fail G3, those plus further BoN runs are the fallback, which is the original Phase 3A.
- The calibration gate G1 is not skipped. Without it a candidate's offline win means nothing.

## 8. Phase 0 status (2026-11-16T11:17:30Z, local CPU, $0)

| Step | State | Result |
| --- | --- | --- |
| 0.1 Verifier check | not started | Grader will reuse the gold-phase code path of `p750_soundness_two_sided.py`. |
| 0.2 Task pool | eval pool done; train pool still being checked | 300 sound eval tasks. Pass 2 over the remaining 1,418 candidates is running. |
| 0.3 Budget emulation | not started | The host budget is session wall clock (generation plus tool time), so the emulation is a virtual clock, not a pure token cap. |
| 0.4 Protocol | statistics done, protocol not frozen | `p750_paired_stats.py` self-test passes (null coverage 0.96). |
| 0.5 Splits | written, eval frozen | `gemma4-agent/configs/p750_pool_splits.json`: calib 150, test 150, train 108 so far. No holdout id, no duplicates. |

**Mining (C3).** 1,913 candidates from merged PRs since 2023-07 across the 11 allow-listed repos:
pydantic 797, pytest 426, starlette 176, urllib3 134, click 133, fastapi 119, attrs 55, httpx 37, flask 20, rich 11, requests 5.
All eleven licences are MIT, BSD-3-Clause or Apache-2.0.

**Soundness so far.**

| Set | Checked | Sound |
| --- | --- | --- |
| Public, non-holdout | 98 | 92 |
| Mined, pass 1 (up to 60 per repo) | 495 | 326 |

- Unsound mined tasks are mostly PRs whose tests already pass without the fix (87), then environment failures.
- Cost: median 7.7 s per task, 2.6 CPU-hours in total for both sets; each pass took under 25 minutes of wall time on 6 workers.
- Verdict rule matches the host's main criterion (pytest exit code 0, at least one test passed). The host's extra
  "required test nodes not skipped" check is not replicated yet.

**Eval pool (300).** 45 public (smoke + dev) · 72 new PRs from the competition repos · 183 from the other seven repos.
Calib and test each hold 150, split within stratum and repo.

**Deviations from the corrections as written, for operator review.**

- *C3, "98 non-holdout public tasks" in the eval pool:* only the 45 smoke + dev tasks are used. The 40 train-pool tasks
  are where the existing adapters' training trajectories came from, so they would favour the adapter arms.
- *C3, RAM budget under 50 MB:* clarified by operator — parent/orchestrator only. Child pytest ≤350 MB; workers ≤4. Measured child peaks 76 MB median / 290 MB max → inside the child cap.
- *C2, SE ≤ 1.8 points at 150 tasks:* holds only if at most about 5% of tasks differ between arms. A simulation with
  2 seeds gave 2.4 points at 150 tasks and detected a 6-point gap 60% of the time (84% at 300 tasks). The extension
  rule in Phase 1 covers this.
- *C2, "harvests 600 real trajectories":* 600 episodes, of which about 100 are expected to pass and be usable as rows.

**Findings that affect later phases.**

- Tasks dated before November 2023 need Python 3.11; compiled dependencies had no Python 3.12 wheels then.
- The caller's `NO_COLOR` / `FORCE_COLOR` / `TERM` change test outcomes in rich; the runner uses a clean environment.
- Three eval tasks hang on the unpatched code (`rich_3480`, `urllib3_3797`, `urllib3_4974`). Each costs the full
  240 s timeout whenever an agent patch does not fix it.
- Inside the public set's date window (to 2026-06-20) the four competition repos have 107 further candidates under
  these filters, 42 sound of the 101 checked. They cannot fill a 120-task hidden set on their own, so the hidden set
  draws on something more: other repos, looser filters, or both. Unconfirmed.
- Verdicts are from native macOS. They must be re-run once on the Linux pod before Phase 1 uses them.


## 8b. Phase 0 COMPLETE (local CPU)

See `gemma4-agent/results/p750_phase0/P750_PHASE0_COMPLETE.md`. Protocol awaiting APPROVE: `gemma4-agent/configs/p750_phase1_protocol.md`. Pass-2 may still enrich `train`.

## 9. Operator decisions (2026-11-16 13:20 UTC+2) — LOCKED

1. **RAM:** `<50 MB` applies to the parent/orchestrator only. Pytest child peak ≤350 MB; concurrent workers ≤4.
2. **Eval public tasks:** 45 smoke+dev only. Confirmed. `train_pool` stays out of calib/test.
3. **Competition-repo mined PRs:** eval-only. Confirmed. Zero rows in `train`.
4. **Vault manifest:** rewrite approved. `ALL_VAULT_AND_MEMORY_CHECKS_PASS = True` after rewrite.
5. **Cloud:** `CLOUD_APPROVAL=NO` until Steps 0.1–0.5 complete and the frozen Phase 1 protocol is reviewed.
   Protocol draft: `gemma4-agent/configs/p750_phase1_protocol.md`.
