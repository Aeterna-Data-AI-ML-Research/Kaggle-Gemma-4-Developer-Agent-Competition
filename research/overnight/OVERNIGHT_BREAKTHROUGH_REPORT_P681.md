# P6.81 Overnight Breakthrough Report

**Written:** 2026-10-31T08:38:20Z  
**Guards:** CLOUD_APPROVAL=NO · G4 · paper frozen · poller 89384 undisturbed · resume+memory monitor

## Stage 1 — Intra-task winner vs loser
- Sometimes-solved: **30** (metas≈778, traces≈1324)
- Divergence kinds: `{"no_tool_divergence_or_empty_seq": 168}`
- Live splice flips: **51**

## Stage 2 — ddmin on 25 stubborn
- Summary: `{"n_done": 25, "mean_pmin_hunks": 8.32, "graft_flip_tasks": 1, "pmin_pass_n": 22}`
- Pytest cumulative: **0**

## Stage 3 — Policy matrix + D42
- Matrix: `{"D33": {"mean_score": 0.3988, "n": 85}, "D36": {"mean_score": 0.4488, "n": 85}, "D40": {"mean_score": 0.8145, "n": 85}, "D41": {"mean_score": 0.8871, "n": 85}, "D42": {"mean_score": 0.9624, "n": 85}}`
- D42 sha12 **c96559cd93b3** · Δ **341B** ≤350 · gates **8/8**

## Artifacts
- `gemma4-agent/results/p618_clean_frontier/p681_stage1_intratask_winner_vs_loser_divergence.json`
- `gemma4-agent/results/p618_clean_frontier/p681_stage2_ddmin_irreducible_patches.json`
- `gemma4-agent/results/p618_clean_frontier/p681_stage3_85task_policy_sim_and_d42.json`
- `docs/MASTER_REALISTIC_FINDINGS_LEDGER.md`
- vault `d42_ddmin_intratask_stabilized_champion.zip`
