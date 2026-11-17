# P6.78 Overnight Breakthrough Report

**Written:** 2026-10-31T02:20:00Z  
**Guards:** `CLOUD_APPROVAL=NO` · G4 holdout sealed · paper / `swe-horizon-bench` frozen at P6.75 · poller `89384` undisturbed  
**D36 live:** `57810851` PENDING (`P6.68_D36_…`, submitted 2026-10-30 16:11:48Z)

## Executive summary

Local-CPU overnight research (`$0/hr`, `live_pods: []`) completed three stages:

1. **Live pytest repair** — reconstructed agent patches for **61 package-edit fail rollouts ∪ 41 unsolved** (85 work items; 79 with applyable patches) and grafted gold companion hunks under hang-aware timeouts.
2. **Tool-failure replay** — **917** non-holdout traces/metas → **1819** failure events; **120** `edit_file` fails re-checked against unpacked snapshots.
3. **D39 staged** — `d39_empirical_mutation_champion.zip` sha12 `d9276ab01573` on D38 base, **7/7** prompt/config gates, **not submitted** (await D36).

## Stage 1 — Live agent+gold-hunk repair

| Metric | Value |
| --- | ---: |
| Worklist | 85 (`pkg61` keys + remaining unsolved) |
| Completed with patch | 79 |
| `no_agent_patch` | 6 |
| **TRUE_SOUND flips** (`empty_pass=False ∧ repaired_pass=True`) | **8** |
| Unique flipped tasks | 7 |

### Measured FAIL→PASS flips

| Task | Companion relation | Graft | 1B mutation class |
| --- | --- | ---: | --- |
| `fastapi_14266` | `cross_file_reexport_or_caller` | 1 hunk | (see ledger) |
| `fastapi_14487` | `cross_file_reexport_or_caller` | 1 hunk | |
| `rich_3105` | `cross_file_reexport_or_caller` | 1 hunk | |
| `rich_3180` | `cross_file_reexport_or_caller` | 1 hunk | |
| `rich_3934` (×2 traces) | `cross_file_reexport_or_caller` | 2 hunks | |
| `rich_3938` | `same_file_sibling_method` | 2 hunks | `M_EXC_TYPE_OR_MSG` |
| `rich_3944` | `cross_file_reexport_or_caller` | 1 hunk | `M_RETURN_EARLY_OR_MUTATION` |

### Experiment 1B — mutation-class histogram (n=66 classified)

| Class | Count | Ship implication |
| --- | ---: | --- |
| `M_TYPE_UNWRAP` | 22 | After first fail: check `Annotated`/`Union`/`Optional` unwrap |
| `M_IMPORT_OR_EXPORT` | 15 | Companion `__init__` / `__all__` / re-export |
| `M_NONE_OR_EMPTY_GUARD` | 13 | `is None` / empty-collection branch |
| `M_EXC_TYPE_OR_MSG` | 9 | Exact exception class / status code |
| `M_RETURN_EARLY_OR_MUTATION` | 7 | Side-effect before early return |

**Companion-relation law:** **7/8** flips were `cross_file_reexport_or_caller`; **1/8** `same_file_sibling_method`. Highest-yield overnight repair trigger = one-call compound `sed -n` read of caller/export companion, then single graft edit.

Artifacts: `gemma4-agent/results/p618_clean_frontier/p678_stage1_live_patch_repair_ledger.json` · checkpoints `<REPO_ROOT>/kaggle/p678_overnight/checkpoints/stage1_progress.jsonl`.

## Stage 2 — Tool-failure replay (expanded corpus)

| Kind | Count |
| --- | ---: |
| Files scanned | **917** (local harvest; paper's 1237 MS rollouts include remote/BoN shards not all on disk) |
| Events | **1819** |
| `edit_file` fails | 745 |
| `run_command` ≥4900 truncation | 190 |
| `python3 -c` inline | 884 |

### Edit-fail classes (observation taxonomy)

`old_string_not_found` dominant in obs text; refined by **snapshot replay** (n=120):

| Snap-replay reason | Count |
| --- | ---: |
| `old_string_absent_from_snap` | 57 |
| `old_string_present_obs_stale_or_tool_bug` | 27 |
| `multi_occurrence_needs_allow_multiple` | 16 |
| `filepath_not_in_snap` | 14 |
| `hallucinated_or_truncated_span` | 6 |

**Call-waste estimate:** ≥745 wasted gated calls from edit fails + ≥190 from truncations hiding pytest footers → forces blind re-runs (`python3 -c` inflation = 884).

Artifact: `p678_stage2_tool_failure_replay.json`.

## Stage 3 — D39 `d39_empirical_mutation_champion.zip`

| Field | Value |
| --- | --- |
| Base | `d38_horizon_compound_champion.zip` (D36 knobs: think=2048, calls=40, timeout=240, wall=8m, out=8192, temp=0.2) |
| Delta | §**3d Empirical mutation repair** — companion caller/export via `sed -n`, exception/`None`/`Annotated` completeness, `allow_multiple` / indent re-read after edit miss |
| SHA-256 | `d9276ab0157386267bf7a1ab2e2fdca38076e4c2292d570733f357c4943dbc3f` |
| SHA12 | `d9276ab01573` |
| Gates | **7/7** (0 forbidden strings; 40-call / 8-minute aligned) |
| Submit | **NO** — await `57810851` terminal |

Vault: `gemma4-agent/proprietary_vault/zips/d39_empirical_mutation_champion.zip` (mode 444) · agent mirror `proprietary_vault/agents/D39_empirical_mutation_champion/`.

## Decision matrix (unchanged route)

| D36 public score | Action |
| --- | --- |
| ≥ 0.24 | HOLD finals floor; D39 offline only |
| 0.18 ≤ score < 0.24 | Operator pick among D39 / D38 / D37 (G3 single-axis) |
| < 0.18 or ERROR | Poller autosubmits D33; queue D39 offline |

## Ops notes (hang safety)

- Worktrees: `/tmp/p678_worktrees` (symlink at `<REPO_ROOT>/kaggle/p678_overnight/worktrees`); hardlink clones + `break_hardlink` before writes (APFS `cp -cR` was ~60s/tree and corrupted shared inodes).
- Checkpoints / logs on pics; AppleDouble stripped; `patch` ≤10s intent, pytest wall 25s.
- Poller `89384` never restarted.

## Paper Track

`docs/paper-draft-nov12.md`, `paper_resource_dataset/`, `swe-horizon-bench/` **untouched** (frozen at P6.75).
