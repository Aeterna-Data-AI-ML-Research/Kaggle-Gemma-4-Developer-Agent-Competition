# Stripped D69-equivalent baseline (reference only)

This directory documents the **declarative four-file shape** of a competition
submission compatible with the Gemma 4 Developer Agent host. It is intentionally
minimal and does **not** include proprietary prompt grafts, adapter weights, or
ForgeSWE wiring.

Host model (not redistributed here): `gemma-4-31b-it-qat-w4a16-ct`.

| File | Role |
| --- | --- |
| `agent.yaml` | Agent name, instruction pointer, toolset list |
| `prompts.yaml` | System / user prompt templates (placeholders) |
| `tools.yaml` | Enabled host tools |
| `sampling.yaml` | Temperature / top_p / thinking budget |

Phase-3 overlay: set `thinking_budget: 1024` in `sampling.yaml` (see
`../think1024_overlay.yaml`).

**Kaggle note:** Companion public dataset —
[moranzavdi/gemma4-agent-behavior-vs-accuracy](https://www.kaggle.com/datasets/moranzavdi/gemma4-agent-behavior-vs-accuracy).
This folder is a **shape reference only** (no proprietary prompts / adapters).
