# P6.96 — `.pth` poison purge + clean regrade + D51 + 3-arm GPU leap

**UTC:** 2026-11-01 · **Pod:** `lvcax991widd3j` (A40 48GB, EU-SE-1, $0.59/hr) · **Spend:** **~$1.62** (watchdog $7.50 / hard $8.00) · **`live_pods` (ours):** `[]` · **`CLOUD_APPROVAL=NO`**

## Stage 1 (local CPU, $0) — P677APFS / `.venv` contamination

P6.93 autopsy tails showed `rich/prompt.py` under `<REPO_ROOT>/worktrees/p677_agent_c4lf6a7v` and `rich.console.input` / `flasgger` warnings during FastAPI regrades.

| Finding | Result |
|---|---|
| Live `.pth` editable hooks → P677APFS | **Not present now** in `.venv_p677_py312` (only setuptools `distutils-precedence.pth`) |
| Regrade isolation | Enforced `PYTHONPATH=<wt>/src:<wt>` + `PYTHONNOUSERSITE=1` + named-file pytest (never bare) |
| Clean regrade of 24 P6.92e `git_diff`s | **2 TRUE_SOUND** (same httpx winners as P6.93); **0 flips**; **0 P677 path hits** |
| `flasgger` WARNING | Cosmetic under scoped pytest (still appears in some tails) |

**Law `H_PTH_WORKTREE_SHADOW`:** even without live `.pth` poison, always pin worktree-first `PYTHONPATH` + refuse bare `pytest`.

## Stage 2 (local CPU) — harness + D51

- `run_command` env: `PYTHONPATH=<wt>/src:<wt>`, `PYTHONNOUSERSITE=1`
- Tools-400 cure: never permanently disable tools; omit schema + parse multiline `call:name\nkey: val`
- **D51** `d51_think4096_clean_pytest_28calls_champion.zip` sha12 **`44276b648aef`** · think **4096** · 28 calls · 8 min · Δ=312≤340
- **E4B-D6** `e83e35f34610` (same ablation on E4B track)

## Stage 3 (live A40) — preflight + 3-arm + E4B

### Preflight (mandatory)

| Check | Result |
|---|---|
| A — `import rich.prompt` from `/tmp` worktree | **PASS** |
| B — `httpx_3672` D50 | **PASS** — `true_sound=1`, `edit_file=5`, `patch=741`, `tools_schema_omitted:400` soft (multiline fallback executed; **no hard disable**) |

### 31B panel10 (`workers=2`)

| Arm | TRUE_SOUND | true_ids | ran_pytest | mean_s | 120-task h | patch>0 |
|---|---:|---|---:|---:|---:|---:|
| **D33** | **2/10** | rich_3675, requests_7205 | 8 | 241.4 | 8.05 | 8 |
| **D50** | **1/10** | requests_7205 | 4 | 197.6 | 6.59 | 4 |
| **D51** | **2/10** | httpx_3672, requests_7205 | 7 | **140.3** | **4.68** | 7 |

**Panel winner:** **D51** (ties D33 on TRUE_SOUND; fastest 12h-safe envelope).  
**Ship default until LB proof:** still **D49** (D33 `57848086` PENDING; no new LB score from this panel).

### E4B panel10

Competition QAT **not on S3** → used public HF `google/gemma-4-E4B-it` (same proxy as P6.87).

| Arm | TRUE_SOUND | patch>0 | mean_s | 120-task h |
|---|---:|---:|---:|---:|
| E4B-D5 | 0/10 | 3 | 284.2 | 9.47 |
| E4B-D6 | 0/10 | 1 | 407.1 | 13.57 |

Retain **E4B-D4** as ship; E4B-D5/D6 vaulted but not promoted on this public-proxy panel.

### Ops fixes burned into playbook

1. vLLM **0.11.0** fails Gemma4 `rope_scaling` → pin **`vllm==0.32.0`** + `VLLM_USE_FLASHINFER_SAMPLER=0`
2. Model weights on **`/root/models`** (80G overlay), not 20G `/workspace` volume
3. `resolve_python`: prefer `/workspace/venv/bin/python` (symlink argv0 breaks site-packages)

## Ladder (post P6.96)

- **Slot1 design:** D51 ≥ D33(panel) ≥ D50 ≥ D49 ≥ D45 …  
- **Slot1 ship:** **D49** until D33 LB returns / D51 submitted  
- **Slot2:** E4B-D4 ≥ E4B-D5 ≥ E4B-D6 (panel 0/10 public HF)

## Artifacts

- Combined: `gemma4-agent/results/p618_clean_frontier/p696_clean_pth_regrade_and_3arm_tournament.json`
- Stage1: `.../p696_stage1_pth_purge_and_clean_regrade.json`
- Live: `gemma4-agent/results/p696_live_gpu/tournament_summary.json` + `checkpoints/*.jsonl`
- D33 poller **12840** undisturbed; D33 `57848086` still **PENDING**
