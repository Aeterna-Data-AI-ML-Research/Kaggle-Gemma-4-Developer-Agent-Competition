# P7.50 Phase 1 protocol — APPROVED

**Status:** protocol **APPROVED** 2026-11-16 by operator · **`CLOUD_APPROVAL=YES`** since 2026-11-16T13:54:16Z (P7.51f, 5 pods × 180 episodes) · `NO_SUBMIT=1`
**Spend:** `$1.34` spent on the aborted P7.51d launch (0 valid episodes). Hard cap for **Phase 1 + Phase 2 combined**: **`$42.00`** (operator directive 2026-11-16 ~16:14Z; was `$36.00` then `$16.00`). Projected Phase 1 ≈ $29–32 at ~22 eps/hr/pod; Phase 2 adds 300 episodes on warm vLLM (no model reload).
**Authority:** `competitions/agent/plans/p749-plan-to-029.md` (C1–C3) + operator decisions of 2026-11-16 13:20 UTC+2 + DECISION APPROVE of 2026-11-16 ~12:00Z.
**Phase 1 may run only under this APPROVED protocol + live `CLOUD_APPROVAL=YES` in `docs/experiment_log.md`.**

## 1. Task set

| Split | File | n | Role |
| --- | --- | --- | --- |
| `calib` | `configs/p750_pool_splits.json` | 150 | Phase 1 Gate G1 |
| `test` | same | 150 | sealed until G3 |
| `train` | same | growing | harvest / DAgger only |
| `reserve_eval` | same | growing | extra competition-repo tasks, eval-only |

- Strata: `competition_public` (45 smoke+dev) · `competition_new` (mined fastapi/rich/requests/httpx, eval-only) · `other`.
- **Calib composition (measured 2026-11-16):** 23 `competition_public` + 35 `competition_new` + 92 `other` = 150 (the other 22 public tasks are in `test`). Phase 1 reads the single file `data/p750_pool/calib_150_tasks.jsonl` (sha256-12 `3c240cefe09d`, built and verified by `scripts/p751_build_calib_tasks.py`; ids == frozen `calib` split, in order).
- Holdout (31) and quarantine never appear.
- Calib/test are frozen; later sound tasks only extend `train` / `reserve_eval`.

## 2. Arms (G1)

| Arm | Vault sha12 | LB score | Notes |
| --- | --- | --- | --- |
| D69 base | `376e932c75dd` | 0.18 | floor |
| ForgeSWE tr20 | `89e6ae70fd36` | 0.17 (`58244433`) | not `58372147` (that scored 0.13) |
| ForgeSWE scale10 | `e2c6e9c807a5` | 0.13 (`58320693`) | |

3 arms × 2 seeds × 150 calib tasks = **900 episodes**.

## 3. Budget (host-faithful)

| Knob | Value | Source |
| --- | --- | --- |
| `max_tool_calls` | 28 | Soft-28 ship |
| `max_time_minutes` | 7 | Soft-7 ship |
| `timeout_seconds` | 240 | command timeout |
| `max_turns` | 80 | ship eval_config |
| Session clock | **virtual** | `scripts/p750_virtual_clock.py` |
| Generation charge | `completion_tokens / r_gen[arm]` s | **arm-specific** (Punica) |
| `r_gen` D69 base | **14.0 tok/s** | Soft-7 planning rate |
| `r_gen` tr20 / scale10 (rank-8 LoRA) | **14.0 × 0.929 = 13.006 tok/s** | P7.06 measured parity (14.59→13.55) |
| Tool charge | measured tool wall seconds | same work → same bill |
| Prompt | D69 7036B `3693fd62ff40` | ship lock |
| Temperature | arm's ship sampling | D69 0.2 / top_p 0.95; tr20 **0.0**; scale10 0.2 / top_p 0.95 (read from the hash-verified zips) |
| Skills | as wired in each zip's `agent.yaml` | D69 none; tr20 4 skills (ADK SkillToolset: +4 unbudgeted tools, + skill system instruction); scale10 none |
| Serving | vLLM `--max-model-len 32768`, `--max-lora-rank 8`, gemma4 tool + reasoning parsers | `scripts/p751_start_vllm.sh` (asserted) |

Container setup time is excluded (matches host: clock starts at `start_agent_session`).

## 4. Pass rule

A task is a pass iff Phase-2 style verification succeeds:

