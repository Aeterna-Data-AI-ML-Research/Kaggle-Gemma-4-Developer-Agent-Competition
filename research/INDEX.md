# Docs index (shared memory)

`docs/` holds **cross-track institutional memory** only.  
The two Kaggle competitions live at repo root under [`../competitions/`](../competitions/).

```text
.
├── competitions/
│   ├── agent/     ← gemma-4-developer-agent (ADK / LB)
│   └── paper/     ← gemma-4-developer-agent-paper
├── docs/          ← you are here (G0 memory)
│   ├── INDEX.md
│   ├── PROPRIETARY_PLAYBOOK.md
│   ├── experiment_log.md
│   └── MASTER_REALISTIC_FINDINGS_LEDGER.md
├── gemma4-agent/  ← code, vault, results, train data
└── AGENTS.md
```

Old paths under `docs/*.md` / `docs/agent-competition/` / `docs/paper-competition/` are **redirect stubs**.

---

## Boot every session (paths frozen here)

| Doc | Role |
| --- | --- |
| [`PROPRIETARY_PLAYBOOK.md`](./PROPRIETARY_PLAYBOOK.md) | Authoritative memory + Hard Graveyard + ship ladder |
| [`experiment_log.md`](./experiment_log.md) | Claims / dones / gates / `CLOUD_APPROVAL` |
| [`MASTER_REALISTIC_FINDINGS_LEDGER.md`](./MASTER_REALISTIC_FINDINGS_LEDGER.md) | Named empirical laws |
| [`../AGENTS.md`](../AGENTS.md) | G0–G18 |
| [`../gemma4-agent/proprietary_vault/`](../gemma4-agent/proprietary_vault/) | Immutable zips + laws JSON |

```bash
python3 gemma4-agent/scripts/verify_vault_and_memory.py
```

---

## Competitions (not under docs/)

| Track | Entry |
| --- | --- |
| Agent LB | [`../competitions/agent/README.md`](../competitions/agent/README.md) |
| Paper | [`../competitions/paper/README.md`](../competitions/paper/README.md) |
| Both | [`../competitions/README.md`](../competitions/README.md) |

### Agent — quick links

- [`implementation-roadmap.md`](../competitions/agent/implementation-roadmap.md)
- [`agent-dev-spec.md`](../competitions/agent/agent-dev-spec.md)
- [`competition-roadmap.md`](../competitions/agent/competition-roadmap.md)
- [`cloud-ops.md`](../competitions/agent/cloud-ops.md)
- Ops: [`../competitions/agent/ops-docs/`](../competitions/agent/ops-docs/) (`harness_verify.md`, etc.)

### Paper — quick links

- Notebook: [`../competitions/paper/notebooks/swe_horizon_bench_paper_reproduction.ipynb`](../competitions/paper/notebooks/swe_horizon_bench_paper_reproduction.ipynb)
- [`paper-outline-nov12.md`](../competitions/paper/paper-outline-nov12.md) · [`paper-draft-nov12.md`](../competitions/paper/paper-draft-nov12.md)
- [`figures/`](../competitions/paper/figures/) · [`resource-dataset/`](../competitions/paper/resource-dataset/)

---

## Reading order

**LB session:** `AGENTS.md` → playbook → experiment_log tail → vault verify → one phase card in `competitions/agent/implementation-roadmap.md`.

**Paper session:** `competitions/paper/README.md` → notebook → outline → draft.
