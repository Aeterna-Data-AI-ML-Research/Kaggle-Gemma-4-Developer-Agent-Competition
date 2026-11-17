# P6.97a — MDP residual analysis + ADK / swegemma architecture audit

**UTC:** 2026-11-01 · **Spend:** **$0.00** · **`CLOUD_APPROVAL=NO`** · **`live_pods: []`** · G4 holdout excluded · Paper frozen at P6.75

**Ops:** D33 `57848086` still **PENDING**; poller **12840** alive (~5h47m). Undisturbed.

Artifact: [`gemma4-agent/results/p618_clean_frontier/p697a_mdp_residual_and_adk_audit.json`](../gemma4-agent/results/p618_clean_frontier/p697a_mdp_residual_and_adk_audit.json)  
Script: [`gemma4-agent/scripts/p697a_mdp_residual_and_adk_loader_audit.py`](../gemma4-agent/scripts/p697a_mdp_residual_and_adk_loader_audit.py)

---

## Stage 0 — Live submission / poller

| Item | Status |
|---|---|
| `57848086` (D33) | `SubmissionStatus.PENDING` (kaggle `--csv`) |
| Poller `12840` | Alive (`bash` 180s loop → `p687_d36_poller.log`) |
| Cloud | **NO** — local CPU only |

---

## Stage 1 — 30-episode MDP residual (D33 / D50 / D51)

### 1.1 Episode matrix + early-stop (D51 140.3s vs D33 241.4s)

| Arm | mean wall_s | hit_28_cap | submit_early | repeat_reject | plain_text | TRUE_SOUND |
|---|---:|---:|---:|---:|---:|---:|
| **D33** | **241.4** | 3 | 4 | 3 | 0 | 2/10 |
| **D50** | 197.6 | 6 | 1 | 3 | 0 | 1/10 |
| **D51** | **140.3** | **7** | **1** | 2 | **0** | 2/10 |

**Verdict:** D51’s compute underutilization is **not** early `submit_patch` (1/10), **not** plain-text stop (0), **not** wall timeout (0). It is **28-call-cap exhaustion on 7/10** with short per-call wall under ubiquitous `tools_schema_omitted:400` soft-omit. D33 spends more wall on fewer capped episodes and more early submits (4/10).

### 1.2 Pre-edit information state $I_{\text{pre}}$ (D33 & D51)

| Cohort | mean lines pre-edit | % read test pre | % red repro pre | mean call@1st edit |
|---|---:|---:|---:|---:|
| D33 winners (rich_3675, requests_7205) | **164.5** | 0% | 0% | 9.5 |
| D33 fails (7 focus) | 88.7 | 0% | 14% | 11.0 |
| D51 winners (httpx_3672, requests_7205) | **206.5** | 0% | **50%** | 16.0 |
| D51 fails (7 focus) | 86.0 | 0% | 14% | 12.8 |

**Almost never** read `tests/test_*.py` before first edit (0% across winners+fails). Winners read ~2× more source lines before editing.

#### Pairwise: `rich_3675` / `httpx_3672`

| Task | Arm | true | wall_s | 1st edit | lines_pre | patch_chars | stop |
|---|---|---|---:|---:|---:|---:|---|
| rich_3675 | **D33** | **PASS** | 231 | 8 | 102 (`rich/console.py`) | 422 | hit_28 |
| rich_3675 | D51 | FAIL | 52 | **none** | **0** | **0** | hit_28 (empty patch) |
| httpx_3672 | D33 | FAIL | 487 | 19 | (edits failed / repeat_reject) | 0 | repeat_reject |
| httpx_3672 | **D51** | **PASS** | 241 | later | high $I_{\text{pre}}$ | >0 | hit_28 |

D51 loses `rich_3675` by **never editing** (28 fast no-op / browse calls). D33 loses `httpx_3672` by late failed edits + `repeat_reject`.

### 1.3 Post-edit verification $I_{\text{post}}$ (V1 / V2 / V3)

Ticket’s **8/10 (D33)** and **7/10 (D51)** “ran pytest” = **harness post-episode agent pytest**, not in-episode.

| Layer | D33 | D51 |
|---|---|---|
| Post-episode agent pytest | **8/10** | **7/10** |
| In-episode `pytest` | 2/10 | 4/10 |
| Failed + in-episode buckets | 7× no_pytest, 1× V2 | 5× no_pytest, 1× V1, 1× V2, 1× V3 |

**Failed D33+D51 in-episode buckets (n=16 fails):**

