# Notebooks

Easy entry points for data scientists and humans.

| Notebook | Purpose | Kaggle |
| --- | --- | --- |
| [`01_reproduce_tables.ipynb`](01_reproduce_tables.ipynb) | Pin PAPER.md §§4–8 against `evidence/*.jsonl` | [reproduce-gemma4-agent-behavior-study](https://www.kaggle.com/code/moranzavdi/reproduce-gemma4-agent-behavior-study) |
| [`02_explore_calibration.ipynb`](02_explore_calibration.ipynb) | Episode-level EDA (WT, submits, gold-file opens, Think-1024) | [explore-gemma4-agent-calibration](https://www.kaggle.com/code/moranzavdi/explore-gemma4-agent-calibration) |

**Dataset (public):** [moranzavdi/gemma4-agent-behavior-vs-accuracy](https://www.kaggle.com/datasets/moranzavdi/gemma4-agent-behavior-vs-accuracy)

**Related (paper track, already public):**
- Dataset: [moranzavdi/gemma4-soundness-and-punica-bench](https://www.kaggle.com/datasets/moranzavdi/gemma4-soundness-and-punica-bench)
- Notebook: [from-local-validation-to-live-evaluation](https://www.kaggle.com/code/moranzavdi/from-local-validation-to-live-evaluation)

**Competition:** https://www.kaggle.com/competitions/gemma-4-developer-agent

### Local

```bash
pip install -r ../requirements.txt pandas
jupyter notebook 01_reproduce_tables.ipynb
```

Or without Jupyter: `python ../scripts/reproduce_all_tables.py`
