# Contributing

This repository is an evidence release for ML / DS researchers.

## Before opening a PR

1. `pip install -r requirements.txt`
2. `python scripts/reproduce_all_tables.py` must print `ALL_PAPER_TABLES_REPRODUCED = True`
3. Do not add secrets, SSH endpoints, raw trajectory dumps, or adapter weights
4. Prefer extending analysis scripts that read `evidence/*.jsonl` only

## Adding analyses

New notebooks or scripts should load compact evidence via the schema in
`evidence/SCHEMA.md`. If you need fields that are missing, open an issue describing
the scientific need — we may expand the compact schema in a future release.