1. agent patch applies,
2. pytest on the task's test targets exits 0,
3. at least one test passed (JUnit `passed_tests > 0`, failures=0, errors=0).

Empty patch must fail. Gold patch must pass (soundness gate already enforced on the pool).

Patch apply uses the host 4-pass chain (`scripts/p750_host4pass_apply.py`, from swegemma 0.2.7).

## 5. Statistics

- Per task: mean over the 2 seeds.
- Statistic: mean over tasks of `(arm_b − arm_a)`.
- Interval: percentile bootstrap over tasks, 10_000 resamples (`scripts/p750_paired_stats.py`).
- Report overall and per stratum.

## 6. Gate G1

**Pass:** D69 beats scale10 on calib; 95% CI excludes 0.

**Extension:** if the CI still includes 0 after 150 tasks, run D69 and scale10 on the sealed `test` 150 (+600 episodes) before calling G1 failed. Do not open `test` for candidate ranking.
During any G1 extension on `test`: log **only** the aggregate `(D69 − scale10)` bootstrap CI (no per-task `test` inspection prior to G3). Cache D69's 2-seed `test` results as the baseline for Gate G3.

**Fail:** after extension, D69 does not beat scale10. Stop; hold the current standing. No Phase 2/3.

## 7. Resource caps (operator)

| Cap | Value |
| --- | --- |
| Parent / orchestrator RSS | < 50 MB (no model weights in the parent) |
| Per-worker pytest child peak RSS | ≤ 350 MB |
| Concurrent pytest workers | ≤ 4 (≤ ~600 MB aggregate child RSS) |

## 8. Data rules (C1)

- Phase 1 rollouts that pass two-sided verification are kept as on-policy rows.
- Failures feed DAgger-Recover only at real post-pytest-failure or missed-companion turns.
- No `causal_compiler.py` gold-compiled trajectories in any multi-hundred-step train set.
- Competition-repo mined tasks: 0 rows in `train`.

## 9. Review checklist

- [x] Operator marks this protocol APPROVED in `docs/experiment_log.md`
- [x] Phase 0.1 regrade agree-rate accepted (37/40=0.925; 0 FP; 3/3 remaining disagree = rich_3675)
- [x] Phase 0.2 train pool checkpointed (pass2 may still enrich; calib/test frozen)
- [x] Phase 0.3 virtual-clock selftest PASS (D69 14.0; rank-8 LoRA 13.006)
- [x] Vault verify PASS
- [x] `CLOUD_APPROVAL=YES` for the 900-episode calibration — live since 2026-11-16T13:54:16Z (P7.51f); hard cap **$42.00** Phase 1+2 since ~16:14Z, `NO_SUBMIT=1`

## 10. Five-pod Phase 1 ops (operator DECISIONS 2026-11-16; supersedes the dual-pod plan)

| Knob | Value |
| --- | --- |
| Design | **900 episodes = 3 arms × 2 seeds × 150 calib tasks**; no seed cut |
| Hardware | **5 pods**, one ≥48 GB GPU each (A40 / RTX A6000 / L40S). Pods 0–1: A40 Secure CA-MTL-1 with network volumes; Pods 2–4: no volume |
| Hard spend cap | **$42.00** Phase 1 + Phase 2 combined (Mac daemon `p751_mac_ctl.py`, `HARD_CAP_USD`); fleet terminated before accrued spend can pass it |
| Sharding | Pod *i* runs `calib[i::5]` (30 tasks, 180 episodes) |
| Concurrency | `--workers 2` on every pod (locked) |
| tr20 seeds | seed 0 = ship config `temperature=0.0`; seed 1 = `temperature=0.2`, `top_p=0.95` |
| Episode end | 1 closing turn after `submit_patch`, billed to the 420 s clock; rows log `patch_at_submit` and `final_patch` |
| Order | preflight → Linux soundness on the shard's 30 tasks → 3 smoke episodes (1 per arm) → full `--resume` run |
| Pod watchdog | hard deadline **16 h from original launch**; Phase 1 `DONE.json` does **not** power off the pod (P7.52: deferred self-stop waits for `results/p752_phase2/P752_DONE.json` + 10 min, or `/tmp/ALLOW_POD_SHUTDOWN`) |
| Termination | Mac daemon terminates a pod only when its Phase 2 `P752_DONE.json` and 60/60 Phase 2 rows are synced (or on the spend cap); network volumes `xuac4svj9x` / `qrgb0y4zgf` are never deleted; no API keys on pods |
| Stage 2 provisioning | model from HuggingFace `google/gemma-4-31B-it-qat-w4a16-ct` @ `52f3f65b` (public, weights sha256 verified); venv from the Pod 0/1 freeze; 11 bare repos cloned from GitHub; bundle from the Mac. Nothing is copied from a pod that is running timed episodes |
| Backup | local sync every 5 min to `results/p751_phase1/checkpoints/` |
| `NO_SUBMIT` | **1** (locked) |

