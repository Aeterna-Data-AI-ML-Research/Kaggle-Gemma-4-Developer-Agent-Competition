# P7.09 Task Research Matrix (85 local non-holdout tasks)

Tier counts: `{'T1_sometimes_solved': 19, 'T2a_keeper_harvested': 3, 'T2b_never_but_reachable': 26, 'T3_deep_multi_hunk': 12, 'T0b_solved_rate_unknown': 15, 'T0_reliable': 10}`

| task | tier | topo | hunks | pass/rollouts | rate | failure code | embed@3 | P7.06 | next lever |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: | --- | --- |
| `fastapi_14459` | T1_sometimes_solved | S3 | 8 | 4/7 | 0.57 | PASS_or_ever_solved | 0.44 |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `fastapi_9425` | T1_sometimes_solved | S1 |  | 4/7 | 0.57 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `rich_3470` | T1_sometimes_solved | S1 |  | 4/7 | 0.57 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `fastapi_13537` | T1_sometimes_solved | S1 |  | 26/49 | 0.53 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `rich_3518` | T1_sometimes_solved | S1 |  | 10/19 | 0.53 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `requests_6644` | T1_sometimes_solved | S1 |  | 8/17 | 0.47 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `httpx_3672` | T1_sometimes_solved | S3 | 18 | 6/14 | 0.43 | PASS_or_ever_solved | 0.36 |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `fastapi_14455` | T1_sometimes_solved | S2 | 2 | 2/5 | 0.40 | PASS_or_ever_solved | 1.00 |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `fastapi_15589` | T1_sometimes_solved | S1 |  | 2/5 | 0.40 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `fastapi_14303` | T1_sometimes_solved | S1 |  | 6/16 | 0.38 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `fastapi_14360` | T1_sometimes_solved | S1 |  | 6/16 | 0.38 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `fastapi_14419` | T1_sometimes_solved | S3 | 7 | 6/28 | 0.21 | PASS_or_ever_solved | 0.71 |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `fastapi_13207` | T1_sometimes_solved | S2 | 2 | 8/38 | 0.21 | PASS_or_ever_solved | 1.00 |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `rich_4075` | T1_sometimes_solved | S2 | 4 | 5/27 | 0.18 | PASS_or_ever_solved | 0.26 |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `requests_7505` | T1_sometimes_solved | S3 | 6 | 5/39 | 0.13 | PASS_or_ever_solved | 0.50 |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `fastapi_15280` | T1_sometimes_solved | S3 | 2 | 2/20 | 0.10 | PASS_or_ever_solved | 0.46 |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `requests_7205` | T1_sometimes_solved | S1 |  | 4/46 | 0.09 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `fastapi_11194` | T1_sometimes_solved | S1 |  | 5/60 | 0.08 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `rich_4077` | T1_sometimes_solved | S1 |  | 2/28 | 0.07 | PASS_or_ever_solved |  |  | self-distill own winners (STaR/RFT) to raise Pass@1 |
| `rich_3480` | T2a_keeper_harvested | S2 | 2 | /0 |  | EMPTY_RECONSTRUCTED_PATCH | 0.00 | BoN n01 KEEP pc=1766 (TRUE_SOUND after scratch strip) | add keeper to SFT; re-measure Pass@k after retrain |
| `fastapi_14479` | T2a_keeper_harvested | S1 |  | /4 |  | W2b_off_by_one_or_regex_or_format_mismatch |  | warm n01 TRUE_SOUND pc=525 (KEEP) | add keeper to SFT; re-measure Pass@k after retrain |
| `fastapi_14492` | T2a_keeper_harvested | S1 |  | /8 |  | N1_never_localized_gold_file |  | BoN resolved (TRUE_SOUND flag unset) | add keeper to SFT; re-measure Pass@k after retrain |
| `fastapi_13920` | T2b_never_but_reachable | S2 | 2 | /28 |  | N2_localized_never_edited_gold | 0.00 | BoN n01 pc=1496 FAIL; n02 timeout | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_14266` | T2b_never_but_reachable | S2 | 2 | /22 |  | N3_edited_gold_in_rollouts_but_all_failed | 0.00 |  (oracle seed) | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3535` | T2b_never_but_reachable | S3 | 2 | /4 |  | W2b_off_by_one_or_regex_or_format_mismatch | 1.00 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3938` | T2b_never_but_reachable | S3 | 2 | /4 |  | N3_edited_gold_in_rollouts_but_all_failed | 0.00 |  (oracle seed) | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_11355` | T2b_never_but_reachable | S2 | 3 | /43 |  | W2a_incomplete_type_or_branch_coverage_in_same_fn | 0.74 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_14448` | T2b_never_but_reachable | S3 | 3 | /14 |  | W2a_incomplete_type_or_branch_coverage_in_same_fn | 1.00 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_14512` | T2b_never_but_reachable | S2 | 3 | /4 |  | N3_edited_gold_in_rollouts_but_all_failed | 1.00 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_14953` | T2b_never_but_reachable | S3 | 3 | /8 |  | W2a_incomplete_type_or_branch_coverage_in_same_fn | 1.00 | BoN 2x pc=560 FAIL; warm r14 pc=1616 ModuleNotFound | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3934` | T2b_never_but_reachable | S3 | 3 | /27 |  | N3_edited_gold_in_rollouts_but_all_failed | 0.61 |  (oracle seed) | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_14986` | T2b_never_but_reachable | S3 | 4 | /4 |  | W2a_incomplete_type_or_branch_coverage_in_same_fn | 0.61 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3180` | T2b_never_but_reachable | S3 | 4 | /4 |  | N3_edited_gold_in_rollouts_but_all_failed | 1.00 |  (oracle seed) | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3468` | T2b_never_but_reachable | S2 | 4 | /12 |  | N3_edited_gold_in_rollouts_but_all_failed | 0.40 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_14482` | T2b_never_but_reachable | S2 | 5 | /4 |  | N1_never_localized_gold_file | 1.00 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3675` | T2b_never_but_reachable | S3 | 5 | /0 |  | E3_missing_gold_file | 0.74 | BoN 2x FAIL (timeout pc=0; wrong TTY pc=452) | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_14962` | T2b_never_but_reachable | S3 | 6 | /4 |  | N3_edited_gold_in_rollouts_but_all_failed | 0.00 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3772` | T2b_never_but_reachable | S2 | 6 | /7 |  | N3_edited_gold_in_rollouts_but_all_failed | 0.43 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3942` | T2b_never_but_reachable | S3 | 6 | /4 |  | W2a_incomplete_type_or_branch_coverage_in_same_fn | 0.57 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3052` | T2b_never_but_reachable | S2 | 8 | /4 |  | N3_edited_gold_in_rollouts_but_all_failed | 0.83 |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_14246` | T2b_never_but_reachable | S1 |  | /4 |  | UNSOUND_NATIVE_ENV_SKIP_OR_EMPTY_PASS |  |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_14487` | T2b_never_but_reachable | S1 |  | /4 |  | N1_never_localized_gold_file |  |  (oracle seed) | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_15661` | T2b_never_but_reachable | S1 |  | /4 |  | W2a_incomplete_type_or_branch_coverage_in_same_fn |  |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_15763` | T2b_never_but_reachable | S1 |  | /0 |  | TRUE_ZERO_TRACE |  |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3105` | T2b_never_but_reachable | S1 |  | /12 |  | N1_never_localized_gold_file |  |  (oracle seed) | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3521` | T2b_never_but_reachable | S1 |  | /4 |  | W2b_off_by_one_or_regex_or_format_mismatch |  | BoN done, no keep | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_3944` | T2b_never_but_reachable | S1 |  | /0 |  | W1_or_wrong_file |  |  (oracle seed) | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `rich_4076` | T2b_never_but_reachable | S1 |  | /8 |  | N1_never_localized_gold_file |  |  | oracle-guided trajectory synthesis + BoN n>=8 on adapter |
| `fastapi_14099` | T3_deep_multi_hunk | S3 | 9 | /4 |  | N3_edited_gold_in_rollouts_but_all_failed | 0.66 |  | park; only via oracle-trajectory SFT after T1/T2 done |
| `fastapi_14306` | T3_deep_multi_hunk | S3 | 11 | /4 |  | W2a_incomplete_type_or_branch_coverage_in_same_fn | 0.10 |  | park; only via oracle-trajectory SFT after T1/T2 done |
| `fastapi_13786` | T3_deep_multi_hunk | S3 | 12 | /0 |  | W2a_incomplete_type_or_branch_coverage_in_same_fn | 0.49 |  | park; only via oracle-trajectory SFT after T1/T2 done |
| `rich_3486` | T3_deep_multi_hunk | S3 | 12 | /0 |  | W2a_or_runtime_exc | 0.28 |  | park; only via oracle-trajectory SFT after T1/T2 done |
| `fastapi_15800` | T3_deep_multi_hunk | S3 | 13 | /0 |  | W1_wrong_span_same_file | 0.01 |  | park; only via oracle-trajectory SFT after T1/T2 done |
| `rich_3061` | T3_deep_multi_hunk | S2 | 13 | /11 |  | W2a_incomplete_type_or_branch_coverage_in_same_fn | 0.43 |  | park; only via oracle-trajectory SFT after T1/T2 done |
| `fastapi_15030` | T3_deep_multi_hunk | S3 | 15 | /4 |  | N3_edited_gold_in_rollouts_but_all_failed | 0.05 |  | park; only via oracle-trajectory SFT after T1/T2 done |
| `fastapi_14605` | T3_deep_multi_hunk | S3 | 16 | /4 |  | N3_edited_gold_in_rollouts_but_all_failed | 0.02 |  | park; only via oracle-trajectory SFT after T1/T2 done |
| `rich_3930` | T3_deep_multi_hunk | S3 | 27 | /0 |  | E_import_or_incomplete_symbol | 0.44 |  | park; only via oracle-trajectory SFT after T1/T2 done |
| `fastapi_14262` | T3_deep_multi_hunk | S3 | 29 | /47 |  | W2c_missing_kwarg_forwarding_or_state_mutation | 0.21 | BoN s2 pc=2411 FAIL (Literal import miss) | park; only via oracle-trajectory SFT after T1/T2 done |
| `fastapi_14186` | T3_deep_multi_hunk | S3 | 51 | /45 |  | W2a_incomplete_type_or_branch_coverage_in_same_fn | 0.27 | STaR/warm n02-n04 no flip (may_v1 residual) | park; only via oracle-trajectory SFT after T1/T2 done |
| `fastapi_14609` | T3_deep_multi_hunk | S3 | 65 | /0 |  | UNSOUND_NATIVE_ENV_SKIP_OR_EMPTY_PASS | 0.12 |  | park; only via oracle-trajectory SFT after T1/T2 done |
| `fastapi_14616` | T0b_solved_rate_unknown | S2 | 2 | /0 |  | PASS_TRUE_SOUND_SOLVE | 0.39 |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `fastapi_14794` | T0b_solved_rate_unknown | S2 | 2 | /42 |  | PASS_or_ever_solved | 0.00 |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `fastapi_14372` | T0b_solved_rate_unknown | S3 | 3 | /42 |  | PASS_or_ever_solved | 0.70 |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `fastapi_14458` | T0b_solved_rate_unknown | S2 | 4 | /10 |  | PASS_or_ever_solved | 0.48 |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `fastapi_14356` | T0b_solved_rate_unknown | S1 |  | /6 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `fastapi_14786` | T0b_solved_rate_unknown | S1 |  | /42 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `fastapi_9555` | T0b_solved_rate_unknown | S1 |  | /8 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `requests_6589` | T0b_solved_rate_unknown | S1 |  | /6 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `requests_6592` | T0b_solved_rate_unknown | S1 |  | /8 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `requests_6629` | T0b_solved_rate_unknown | S1 |  | /6 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `rich_3006` | T0b_solved_rate_unknown | S1 |  | /28 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `rich_3067` | T0b_solved_rate_unknown | S1 |  | /29 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `rich_3882` | T0b_solved_rate_unknown | S1 |  | /30 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `rich_3894` | T0b_solved_rate_unknown | S1 |  | /28 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `rich_3905` | T0b_solved_rate_unknown | S1 |  | /34 |  | PASS_or_ever_solved |  |  | measure Pass@1 (n>=4) before deciding T0 vs T1 |
| `fastapi_14873` | T0_reliable | S2 | 2 | 8/8 | 1.00 | PASS_or_ever_solved | 0.00 |  | keep: regression guard only |
| `rich_3676` | T0_reliable | S3 | 8 | 6/6 | 1.00 | PASS_or_ever_solved | 0.67 |  | keep: regression guard only |
| `fastapi_14349` | T0_reliable | S1 |  | 6/6 | 1.00 | PASS_or_ever_solved |  |  | keep: regression guard only |
| `rich_2725` | T0_reliable | S1 |  | 8/8 | 1.00 | PASS_or_ever_solved |  |  | keep: regression guard only |
| `fastapi_9753` | T0_reliable | S2 | 2 | 10/11 | 0.91 | PASS_or_ever_solved | 1.00 |  | keep: regression guard only |
| `requests_7315` | T0_reliable | S1 |  | 8/9 | 0.89 | PASS_or_ever_solved |  |  | keep: regression guard only |
| `rich_2943` | T0_reliable | S1 |  | 14/16 | 0.88 | PASS_or_ever_solved |  |  | keep: regression guard only |
| `fastapi_5624` | T0_reliable | S1 |  | 8/10 | 0.80 | PASS_or_ever_solved |  |  | keep: regression guard only |
| `requests_7427` | T0_reliable | S1 |  | 6/8 | 0.75 | PASS_or_ever_solved |  |  | keep: regression guard only |
| `fastapi_14301` | T0_reliable | S1 |  | 16/24 | 0.67 | PASS_or_ever_solved |  |  | keep: regression guard only |
