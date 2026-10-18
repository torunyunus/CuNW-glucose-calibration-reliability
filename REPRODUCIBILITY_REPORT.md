# Computational reproducibility report

## Release and validation status

This report summarizes the executable calibration-reliability analysis associated with the source revision **`22af58be481782a4bc7e421b623902890efccb8d`** (18 October 2026). It supersedes the pending-verification status and obsolete model-family simulation comparisons recorded in earlier versions of this report.

- **Validated source revision:** [`22af58be481782a4bc7e421b623902890efccb8d`](https://github.com/torunyunus/CuNW-glucose-calibration-reliability/commit/22af58be481782a4bc7e421b623902890efccb8d)
- **GitHub Actions verification:** [Run 39146010847](https://github.com/torunyunus/CuNW-glucose-calibration-reliability/actions/runs/39146010847) — **completed successfully** for that exact source revision.
- **Execution environment:** GitHub Actions, Ubuntu runner, Python 3.11.17; dependencies installed from `requirements.txt`.
- **Executed commands:** `python run_all.py` and `python -m pytest -q`.
- **Test outcome:** **6 passed** (pytest, 0.44 s). All workflow stages, including the full analysis and upload of generated outputs, completed successfully.
- **Generated-output artifact:** `cunw-analysis-outputs` (artifact ID `12143223230`), containing 46 files from this run. [View workflow artifact](https://github.com/torunyunus/CuNW-glucose-calibration-reliability/actions/runs/39146010847/artifacts/12143223230).

These observations verify that the specified code revision executed successfully and passed its repository regression checks. They do **not** constitute independent-electrode validation, external analytical validation, or an independent replication of the experimental study.

## Source data and experimental chronology

The underlying measurements were previously reported by Zeynalova, Ateş and Oskay (*Topics in Catalysis*, 2026; DOI: [10.1007/s11244-026-02297-y](https://doi.org/10.1007/s11244-026-02297-y)). No new electrode measurements are introduced by this computational work. File provenance and extraction mapping are documented in [`DATA_ORIGIN.md`](DATA_ORIGIN.md).

The calibration analysis uses one sequential amperometric record with nine cumulative glucose levels: **5, 50, 100, 150, 200, 500, 2000, 3000 and 4000 µM**. The experimental group clarified nominal addition times of **100, 150, 200, 250, 300, 350, 400, 450 and 500 s**. The detected current transitions were **111, 165, 213, 263, 319, 365, 411, 462 and 514 s**. The resulting operational lags (11–19 s; median 13 s) include mixing, acquisition and detection-window effects; they are **not** intrinsic electrode-response times.

For every non-final plateau, extraction ends before the next nominal addition. Concentration-level means—not individual temporally correlated current samples—are the units of calibration fitting and leave-one-concentration-out (LOCO) prediction. The fixed 500 µM boundary is taken from the previously published calibration analysis of this same record.

## Reproduction instructions

Use the validated source revision above, rather than assuming the repository's default branch contains the same analysis.

```bash
git checkout 22af58be481782a4bc7e421b623902890efccb8d
python -m pip install -r requirements.txt
python run_all.py
python -m pytest -q
```

The full pipeline reconstructs the calibration, fits five response families, evaluates forward and inverse LOCO prediction, performs breakpoint and local-conditioning analyses, runs controlled simulations, and produces supporting electrochemical calculations and data-derived figures. Additional numerical detail and source-code organization are given in [`README.md`](README.md).

## Variance-inclusive AICc: executable implementation

The analysis uses the small-sample corrected Akaike information criterion with the **estimated residual variance counted as a parameter**:

```text
n = 9
k = p + 1
AICc = n * ln(RSS/n) + 2*k + 2*k*(k+1)/(n-k-1)
```

Here `p` is the number of fitted mean-response parameters. A constant common to the Gaussian likelihoods is omitted. The corresponding `k` values are **3, 4, 5, 4 and 5** for the linear, fixed-500-µM segmented, free-breakpoint segmented, Langmuir and Hill models, respectively.

| Model | AICc (variance-inclusive) |
| --- | ---: |
| Single linear | 71.42 |
| Continuous segmented, fixed 500 µM boundary | 47.94 |
| Continuous segmented, free breakpoint | 55.40 |
| Langmuir | 60.86 |
| Hill | 59.41 |

In a separate parameter-count sensitivity calculation, assigning one additional effective parameter to the previously selected reference boundary increases the fixed-boundary model's AICc to **59.94**. This is a sensitivity analysis, not a redefinition of the principal fitted response.

The same variance-inclusive parameter counting is applied in the model-family recovery simulations. Implementation details and the corresponding numerical update are recorded in [`AICc_UPDATE.md`](AICc_UPDATE.md).

## Resolution of the earlier model-family discrepancy

An earlier simulation reference incorrectly reported zero selection of some nonlinear response families. The discrepancy was traced to an **omitted SciPy `least_squares` import** in the older simulation reference script; broad exception handling then assigned infinite AICc to the affected Langmuir and Hill fits. Those historical model-family selection frequencies and associated figures **must not be used as current reference outputs**.

The corrected executable workflow includes the nonlinear candidate fits and the variance-inclusive AICc calculation. For the source revision cited above, the full workflow and six regression checks passed in GitHub Actions. Its associated model-family output and the regenerated Supplementary Figures S7–S8 supersede the invalid earlier reference. The update notes report **2400 successful nonlinear solver calls** in the corrected model-family rerun.

The sparse/dense breakpoint experiment and validation-hierarchy simulation address separate questions; their numerical results must not be conflated with model-family selection frequencies.

## Interpretation and limits of verification

- The regression tests and successful workflow establish **computational execution and consistency against the implemented checks**, not the physical correctness of any fitted response model.
- The reported LOCO values are **retrospective within-record diagnostics**. In particular, retaining the original 500 µM knot in each fixed-knot holdout makes those predictions conditional on a boundary previously inferred from the same series.
- Bootstrap results and Monte Carlo simulations are conditional on their stated response and noise assumptions; they do not provide independent experimental replicates.
- Glucose concentration and elapsed time increased together in the original sequence. Temporal drift or electrode conditioning cannot be disentangled from concentration response without new measurements.
- Generalization to independent electrodes, newly prepared standards, blinded unknowns and sample matrices has **not** been established.

**Versioning note:** This report documents the validated source commit above. Any later documentation-only commit does not retroactively change the contents of that immutable commit or its recorded CI run. If analysis source, data, dependencies or tests change, verify the new revision separately and update this report and the manuscript's Data Availability reference accordingly.
