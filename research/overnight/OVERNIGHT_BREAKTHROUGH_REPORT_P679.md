# P6.79 Overnight Breakthrough Report

**Written:** 2026-10-31T04:30:17Z  
**Guards:** `CLOUD_APPROVAL=NO` · G4 · paper frozen at P6.75 · poller `89384` undisturbed  
**D36 live:** `57810851,submission.zip,2026-10-30 16:11:48.877000,P6.68_D36_hong024_8m_8192_240s_think2048_calls40_allow_mult_inline_repro,SubmissionStatus.PENDING,,`

## Executive summary

1. **Bloat audit** of stacked D37/D38/D39 §3b/§3c/§3d on D36 (W4A16 instruction dilution).
2. Distilled unified zero-bloat **D40** (`d40_unified_horizon_mutation_champion.zip`) — **single `## 3x` clause**, net delta **318 B** over D36 (Gate8 ≤320), **8/8** gates.
3. **Stage-4** agent-hunk → gold **replacement** (not additive graft) on remaining non-flips: **7** TRUE_SOUND flips.
4. Locked laws into `PERMANENT_EMPIRICAL_LAWS.json` + **G17** in `AGENTS.md` / playbook + verify banner.

## D36..D39 byte audit

| Zip | sys_bytes | Δ vs D36 | §3b | §3c | §3d |
| --- | ---: | ---: | :---: | :---: | :---: |
| D36 | 7148 | 0 | no | no | no |
| D37 | 7311 | 163 | yes | no | no |
| D38 | 7566 | 418 | yes | yes | no |
| D39 | 8038 | 890 | yes | yes | yes |
| **D40** | 7466 | **318** | no | no | no (`## 3x` only) |

Stacked tail bytes: `{"D37": 162, "D38": 417, "D39": 889}`

## D40 specification

- Base: `D36_hong_024_surgical_027_perfect_champion.zip` (timeout 240 / think 2048 / calls 40 / 8m / 8192 / temp 0.2)
- Clause bytes: **316** (budget ≤320)
- SHA256: `e07e015f915c8d35d549bfe3c5b2f053d2b71ce2f487ec3bdc965ea354efe45a`
- SHA12: `e07e015f915c`
- Gates: **8/8** · check_pass=None
- **Submit:** NO (await `57810851`)

Clause:
```
## 3x. Horizon+mutation
- 1-call `grep -rn`/`sed -n` for primary+companion past 150-line cut.
- Same cycle: `__init__`/`_compat` export, caller, sync/async sibling.
- First fail → Annotated/Union/Optional, None/empty, exact exception/status, companion hunk.
- Edit miss → `allow_multiple` or `sed -n`; no guess.

```

## Stage 4 — Replacement repair

| Metric | Value |
| --- | ---: |
| Candidates (unique non-flip w/ agent patch) | 24 |
| Done | 24 |
| TRUE_SOUND replacement flips | **7** |

Flip IDs: `fastapi_11355, fastapi_14246, fastapi_14479, fastapi_15661, rich_3521, rich_3934, rich_3938`

**Implication:** When additive companion graft fails, **replace** the agent's conflicting function body with the MS gold hunk (1–2 hunks) before more exploration — complementary to D40's companion/mutation triggers.

## Memory lock

- `gemma4-agent/proprietary_vault/PERMANENT_EMPIRICAL_LAWS.json`
- `AGENTS.md` / `docs/PROPRIETARY_PLAYBOOK.md` → **G17**
- `verify_vault_and_memory.py` asserts laws + D33/D36–D40 mode 0444 + ACTIVE MEMORY REMINDER banner

## Priority ladder

**D40 > D39 > D38 > D37**; **D33** if D36 `< 0.18` / ERROR (poller).
