# P6.97b — Host-parity gemma4 parser + D33/D52/D53 panel10 (E4B skipped)

**Status:** DONE (31B arms only). E4B-D7/D8 **not run** (operator stop).  
**Pod:** `n75vhug8gthcta` L40S OC-AU-1 @ $1.09/hr → **terminated**; `live_pods: []`; `CLOUD_APPROVAL=NO`.  
**Spend:** ~**$1.83** (~1.68 h; target ≤$2.10).  
**vLLM:** `--enable-auto-tool-choice --tool-call-parser gemma4 --reasoning-parser gemma4`.  
**Artifacts:** `gemma4-agent/results/p697b_live_gpu/` · `p697b_cpu_autopsy_timeout_regression.json` · `tournament_summary_no_e4b.json`.

## Panel10 scoreboard (TRUE_SOUND)

| Arm | TRUE | IDs | Edits>0 | in_ep pytest | mean wall | extrap 120 | tools400 | repeat_reject Σ |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **D33** | **1/10** | rich_3675 | **4**/10 | 0/10 | 210.6s | 7.02h | 0 | 657 |
| **D52** | **1/10** | rich_3675 | **4**/10 | 1/10 | 320.8s | 10.69h | 0 | 1390 |
| **D53** | **2/10** | rich_3675, **requests_7205** | **10**/10 | **8**/10 | **167.0s** | **5.57h** | 0 | 339 |

**vs P6.96 D33:** was **2/10** (rich_3675+requests_7205), **Edits>0=8/10**. P6.97b D33 regressed to 1/10 and 4/10 edits under the same panel + gemma4 parsers.

**Ship ladder unchanged for LB:** still ship **D49**; panel reference remains **D51 (2/10 @4.68h P6.96)** ≥ D53 (2/10 @5.57h this run, different parser stack) ≥ D33. D53 is the **in-run** winner and cures the P6.97a `no_in_episode_pytest` residual (8/10).

Vault: D52 `2e8f7f164f6b` · D53 `66b32874fb1b` (Gate8 Δ≤340).

## Timeout regression autopsy (requests_7205 / rich_3480 / rich_3061)

### (a) Did `--reasoning-parser gemma4` ignore `thinking_budget` and emit ~8k thought tokens/turn?

**REJECTED by proxy (reasoning_content not persisted in jsonl).**

Evidence:

1. Harness `chat_completion` clamps `max_tokens = min(sampling.max_output_tokens, 2048)` — client cannot request 8k completions even though agent `sampling.yaml` lists `max_output_tokens: 8192` / `thinking_budget: 4096`. `thinking_budget` is **loaded but never sent** in the OpenAI payload.
2. No `reasoning` / `reasoning_content` / `usage` fields appear in any episode jsonl.
3. On D33/D52 timeout tasks, **sec / approx_LLM_turn ≈ 1.7–3.5 s** across **140–280** turns (rejects + successful calls). That is incompatible with multi-thousand thought tokens per turn on L40S; successful tasks show similar sec/turn (~2–4 s).

### (b) Tool calls before 480s timeout

| Task | Arm | sec | successful `tool_calls` | `repeat_reject` | patch |
| --- | --- | ---: | ---: | ---: | ---: |
| requests_7205 | D33 | 481 | 10 | **197** | 0 |
| requests_7205 | D52 | 481 | 10 | **207** | 0 |
| rich_3480 | D33 | 483 | 13 | **267** | 0 |
| rich_3480 | D52 | 483 | 12 | **126** | 0 |
| rich_3061 | D33 | 482 | 18 | **145** | 0 |
| rich_3061 | D52 | 481 | 12 | **134** | 0 |

P6.96 D33 same tasks: requests_7205 **TRUE** in **57s / 14 calls / 0 rejects**; rich_3061 patch>0 in 76s / 0 rejects.

**Dominant mechanism:** under native gemma4 structured `tool_calls` (`injected_structured_tool_calls=0` on these timeouts vs heavy inject in P6.96), the model enters **identical-command loops**. Harness `repeat_reject` returns a STOP message but does **not** consume useful edit progress; wall clock burns to 480s with **patch=0**.

### (c) D53 `verifier_critic_agent` rescues (10 tasks)

| Class | Count | Tasks |
| --- | ---: | --- |
| critic started | **9**/10 | all except rich_3052 (hit 480s in coder) |
| **true_after_critic_work** | **1** | **requests_7205** (handoff patch=426; post_edits=3; post_submit=1; TRUE) |
| true_likely_coder_verified_by_critic | **1** | rich_3675 (handoff already 676; critic pytest×5) |
| patch_improved_not_true | **4** | httpx_3672, rich_3061, fastapi_14479, fastapi_14455 |
| critic_no_material_change | **3** | rich_3480, fastapi_13920, fastapi_14953 |
| no_critic | **1** | rich_3052 |

**Net:** Sequential critic **rescued 1 TRUE** (`requests_7205`, which D33/D52 timed out at patch=0) and **improved patches on 4 more** without TRUE_SOUND. Critic also drove **in_ep pytest 8/10** (vs 0–1 on D33/D52).

## Operator decisions locked

- E4B-D7/D8 on this pod: **SKIPPED**.
- Pod terminated immediately after D53 10/10 sync.
- D33 poller **12840** / submission `57848086` undisturbed.

## Next (no cloud)

1. Harden harness against gemma4 structured repeat storms (stronger than current 3-identical reject; escalate to force `read_file`/`edit_file`).
2. Log `reasoning_content` length + `usage` per turn if a future parser ablation is needed.
3. Treat **D53** as panel co-contender with D51 for residual-pytest; ship default remains **D49** until LB.
