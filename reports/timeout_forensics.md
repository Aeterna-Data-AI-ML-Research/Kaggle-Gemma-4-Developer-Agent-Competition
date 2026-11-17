# Appendix: clock-timeout forensics

On Phase-1 `tr20` seed 1 (150 calib tasks), 74 failing clock-timeout episodes:

- 52 `timeout_empty_diff`
- 22 `timeout_unsubmitted_with_diff`

Of the 52 empty-diff timeouts, most had already opened a gold file via `read_file`
or a shell command (48/52 in the compact evidence). The median fatal turn began with
~68 virtual seconds remaining and was dominated by reasoning tokens, ending in a
tool call that never executed before the 420 s cutoff.

Median tool wall time on these failures was a fraction of a second — generation
dominated the virtual clock. Reproduce with:

```bash
python scripts/reproduce_all_tables.py
```

(see Section 5/6 output).
