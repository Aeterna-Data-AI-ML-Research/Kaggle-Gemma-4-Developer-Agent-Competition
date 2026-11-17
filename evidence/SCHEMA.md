# Evidence schema

All claim reproduction uses these JSONL files only (never private raw traces).

| File | Rows | Description |
| --- | ---: | --- |
| `phase1_calibration_900.jsonl` | 900 | Three arms × 2 seeds × 150 calib tasks |
| `phase2_guards_300.jsonl` | 300 | Submit-guard harness arms P2_A / P2_B on calib |
| `phase3_thinkcap_150.jsonl` | 150 | Thinking-budget 1024 vs Phase-1 tr20 seed-1 baseline |
| `manifest.sha256` | — | SHA-256 digests of the evidence + benchmark files |

## Episode object

| Field | Type | Notes |
| --- | --- | --- |
| `phase` | string | `phase1` / `phase2` / `phase3` |
| `task_id` | string | e.g. `fastapi_16418` |
| `arm` | string | `d69` / `tr20` / `scale10` |
| `harness_arm` | string \| null | Phase 2: `P2_A` or `P2_B` |
| `seed` | int | |
| `stratum` | string | `competition_public` / `competition_new` / `other` |
| `pass` | bool | Working-tree (WT) grader pass |
| `strict_pass` | bool | WT pass **and** `submit_patch` recorded |
| `end_reason` | string | e.g. `time_budget`, `submitted`, `tool_budget` |
| `failure_mode` | string \| null | |
| `virtual_seconds` | float | Virtual clock at episode end (cutoff 420 s) |
| `tool_s` | float | Sum of tool wall seconds |
| `gen_tokens` | int | |
| `tool_calls` | int | |
| `thinking_budget` | int \| null | Token cap for reasoning (4096 default; 1024 in phase3) |
| `temperature` | float \| null | |
| `r_gen` | float \| null | Charged generation rate (tok/s) for virtual clock |
| `patch_chars` | int | |
| `patch_sha12` | string \| null | SHA-256 prefix of final patch text |
| `patch_submitted` | bool | |
| `n_gold_files` | int | |
| `turn_summary` | list | Dense turn tuples (below) |
| `first_edit_turn` | int \| null | 0-based tool-trace turn of first successful edit |
| `first_edit_virtual_sec` | float \| null | |
| `opened_gold_file_read` | bool | `read_file` hit a gold path |
| `opened_gold_file_shell` | bool | `run_command` args mentioned a gold path |
| `opened_all_gold_files` | bool | Every gold path seen via read or shell args |
| `fatal_turn_remaining_sec` | float \| null | Seconds left when last turn started (time_budget ends) |
| `fatal_turn_reasoning_tokens` | int \| null | Estimated reasoning tokens on fatal turn |
| `thoughts_gt_1024` | bool | Any turn with estimated reasoning tokens &gt; 1024 |

## `turn_summary` dense tuple

Each element is:

```text
[turn_idx, virtual_sec_start, virtual_sec_end, reasoning_tokens, content_tokens,
 tool_name, target_is_gold_file, exit_code]
```

- `target_is_gold_file`: `1` / `0`
- `exit_code`: `0` ok, `1` failed tool, or `null` if no tool on that turn
- Reasoning tokens estimated as `min(completion_tokens, reasoning_chars / 4.197)`

Helper in `scripts/reproduce_all_tables.py`:

```python
def expand_turn(t):
    return {
        "turn_idx": t[0], "virtual_sec_start": t[1], "virtual_sec_end": t[2],
        "reasoning_tokens": t[3], "content_tokens": t[4], "tool_name": t[5],
        "target_is_gold_file": bool(t[6]), "exit_code": t[7],
    }
```

Raw tool argument text, reasoning strings, and `git_diff` blobs are **not** shipped.