## 10b. Phase 2 (P7.52) — zero-idle per-pod handoff

| Knob | Value |
| --- | --- |
| Trigger | Each pod moves on alone when it has 180/180 Phase 1 rows + `DONE.json` **and** the fleet has ≥ 600 Phase 1 rows (≥ 90 complete 6-episode tasks) |
| Winner lock | `scripts/p752_auto_selector.py` writes `results/p752_phase2/P752_WINNER_LOCK.json` once (mode 0444); later 900/900 run writes `P752_WINNER_RECHECK.json` only |
| Grading modes | Mode 1 `working_tree_graded` (Phase 1 verdict); Mode 2 `strict_submitted_only` (requires `submit_patch` before the 420 s cutoff). Winner = max Mode 1; ties → Mode 2 → lower mean virtual seconds |
| Phase 2 plan | Locked winner @ `seed=0` × `{P2_A, P2_B}` × 30 shard tasks = **60 episodes/pod, 300 total** |
| `P2_A` | clock_aware_submit_guard: soft notice at ≥ 330 s; urgent notice at ≥ 375 s with a non-empty working-tree diff |
| `P2_B` | `P2_A` + one-shot pre-submit gate: first `submit_patch` at ≤ 310 s with an edit since the last pytest is intercepted once |
| vLLM | Reuse the warm server Phase 1 left running (port auto-detect: process `--port`, fleet hint, then 18411, then 8000). Weights are never reloaded |
| Gate to push | `scripts/p752_local_dryrun.py` → `results/p752_phase2/local_dryrun/P752_LOCAL_DRYRUN.json` with `ok: true` for the same overlay source hashes; real push refused otherwise |
| Overlay | Additive rsync of Phase 2 scripts + lock (no `--delete`); pod must still match Phase 1 `requires_existing` hashes |


## 11. Launch prerequisites (operator directive 2026-11-16, after the P7.51d abort)

No pod is rented or booted until every item below is done **and reviewed by the operator**.

**Security rule (verbatim):** NEVER copy AWS credentials, RunPod API keys, or `.env` files onto any remote pod or into repo subdirectories. Any sync to a pod must go via `rsync`/`scp` initiated from the local Mac over SSH.
Enforced by: `scripts/p751_build_pod_bundle.py` (secret scan aborts the bundle), pod-side scripts read no credentials, results are pulled from the Mac, the Mac-side monitor terminates pods.

| Item | Artifact | State |
| --- | --- | --- |
| Arm packs from sha256-verified zips only | `scripts/p751_build_arm_packs.py` → `results/p751_phase1/arm_packs/ARM_MANIFEST.json` | done |
| Unified calib file 150/150 | `data/p750_pool/calib_150_tasks.jsonl` | done |
| Runner with real episodes (no stubs) | `scripts/p751_phase1_pod_runner.py` + `p751_host_tools.py` + `p751_grader.py` | done |
| vLLM launcher with hard assertions | `scripts/p751_start_vllm.sh` | done (launch itself untested without a GPU) |
| Pod preflight; runner refuses to start without a passing report | `scripts/p751_preflight_pod.py` | done |
| Local mock dry run on CPU | `scripts/p751_local_dryrun.py` → `results/p751_phase1/local_dryrun/P751_LOCAL_DRYRUN.json` | PASS 53/53 checks |
| Operator review of the open decisions in `docs/experiment_log.md` (P7.51e) | — | **pending** |

Arm facts (from the verified zips): all three share the 7036 B prompt `3693fd62ff40`, 6 tools, budget 240/28/7/80. tr20 and scale10 ship the **same** `adapter_model.safetensors` (sha256-12 `92f4e00d0984`, r=8) and differ in `lora_alpha` (16 vs 8), sampling, and skills.
