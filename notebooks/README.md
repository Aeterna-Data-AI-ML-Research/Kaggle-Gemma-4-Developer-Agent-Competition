# Notebooks

Easy entry points for data scientists and competitors.

| Notebook | Purpose | Kaggle |
| --- | --- | --- |
| [`01_reproduce_tables.ipynb`](01_reproduce_tables.ipynb) | Pin PAPER.md §§4–8 against `evidence/*.jsonl` | [reproduce-gemma4-agent-behavior-study](https://www.kaggle.com/code/moranzavdi/reproduce-gemma4-agent-behavior-study) |
| [`02_explore_calibration.ipynb`](02_explore_calibration.ipynb) | Episode-level EDA (WT, submits, gold-file opens, Think-1024) | [explore-gemma4-agent-calibration](https://www.kaggle.com/code/moranzavdi/explore-gemma4-agent-calibration) |
| [`03_lessons_for_competitors.ipynb`](03_lessons_for_competitors.ipynb) | LB lattice + Think-1024 + timeout localization lessons | [gemma4-agent-lessons-for-competitors](https://www.kaggle.com/code/moranzavdi/gemma4-agent-lessons-for-competitors) |

**Dataset (public):** [moranzavdi/gemma4-agent-behavior-vs-accuracy](https://www.kaggle.com/datasets/moranzavdi/gemma4-agent-behavior-vs-accuracy)

**Related (paper track, already public):**
- Dataset: [moranzavdi/gemma4-soundness-and-punica-bench](https://www.kaggle.com/datasets/moranzavdi/gemma4-soundness-and-punica-bench)
- Notebook: [from-local-validation-to-live-evaluation](https://www.kaggle.com/code/moranzavdi/from-local-validation-to-live-evaluation)

**Competition:** https://www.kaggle.com/competitions/gemma-4-developer-agent  
**Medium:** https://medium.com/@when1go2market

### Local

```bash
pip install -r ../requirements.txt pandas
jupyter notebook 01_reproduce_tables.ipynb
```

Or without Jupyter: `python ../scripts/reproduce_all_tables.py`