| Bucket | Count | Meaning |
|---|---:|---|
| **`no_in_episode_pytest`** | **12** | **DOMINANT residual** — stop/submit without named-file pytest |
| `V2_red_traceback_seen_failed_repair` | 2 | Saw red; did not repair (D33 `rich_3052`, D51 `fastapi_14479`) |
| `V1_false_green_unpatched_suite` | 1 | D51 `fastapi_14455`: green on **wrong** file `tests/test_openapi_schema_type.py` |
| `V3_pre_edit_only_pytest` | 1 | D51 `rich_3061`: green on `tests/test_text.py` (89 passed) @call18, **re-edited @25 without re-pytest** |

**Post-episode:** 11/16 failed graded episodes are `post_V2_red_agent_suite` — the harness sees reds the agent never consumed mid-episode.

Exact in-episode examples (tails truncated in JSON artifact):

- **V1** `D51/fastapi_14455`: `pytest tests/test_openapi_schema_type.py` → exit 0 (4 passed) after earlier red on the correct security-scheme test.
- **V2** `D51/fastapi_14479`: `pytest tests/test_tutorial/test_query_params` → exit 1 (starlette error) — unrepaired.
- **V3→mutate** `D51/rich_3061`: `pytest tests/test_text.py` → 89 passed, then further `edit_file` with no final verify.
- **V2-ish** `D33/rich_3052`: `python3 -c '… import pytest'` → `ModuleNotFoundError: pytest` (not a real suite run).

`P_live` vs $P_{\min}^*$ heads for all failed D33/D51 episodes are in the artifact (`P_live_vs_P_min_failed_D33_D51`).

---

## Stage 2 — `swegemma` / `adk_submission` / `google.adk` audit

**Note:** Ticket named `.venv_p677_py312` — that venv has **no** `swegemma` / `adk_submission`. Competition pins live in **`gemma4-agent/.venv_bootstrap` (py3.14)** → audited there.

### 2.1 Declarative multi-agent topologies — **YES**

`adk_submission.schema` union + `compiler.py` support:

| `agent_class` | YAML keys (abbrev.) |
|---|---|
| `LlmAgent` | `model`, `instruction`, `tools`, `skills`, `sub_agents`, `generate_content_config`, `output_key` |
| **`SequentialAgent`** | **`sub_agents`**, name, description, callbacks |
| **`LoopAgent`** | **`sub_agents`**, **`max_iterations`** |
| `ParallelAgent` | `sub_agents` |

**Answer:** A valid `submission.zip` **can** declare:

```yaml
agent_class: SequentialAgent
name: swe_pipeline
sub_agents:
  - config_path: sub_agents/coder_agent.yaml
  - config_path: sub_agents/verifier_critic_agent.yaml
```

where `verifier_critic_agent` is an `LlmAgent` with tools to inspect `git diff`, run discriminative pytest, and repair L1 bugs on the **remaining** shared call/time budget. Caveat: harness budgets are shared — allocate call/time split explicitly.

### 2.2 Official vLLM tool flags (eliminate `tools_schema_omitted:400`)

`adk_submission.server.VllmServer.build_cmd` (defaults `enable_auto_tool_choice=True`, `tool_call_parser="hermes"`; docs list **`gemma4`**):

```text
--enable-auto-tool-choice
--tool-call-parser hermes   # or gemma4 for host parity
# recommended Gemma 4:
--tool-call-parser gemma4
--reasoning-parser gemma4
```

**Why P6.96 got HTTP 400:** local harness started `vllm serve` with only model/host/port/len/seqs/prefix-cache — **without** `--enable-auto-tool-choice` / `--tool-call-parser`. Passing `tools=[...]` then 400s; soft-omit + multiline `call:` parse recovered tools but left every episode tagged `tools_schema_omitted:400`.

**P6.97b must** start vLLM via `VllmServer` (or identical flags) for **0% tools-400**.

---

## Dominant residual → P6.97b design target

1. **Primary:** `no_in_episode_pytest` (12/16 failed D33+D51) — agents do not verify before stop.
2. **Secondary:** false-green / wrong-file green + mutate-without-reverify (V1/V3); red unrepaired (V2).
3. **Infrastructure:** host-parity vLLM tool parser (`gemma4`) to stop soft-omit distortion of the MDP.
4. **Architecture unlocked:** `SequentialAgent` coder → verifier_critic (or `LoopAgent` repair) is **first-class** in the competition loader.

**Ship default unchanged:** D49. Panel winner remains D51 pending D33 LB. No GPU until P6.97b ticket + live `CLOUD_APPROVAL=YES`.
