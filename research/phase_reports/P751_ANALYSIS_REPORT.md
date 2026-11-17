# P7.51 Phase 1 analysis — final (2026-11-16T23:27:37Z)

Rows 900/900 · tasks with all 6 episodes 150/150 · rows per pod {'pod0': 180, 'pod1': 180, 'pod2': 180, 'pod3': 180, 'pod4': 180}

Only complete tasks are scored. `working_tree_graded` is the Phase 1 verdict; `strict_submitted_only` also requires that `submit_patch` was called.

| config | arm | seeds | temp | episodes | working_tree_graded | strict_submitted_only | pass only via working tree | mean virtual s | time_budget unsubmitted |
|---|---|---|---|---|---|---|---|---|---|
| d69 | d69 | [0, 1] | [0.2] | 300 | 93/300 = 0.3100 | 58/300 = 0.1933 | 35 | 399.516 | 180 |
| tr20_s0 | tr20 | [0] | [0.0] | 150 | 47/150 = 0.3133 | 27/150 = 0.1800 | 20 | 402.028 | 87 |
| tr20_s1 | tr20 | [1] | [0.2] | 150 | 48/150 = 0.3200 | 22/150 = 0.1467 | 26 | 405.272 | 85 |
| scale10 | scale10 | [0, 1] | [0.2] | 300 | 91/300 = 0.3033 | 47/300 = 0.1567 | 44 | 411.964 | 188 |
| tr20_pooled (report only) | tr20 | [0, 1] | [0.0, 0.2] | 300 | 95/300 = 0.3167 | 49/300 = 0.1633 | 46 | 403.65 | 172 |

pass@6 oracle (any of the 6 rollouts): working_tree_graded 66/150 = 0.4400 · strict_submitted_only 49/150 = 0.3267

## Paired comparisons (b minus a, bootstrap over tasks)

### working_tree_graded

| a | b | rate a | rate b | delta | 95% CI | CI excludes 0 |
|---|---|---|---|---|---|---|
| d69 | tr20_s0 | 0.31 | 0.3133 | +0.0033 | [-0.04, 0.0467] | False |
| d69 | tr20_s1 | 0.31 | 0.32 | +0.0100 | [-0.0467, 0.0667] | False |
| d69 | tr20_pooled | 0.31 | 0.3167 | +0.0067 | [-0.0333, 0.0467] | False |
| d69 | scale10 | 0.31 | 0.3033 | -0.0067 | [-0.0467, 0.0333] | False |
| tr20_s0 | tr20_s1 | 0.3133 | 0.32 | +0.0067 | [-0.0533, 0.0667] | False |
| tr20_s0 | scale10 | 0.3133 | 0.3033 | -0.0100 | [-0.0533, 0.0333] | False |
| tr20_s1 | scale10 | 0.32 | 0.3033 | -0.0167 | [-0.07, 0.0367] | False |
| tr20_pooled | scale10 | 0.3167 | 0.3033 | -0.0133 | [-0.05, 0.0233] | False |

### strict_submitted_only

| a | b | rate a | rate b | delta | 95% CI | CI excludes 0 |
|---|---|---|---|---|---|---|
| d69 | tr20_s0 | 0.1933 | 0.18 | -0.0133 | [-0.0667, 0.0433] | False |
| d69 | tr20_s1 | 0.1933 | 0.1467 | -0.0467 | [-0.11, 0.0167] | False |
| d69 | tr20_pooled | 0.1933 | 0.1633 | -0.0300 | [-0.08, 0.02] | False |
| d69 | scale10 | 0.1933 | 0.1567 | -0.0367 | [-0.08, 0.0033] | False |
| tr20_s0 | tr20_s1 | 0.18 | 0.1467 | -0.0333 | [-0.0933, 0.0267] | False |
| tr20_s0 | scale10 | 0.18 | 0.1567 | -0.0233 | [-0.0733, 0.0267] | False |
| tr20_s1 | scale10 | 0.1467 | 0.1567 | +0.0100 | [-0.0467, 0.0633] | False |
| tr20_pooled | scale10 | 0.1633 | 0.1567 | -0.0067 | [-0.0467, 0.0367] | False |

## Winner lock

`WINNER_ARM = tr20` · `WINNER_TEMP = 0.2` · config `tr20_s1` · sha12 `89e6ae70fd36` · locked 2026-11-16T22:33:20Z at stage `interim` (857 rows, 140 complete tasks) · tie-break used: none · lock sha12 `7473149739a9`

Recheck on this run: recomputed winner `tr20_s1` — agrees with the lock (the lock is never changed after it is written).

## Failure buckets on `tr20_s1` (this run's winner)

113 bucketed episodes of 150 (102 failed; an unsubmitted time-budget end is bucketed even when its working tree passed).

| bucket | n | share | end reasons | examples |
|---|---|---|---|---|
| timeout_unsubmitted_with_diff | 33 | 0.2920 | {'time_budget': 33} | flask_5917/s1, pydantic_7803/s1, pytest_12854/s1, starlette_2815/s1, attrs_1200/s1 |
| timeout_empty_diff | 52 | 0.4602 | {'time_budget': 52} | attrs_1165/s1, click_3764/s1, fastapi_10773/s1, fastapi_13827/s1, fastapi_14482/s1 |
| submitted_untested_regression | 3 | 0.0265 | {'submitted': 3} | rich_3675/s1, starlette_3489/s1, fastapi_16418/s1 |
| submitted_after_failed_test | 1 | 0.0088 | {'submitted': 1} | fastapi_14986/s1 |
| other_logic_or_localization_fail | 24 | 0.2124 | {'submitted': 8, 'tool_budget': 16} | click_3031/s1, fastapi_15908/s1, pydantic_11941/s1, pytest_14015/s1, rich_3938/s1 |

- Unsubmitted time-budget ends with a diff whose working tree passed: 11
- Episodes whose only edits went through `run_command` (invisible to the edit-tool rule): 3
- Coverage of complete tasks by repo: {'attrs': 14, 'click': 14, 'fastapi': 36, 'flask': 8, 'httpx': 11, 'pydantic': 14, 'pytest': 14, 'rich': 10, 'starlette': 14, 'urllib3': 14, 'requests': 1} (planned {'attrs': 14, 'click': 14, 'fastapi': 36, 'flask': 8, 'httpx': 11, 'pydantic': 14, 'pytest': 14, 'rich': 10, 'starlette': 14, 'urllib3': 14, 'requests': 1})

