# P6.93 — Live $P_{\mathrm{live}}$ vs $P_{\min}^*$ Autopsy (P6.92e corpus)

**UTC:** 2026-11-01 · **Cloud:** `CLOUD_APPROVAL=NO` · **Pods:** `live_pods: []` (terminated `i67z7ld5h3oss1`) · **Paper:** frozen P6.75 · **G4:** clean

## Ops

| Item | Status |
| --- | --- |
| D36 `57810851` | **COMPLETE**, `publicScore=""` (empty) |
| D33 `57848086` | **PENDING** (autosubmit after D36 empty score) |
| Poller | restarted PID in `gemma4-agent/docs/p687_d36_poller.pid` (CSV watcher) |
| Pod `i67z7ld5h3oss1` | **terminate → 204**, then **404 gone** |

## Stage 1 — Class histogram (24 episodes: pass1e×4 + panel10×20)

| Class | n | Meaning |
| --- | --- | --- |
| **L1_RIGHT_FN_WRONG_COND** | **9** | Touched $P_{\min}^*$ file/fn but wrong/partial condition |
| L2_MISSED_COMPANION | 5 | Subset of $P_{\min}^*$ files |
| L2_WRONG_FILE | 3 | No overlap with $P_{\min}^*$ files |
| L0_NO_PATCH | 3 | Empty `git_diff` |
| L4_OVER_EDIT | 2 | Bloated / multi-site corruption |
| L3_RED_PYTEST_IGNORED | 0 | (almost no in-episode post-edit pytest) |
| PASS | 2 | TRUE_SOUND |

**Dominant fail = L1.** Artifact: `gemma4-agent/results/p618_clean_frontier/p693_live_plive_vs_pmin_autopsy.json`.

## Stage 2 — `httpx_3672` gold-standard 2×2 (local py3.12 regrade)

| Wave | Agent | patch_B | Class | Local TRUE_SOUND |
| --- | --- | --- | --- | --- |
| pass1e | **D43** | **973** | PASS | **True** (24 passed) |
| pass1e | D45 | 2066 | **L4** | False (`SyntaxError` / collection error; also touched `_network.py`) |
| panel10 | D43 | 332 | **L2** | False (only `_server.py`; missing `_parsers.py`) |
| panel10 | **D45** | **741** | PASS | **True** (24 passed) |

Winners edit **both** `src/httpx/_parsers.py` + `src/httpx/_server.py` with ≤2 successful `edit_file`s. Loser L4 grows to 2066B and breaks parse; loser L2 misses the companion parsers hunk.

## Stage 3 — D48 / E4B-D4

Proposed anti-L4/L3 clause blew **Δ=370B > 340B** over D36 (D45 already Δ=335B). Dominant class is **L1**, not cured by that clause under the byte budget.

**Retain:** Slot1 **D45** `bbd403506c83` · Slot2 **E4B-D3 ≥ E4B-D2**. **No D48/E4B-D4 vaulted.**

## Law (MEASURED)

Live 31B $P_{\mathrm{live}}$ failures on the P6.92e panel are dominated by **L1** (right file, wrong condition) and **L2** (missed companion), not invisible-tool loops (fixed in P6.92e). Compact dual-file httpx patches (741–973B) pass; bloat (≥2kB) fails.
