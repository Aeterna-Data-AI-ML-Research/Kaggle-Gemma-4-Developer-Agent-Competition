# P6.95 — Plain-text early-stop audit + D50/E4B-D5 + live A40 8-task verify (≤$0.80)

**UTC:** 2026-11-01 · **Pod:** `7flevwk1a5pxaw` (A40 48GB, EU-SE-1) · **Spend:** **$0.72** (watchdog trigger; hard cap $0.80) · **`live_pods` (ours):** `[]` · **`CLOUD_APPROVAL=NO`**

## Phase 1 (local CPU, $0) — early-stop diagnosis

| Hypothesis | Result |
|---|---|
| Possibility 1: plain-text final turn after `edit_file` (`if not tool_calls: break`) | **FALSE** — `plain_only_after_edit_count=0/24` on P6.92e panel |
| Possibility 2: harness/parser / loops | **TRUE (dominant)** — `repeat_reject` + wall-clock timeouts + false-green `python3 -c` → submit; `rich_3052` D43 had literal `\\n` `edit_file` (harness unescape fixed) |
| L1 `rich_3052` | Confirmed: `__init__` edited; `@classmethod ask` same-file entrypoint missed |
| L1 `fastapi_14479` | `tests/test_invalid_sequence_param.py` already in snap with assertion regex |

**Vaulted:**
- **D50** `d50_no_early_stop_caller_and_pytest_12h_safe_champion.zip` sha12 **`7d336100c312`** Δ=312≤340 · 28/7/think2048 · entrypoint/caller + no-plain-text + mandatory next-turn pytest
- **E4B-D5** `e4b_d5_no_early_stop_caller_and_pytest_champion.zip` sha12 **`d41ca3811eaf`**

## Phase 2 (live A40) — D50 panel8

**Panel (no 20KB ceilings):** httpx_3672, rich_3480, rich_3052, rich_3061, rich_3675, fastapi_14479, fastapi_13920, fastapi_14953.

**Ops blockers burned budget before 8/8 finished:**
1. `/workspace` network volume **20G** < model **22G** → Disk quota; redirected weights to **`/root/models`** (80G overlay).
2. vLLM 0.32 FlashInfer JIT needed `ninja` → fixed with `VLLM_USE_FLASHINFER_SAMPLER=0`.
3. `p677.ensure_snap_cached` required `<REPO_ROOT>` → patched to prefer preseeded `/tmp/p692_snap_cache`.

**Completed before $0.72 kill: 4/8** (killed mid-run: rich_3675, fastapi_14479, fastapi_13920, fastapi_14953).

| task | tool_calls | edit_file | patch | true_sound | note / error |
|---|---:|---:|---:|:---:|---|
| httpx_3672 | 28 | 0 | 0 | ✗ | `tools_disabled:400`; only `run_command`; repeat_reject |
| rich_3480 | 0 | 0 | 0 | ✗ | `tools_disabled:400`; multiline `call:` as assistant_text; vLLM timeout |
| rich_3052 | 0 | 0 | 0 | ✗ | `tools_disabled:400`; 37× assistant_text `call:` (not executed) |
| rich_3061 | 0 | 0 | 0 | ✗ | `tools_disabled:400`; assistant_text only |
| rich_3675 | — | — | — | — | incomplete (watchdog) |
| fastapi_14479 | — | — | — | — | incomplete |
| fastapi_13920 | — | — | — | — | incomplete |
| fastapi_14953 | — | — | — | — | incomplete |

### KPI vs ticket goal

| KPI | Target | Measured |
|---|---|---|
| `ran_post_edit_pytest` | 0% → >75% | **0/4 completed** (no `edit_file` at all) — **FAIL / blocked** |
| TRUE_SOUND | flips | **0/4** |
| Finish 8/8 under $0.72 | yes | **4/8** then terminate |

### New law — `H_TOOLS_DISABLED_400`

When the OpenAI-tools request to vLLM returns **HTTP 400**, the harness sets `note=tools_disabled:400` and stops offering native tools. Gemma then emits **multiline** `call:run_command\ncommand:...` which the P6.92e injector only lifts from **brace** form `call:name{...}`. Net effect: trajectory fills with `assistant_text`, `tool_calls=0`, empty patch — **looks like plain-text stop but root cause is tools API disable**, not the Phase-1 `if not tool_calls` after a successful edit.

## Ladder

- **Design:** D50 ≥ D49 ≥ D45 (vaulted; Gate8 OK).
- **Live:** pytest-loop KPI **not verified**. Do **not** treat D50 as LB-proven over D49 until a tools-400-fixed GPU rerun completes 8/8.
- **E4B:** E4B-D5 vaulted sync of D50; same caveat.
- Ship default remains **D49** until D50 live tools path is green.

## Artifacts

- Phase1: `gemma4-agent/results/p618_clean_frontier/p695_phase1_early_stop_and_d50.json`
- Live: `gemma4-agent/results/p695_live_gpu/checkpoints/d50_panel8.jsonl`
- Summary: `gemma4-agent/results/p695_live_gpu/p695_final_summary.json`
- D33 poller **12840** undisturbed; D33 `57848086` still PENDING at claim time.
