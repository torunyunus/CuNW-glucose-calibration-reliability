# CuNWs/Fe-BC calibration-reliability reproducibility repository

This repository reproduces the Python analyses, tables and data-derived figures for the regime-aware calibration and inverse-quantification study based on the CuNWs/Fe-BC amperometric glucose platform.

## What is reproduced
- raw-trace change-point detection and chronology-aware plateau extraction
- temporal-dependence diagnostics
- five calibration models: linear, fixed segmented, free segmented, Langmuir, Hill
- R², AICc and forward LOCO
- inverse LOCO for all models
- free-breakpoint profile analysis
- local inverse sensitivity and wild bootstrap
- 81-setting chronology-aware extraction robustness analysis
- concentration-level jackknife
- model-family recovery simulations
- sparse-versus-dense breakpoint simulations
- validation-hierarchy simulations
- supporting scan-rate, working-potential, interference and EIS calculations
- assembly of the submitted data-derived figures

## Reproduce everything
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
python run_all.py
pytest -q
```

Expected chronology-aware core results:
- nominal additions: 100, 150, 200, 250, 300, 350, 400, 450, 500 s
- detected change points: 111, 165, 213, 263, 319, 365, 411, 462, 514 s
- operational lag: 11–19 s; median 13 s; mean 13.7 s
- reconstruction RMSE ≈ 0.63 µA
- low slope ≈ 0.236805 µA/µM
- high slope ≈ 0.015128 µA/µM
- slope ratio ≈ 15.65×
- fixed-boundary forward LOCO RMSE ≈ 8.39 µA

## Chronology-aware plateau rule
For every non-final concentration, plateau extraction is capped before the next physical analyte addition:

```
end_j = min(cp_j + delay + duration,
            cp_{j+1} - safety,
            add_{j+1} - 1 s)
```

This prevents post-addition samples from being assigned to the preceding concentration level.

## Interpretation
- The 500 µM boundary is a publication-informed reference boundary.
- Dense time samples are not treated as independent calibration conditions.
- The 5 and 4000 µM LOCO cases are edge/extrapolation stress tests.
- Bootstrap and Monte Carlo iterations do not create experimental replicates.
- The 11–19 s operational lag is not interpreted as a pure kinetic response time.

## Submission figure assembly
`08_assemble_submission_figures.py` assembles the submitted data-derived figure set from regenerated analysis figures. The conceptual workflow diagram (Main Figure 1) and supporting electrochemical composite (Supplementary Figure S5) are retained as static source assets.

Repository: https://github.com/torunyunus/CuNW-glucose-calibration-reliability
