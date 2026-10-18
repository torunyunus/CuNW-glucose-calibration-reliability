# Variance-inclusive AICc correction supplement

Baseline repository commit: b25fbe4000ea9624016e98e00cbdd796c52465a2
Baseline GitHub Actions run: 37830789777 (successful; validates the baseline).
This update contains the corrected executable source. The reproducibility workflow runs the full analysis and six regression tests, and publishes generated outputs as a GitHub Actions artifact. The cited baseline run validates the baseline only; use the workflow run attached to the corrected commit for the current validation.

## Reproduce
From the analysis directory, install requirements.txt in a compatible Python environment, then run:

    python run_all.py
    python run_validation.py

The six regression checks comprise the four unchanged baseline checks and two checks for AICc parameter counting / the small-sample denominator. All six passed locally.

## Calculation
The aicc function accepts the number p of mean-function parameters, adds the estimated residual variance (k = p + 1), and calculates n*log(RSS/n) + 2*k + 2*k*(k+1)/(n-k-1). A common Gaussian likelihood constant is omitted. The same variance-inclusive criterion is used in all model-family simulations. The optional reference-knot sensitivity adds a further parameter only to the fixed-knot model (k = 5 at n = 9); this is distinct from counting variance.

Corrected experimental AICc values, in model order (linear, fixed segmented, free segmented, Langmuir, Hill): 71.421985, 47.940955, 55.395845, 60.855463, 59.410728. Fixed-knot sensitivity AICc: 59.940955.

Only model_comparison_forward.csv and simulation_model_family_recovery.csv changed among the original numerical tables. Reconstruction, slopes, breakpoint profiling, LOCO predictions, bootstrap results, sparse/dense design simulation and validation-hierarchy tables were byte-identical to the local baseline rerun. The updated model-family figures are Figure_S7_AICc_corrected.png and Figure_S8_AICc_corrected.png; these are the figures embedded in the revised Supplementary Information. Their blue colour scale and 2200 x 1375 pixel canvas are retained.

A convergence audit of the model-family rerun recorded 2400 nonlinear fits, all successful. The random seed and draw order are unchanged.

The original README and reproducibility report included in the baseline source describe the prior workflow. This update note and the corrected outputs are authoritative for the AICc correction.
