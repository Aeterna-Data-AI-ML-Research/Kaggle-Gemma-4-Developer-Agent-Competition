# Lessons for Gemma 4 Developer Agent competitors

**Author:** Moran Zavdi · Apache-2.0  
**Competition:** https://www.kaggle.com/competitions/gemma-4-developer-agent  
**Evidence:** https://www.kaggle.com/datasets/moranzavdi/gemma4-agent-behavior-vs-accuracy

These are the highest-signal takeaways from a 1,350-episode calibration campaign.
They are meant to save other teams GPU time and false-positive “wins.”

## 1. Process gains ≠ accuracy gains

Reducing `thinking_budget` 4096→1024 nearly eliminated long thoughts and raised
submit rate, but working-tree (WT) accuracy stayed **48/150 = 48/150**
(paired flips +9/−9). Always report task-level WT with paired bootstrap CIs.

## 2. Public LB is a coarse lattice

Assuming ~58 public tasks and two-decimal truncation, one extra solve moves the
displayed score by ~0.017. See `lb_lattice.csv`. Offline ~31% WT does **not**
map 1:1 onto the public lattice.

## 3. Localization is often already done before timeouts

Most empty-diff clock kills had already opened a gold file. Failures were late
edits and long reasoning bursts under a 420s virtual clock—not “never found the file.”

## 4. Strict submit ≠ working-tree pass

An agent can leave a passing tree without calling `submit_patch` (or the reverse).
Use WT as the primary offline metric; treat submit ceremony separately.

## 5. Train only when you have volume and a selector

On-policy SFT rows collapsed from hundreds of raw passes to ~90 usable unique
rows—far below a 1,000+ distillation target. pass@6 oracle ≈ 44% WT shows
stochastic headroom without a deployable selection mechanism under the host budget.

## 6. What to reproduce first

```bash
pip install -r requirements.txt
python scripts/reproduce_all_tables.py
```

Or open the Kaggle notebooks linked in the dataset / GitHub README.
