# P6.94 — D36 Empty Score · False-Green Pytest · D49 / E4B-D4

**UTC:** 2026-11-01 · **Cloud:** `CLOUD_APPROVAL=NO` · **Pods:** `live_pods: []` · **Paper:** frozen P6.75 · **G4:** clean · **Poller:** PID **12840** (D33 `57848086`) undisturbed

## Ops

| Item | Status |
| --- | --- |
| D36 `57810851` | **COMPLETE**, `publicScore=""` (empty — not a numeric zero) |
| D33 `57848086` | **PENDING** (still) |
| Poller | `12840` CSV watcher alive |
| Cloud | NO / $0.00 |

## Stage 1 — Why D36 returned empty + why `ran_post_edit_pytest == 0/24`

### Finding A — D36 empty score = 12h / runner, not schema

| Agent | calls | minutes | think | out | Live result |
| --- | ---: | ---: | ---: | ---: | --- |
| **D36** | **40** | **8** | 2048 | 8192 | COMPLETE **empty** |
| D45–D47 family | 40 | 8 | 2048 | 8192 | (same unsafe envelope) |
| D33 | 28 | 8 | 4096 | 8192 | PENDING |
| P6.14 `57628655` | 28 | 8 | 4096 | 8192 | **0.17** |
| P6.11 `57538500` | 28 | 7 | 4096 | 6144 | **0.18** |

- `agent.yaml` keys identical D36↔D33↔D45; only numeric envelope + prompt bytes differ → **not** a YAML validation reject.
- Worst-case wall: **120 tasks × 8 min = 16.0 h > 12 h**. Public writeups (Hitarth) treat **40–100 calls** as a finish-risk; scored Hong/budget-fit packs use **28 calls**.
- **Law:** never treat D36’s **40-call / 8-min** as an unverified safe default for D40–D47/D45.

Artifact: `gemma4-agent/results/p618_clean_frontier/p694_d36_empty_and_l1_exact_diffs.json`.

### Finding B — `H_FALSE_GREEN_INLINE_REPRO` (MEASURED)

Across all **24** P6.92e live 31B episodes:

| Metric | Value |
| --- | ---: |
| `ran_post_edit_pytest` | **0 / 24** |
| ran `python3 -c` after last ok edit | 7 |
| false-green (pyc OK → submit, no pytest) | **6** |

Examples: `rich_3480` / `rich_3061` run toy `python3 -c "from rich.text import Text; …"` then `git status && git diff` → `submit_patch`, never `pytest tests/…` where `test_append_loop_regression` / `test_extend_style` live. Prompt root: D36/D45 Verify bullet *“Always also run one `python3 -c`…”* + 3x Miss packing `python3 -c` with pytest.

### Exact L1/L2 diffs

Printed unified `git_diff` ($P_{\mathrm{live}}$) vs $P_{\min}^*$ for focus tasks (`rich_3480/3052/3061`, `fastapi_14479/13920/14099/14262/14455`) into the Stage1 JSON (`git_diff_full` / `pmin_diff_full` + line-set compare). Dominant residual remains **L1** (right file, wrong condition) and skipped real pytest.

Edit-call preserve under 28-call cap: **16/18** last-ok edits ≤28 (88.9%); outliers `httpx_3672`/D43 last=37 (already TRUE) and `fastapi_14262`/D45 last=39 (FAIL).

## Stage 2 — Public notebooks

| Source | Takeaway |
| --- | --- |
| `ryanholbrook/…small-model-leaderboard` | Small-model prize LB: **444** teams; top **0.10** (4 teams); we absent. Organizer CSV in kernel output. |
| `hitarthjain0/…0-12-0-24` | **12h wall** is binding; thinking must stay on; 28/8/240 is the 0.18→0.24 recipe; graph tools unused. |
| `hitarthjain0/…apex-silver…0-24` | Explicitly warns **40–100 tool calls** fail to finish; one focused `pytest -k` after edit. |

Artifact: `gemma4-agent/results/p618_clean_frontier/p694_stage2_public_notebook_scan.json` (notebooks under `external_notebooks/p694_scan/`, untracked).

## Stage 3 — D49 + E4B-D4 vaulted

| Zip | sha12 | Δ vs D36 | Envelope | Prompt fix |
| --- | --- | ---: | --- | --- |
| `d49_pytest_closed_loop_12h_safe_champion.zip` | **`4d40e3dc4f49`** | **327** ≤340 | **28 / 7 min / 2048 / 240** | Mandatory post-edit named-file pytest; `python3 -c` alone = false-green |
| `e4b_d4_pytest_closed_loop_champion.zip` | **`0dc160d87ad5`** | **327** ≤340 | same + `gemma-4-e4b-it-qat-w4a16-ct` | same |

Gates **8/8**. Mode **0444**. **Not submitted** (await D33; daily quota).

**Ladder now:** Slot1 **D49 ≥ D45 ≥ D43 ≥ …**; Slot2 **E4B-D4 ≥ E4B-D3 ≥ E4B-D2**.

## Law (MEASURED)

1. **D36 empty score ⇒ 40-call/8-min is not 12h-safe.** Prefer ≤28 calls and ≤7–8 min (P6.11/P6.14/Hong public packs).
2. **`python3 -c` without named-file pytest after edit is false-green** (0/24 real pytest on P6.92e panel). D49 forces pytest → traceback repair → then submit.
