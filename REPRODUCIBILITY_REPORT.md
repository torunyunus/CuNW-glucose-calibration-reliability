# Reproducibility reconciliation — V35 (pending full repository validation)

## Status and provenance

The previous report documented **an older, pre-chronology-correction run**. Its metrics and unresolved 36–37 s clock discrepancy must **not** be interpreted as evidence validating V34 manuscript results. The experimental group subsequently clarified nominal additions at 100, 150, 200, 250, 300, 350, 400, 450 and 500 s; detected transitions are 111, 165, 213, 263, 319, 365, 411, 462 and 514 s (operational delays 11–19 s).

This branch updates the segmented ground truth in `scripts/06_simulations.py` to:

```python
def seg(x):
    x = np.asarray(x, float)
    return 18.392512639957 + 0.236805055829*x - 0.221677359644*np.maximum(0, x-500)
```

The corresponding low/high slopes are 0.236805055829 and 0.015127696185 µA/µM, respectively (ratio ≈ 15.65). Concentration is in µM and current in µA.

## Independently generated V34 simulation reference

With seed 20260909 and the original random-draw sequence (model-family recovery, sparse/dense design, then validation hierarchy), previously generated independent V34 results were:

| Metric | Sparse | Dense |
| --- | ---: | ---: |
| Breakpoint 2.5th percentile (µM) | 425.87 | 465.57 |
| Breakpoint median (µM) | 500.00 | 500.00 |
| Breakpoint 97.5th percentile (µM) | 567.03 | 531.80 |
| Inverse RMSE at 2 mM (µM) | 357.07 | 279.57 |
| Inverse RMSE at 3 mM (µM) | 304.12 | 291.65 |

The separate validation-hierarchy simulations reported LOCO/random RMSE ratios of 1.04–1.41 (level-offset SD 0), 1.54–1.67 (1 µA), and 1.78–1.89 (3.5 µA), conditional on simulated temporal dependence and level offsets.

These are **independent reference calculations, not an executed PASS result for this branch**.

## Mandatory verification before merge/publication

1. Install dependencies: `pip install -r requirements.txt`.
2. Run: `python run_all.py`.
3. Run: `pytest -q`.
4. Compare generated model and simulation CSV values with the V34 reference outputs and current manuscript/SI, noting numerical tolerances and RNG order.
5. Confirm public redistribution rights for shared raw datasets with all coauthors, as flagged in `DATA_ORIGIN.md`.
6. Record commit SHA, environment versions, command output and test outcome in a final report. Replace this pending status **only after tests have actually passed**.


## CI run and output comparison (V38)

GitHub Actions run 37829925167 completed successfully for commit 68ec8af97e5f790703c43fe9b89c5ff6a8e7ba73. Python 3.11.17; full analysis passed; pytest: four passed. Artifact: cunw-analysis-outputs, ID 11573600123.

The generated sparse/dense simulation summary matches V34 to a maximum absolute difference of 4.6e-6 across two rows. The 12-row validation hierarchy grid matches to 1.3e-9. In contrast, the 40-row model-family recovery result differs substantially: the V34 reference reports 0/150 Langmuir selections for the sparse Langmuir simulation, while the GitHub run reports 139/150. The sparse Hill simulation reports 0/150 Hill selections in V34 versus 141/150 in the workflow output.

Overall: CI passed; complete V34 manuscript and supplementary figure reconciliation is pending. Figures S7-S8 and their underlying reference CSV should be audited before merging this PR.

## Current execution status

**CI PASSED; FULL V34 RECONCILIATION PENDING.**
