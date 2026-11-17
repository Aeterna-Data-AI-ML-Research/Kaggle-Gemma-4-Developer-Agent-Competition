# Evaluation protocol (virtual clock + two-sided soundness)

This document describes the measurement protocol used for the calibration campaign
shipped in `evidence/`. It is a sanitized research summary of the frozen Phase-0/1
protocol (internal ticket family P750–P753).

## Task splits

Frozen in `benchmark/tasks_manifest.jsonl` (730 tasks):

| Split | n | Role |
| --- | ---: | --- |
| `calib` | 150 | model / scaffold / harness comparisons |
| `test` | 150 | sealed go/no-go (IDs listed; **no graded test trajectories** in this release) |
| `train` | 426 | trajectory harvest / training only |
| `holdout` | 4 | `reserve_eval` — competition-repo extras, eval-only |

Calib stratum mix: 23 `competition_public` + 35 `competition_new` + 92 `other`.

Holdout / quarantine pools beyond these frozen IDs were never assigned into calib/test.

## Two-sided soundness

A mined task entered the pool only if:

1. the empty agent patch failed the task tests;
2. the gold patch passed the same tests.

Grading applies the agent patch, applies the task `test_patch`, then runs pytest on
the test-patch targets. Pass requires pytest exit 0 and at least one passed test.

## Virtual clock

Host wall-clock is not used as the episode budget. Each episode bills:

- **generation:** `completion_tokens / r_gen` seconds (`r_gen ≈ 14.0` tok/s for the
  unadapted baseline; LoRA arms use the measured Punica parity rate);
- **tools:** measured tool wall seconds.

Hard cutoff: **420 virtual seconds**. Soft notices at 330 s and 375 s were used in
Phase 2 harness arms. Container setup time is excluded (clock starts at session start).

Other budgets used in the campaign: `max_tool_calls=28`, command timeout 240 s.

## Pass definitions

- **Working-tree (WT) pass:** final working-tree patch grades green, whether or not
  the agent called `submit_patch`.
- **Strict pass:** WT pass **and** a recorded `submit_patch`.

## Statistics

Paired comparisons average per-task differences, then take a percentile bootstrap
over tasks (10,000 resamples, seed 0) for 95% intervals. One experimental variable
changes per phase.

## Phases in this release

1. **Phase 1 (900 eps):** arms `d69`, `tr20`, `scale10` × seeds `{0,1}` on calib.
2. **Phase 2 (300 eps):** harness `P2_A` (clock notices) vs `P2_B` (clock + pre-submit
   pytest gate) on the Phase-1 winner config.
3. **Phase 3 (150 eps):** `thinking_budget=1024` vs Phase-1 `tr20` seed 1 (`4096`).
