# ForgeSWE 0.24 Roadmap — P7.31-GM-Complete (W1–W18)

**Status:** Local CPU Phases 0→1→2→V + **P7.31-local-cpu-4fixes**. `NO_SUBMIT=1` · `CLOUD_APPROVAL=NO` · `G4=0` · prompt **7036B** D69 locked · `G19=PASS` · `NO_SOUPS=1`.

## GPU Stage-A order (when `CLOUD_APPROVAL=YES`)

1. **Bench pre-minted full-depth 600-key scale twins first (zero new train cost):**
   - `*_scale10_a8` (600 keys, served scale 1.0) — prefer `d98_v2_scale075_a6` / `d100_forgeswe_v3_scale10_a8` (Phase I **15/22 = 68.2%**)
   - `*_scale075_a6` (600 keys, scale 0.75)
   - `tr20_scale10_a8` / `tr20_scale15_a12` / `d100_forgeswe_v3_scale15_a12` (α=12 probe; ship Gate2 still scale≤1.0)
   - **RETIRED — do not mount/ship:** `*_L30_59_scale10_a8` (300 keys), `*_L30_59_mlp_only_scale10_a8` (180 keys) — measured collapse **68.2% → 50.0%–54.5%**; broke `rich_3676` (0 edits) / `rich_2943` (39 edits).
2. On **22-pair** contrastive: `pick_anchor` ranks by **`(win_pct, code_edit_margin, tier2_6_margin)`** + **first-token** `P(EOS)<0.005` ∧ `P(tool_call_open)<0.01` (not `P(<|thought|>)` — chat template already opens thought) + **N=8** prefix-cached fork (`RUN_GPU_FORK=1`).
3. **Then** 6-step v4 focal train (action-only SFT + thought+edit GapDPO, `focal_token_weight=4.0`, init from best 600-key scale twin).
4. Panel Soft-28 / Hard-34 6T with **hard worktree reset** (`git reset --hard HEAD && git clean -fdx` + fresh `PYTHONPATH` pre/post episode); unlock `NO_SUBMIT=0` iff `best9 >= 6`.
5. Optional E4B←31B distill @ scale 1.0.

## W1–W18 matrix

| ID | Assert | Encoding |
| --- | --- | --- |
| W1 | 6T single agent; library-only edits; DiffGuard `PYTHONPATH=src:.`; no graph tools / sub-agents | `p727_package` TOOLS; v4 filters; SCAFFOLD_FREEZE agent/ not ship source |
| W2 | 7036B lock; Soft-28/Hard-34; unlock≥6/9; no teacher-brevity | `eval_config_34calls_7m.yaml`; prompt byte lock |
| W3 | behavioral dedup; y_win TRUE_SOUND | GapDPO `(task_id,action_hash)` unique |
| W4 | G4=0; no decision-turn-only LoRA; no early submit in y_win; wrong_fix forks non-holdout | Tier2 firewall; eval-only fork fixtures |
| W5 | no collapsed-emb tools; median first-edit ≤10 | v4 SFT builder |
| W6 | pytest **or** python3-c; no D49/D62b | DiffGuard forks / hygiene |
| W7 | scale1.0/0.75 **600-key** twins; no OPD; scale≤1.0 ship law; **ban post-hoc 300/180 strip** | Phase 0 mint + Gate2 `{600}` |
| W8 | detectors pass; 7m clock; EOS stub = `P_EOS`+`P_tool_call_open` | `p731_forgeswe_adapter_detectors.py` |
| W9 | action-only SFT; thought+edit GapDPO; **600-key only** (strip retired) | v4 datasets + twins |
| W10 | delimiter hygiene; fork-replay (str|dict y_lose) | detectors + `p731_fork_replay_screen.py` |
| W11 | single-agent only; sibling/read recency (w/ W17) | package 6T; read-recency detector |
| W12–W14 | bans / no multi-agent | documented here; W13 no `/tmp` write |
| W13 | no `/tmp` or scratch `write_file` in y_win | detector + builder |
| W15 | L1/L2 companion forks in GapDPO | operators in v4 GapDPO |
| W16 | focal 4.0x; `max_output_tokens==6144` | v4 + `configs/sampling.yaml` |
| W17 | sliding_window_1024 read recency ≥85% | detector |
| W18 | no vLLM hang delimiter patterns in y_win | detector |

## Clean-room IP (3 assertions)

1. `ip_clean_room_audit == PASS` — twins only from local `d100_s6` / `d98_v2` / `tr20`; jsonls from local ForgeSWE corpora.
2. `edit_in_window_pct == 100%` — `est_tokens<=8192`, `n_unmasked_supervised_tokens>=25`.
3. `valid_6t_tool_names_only` — supervised / y_win tools ⊆ 6T.

## Production wiring (ship / GPU)

| Path | Wire |
| --- | --- |
| `scripts/p727_package_forgeswe_zip.py` | Soft-28/Hard-34 `eval_config` + Gate2 **600-only** + scale≤1.0 + post-pack `assert_zip_production_contract` + P7.31 detectors |
| `scripts/safe_stage_submission_zip.py` | G19 + `RUN_P731_DETECTORS=1` zip audit (dry-run too) |
| `scripts/p730_stage2_gm_gpu_remote.py` | Soft-28/Hard-34 panel eval_config |
| `scripts/p730_stage2_phase1_train.py` | `FORGESWE_TRAIN_GEN=v4` → v4 jsonl + focal sample_weight + INIT best 600-key scale twin + `SERVED_ALPHA=8` |
| `scripts/p731_phase1_twins_and_v4_train.py` | `pick_anchor` = `(win_pct, code_edit_margin, tier2_6_margin)` on 600-key only |
| `scripts/rejection_sample.py` | `P731_HARD_RESET_WORKTREE` pre/post episode |
| `scripts/p731_stage_a_production.py` | dry-packs 600-key ship-law twins under `CLOUD=NO` |

## Artifacts

- Twins: `gemma4-agent/ckpts/d100_*scale*`, `d98_v2_*scale*`, `tr20_scale*` (600-key). Historical `*_L30_59*` left on disk but **banned** from pick_anchor / Gate2 / SHIP_TWINS.
- Autopsy: `gemma4-agent/results/p731_stage1_cpu/P731_STAGE1_REPORT.{md,json}` · GPU Phase I `results/p731_gpu_clean_2phase/`
- Datasets: `data_train/forgeswe_v4_sft_action_only_7036b.jsonl`, `forgeswe_v4_gapdpo_thought_and_edit_7036b.jsonl`
- Coverage: `results/p731_w1_w10_coverage_report.json` → `ALL_W1_TO_W18_CHECKS_PASS`
- Stage-A dry zips: `results/p731_stage1_cpu/stage_a_production/dry_zips/`

## Explicit bans

Prompt grafts; 9T/graph tools in **ship** zips; SequentialAgent; Soft announce-32; Hard-40/8m; scale 2.0 ship; OPD; teacher-brevity; soups; Tier-2 in `data_train/`; `/tmp` write_file supervision; D49/D62b; 2k–3k synth inflation; external competitor IP; **post-hoc L30_59 / mlp_only stripping on 600-key checkpoints**.
