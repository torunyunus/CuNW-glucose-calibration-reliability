# CuNWs/Fe-BC calibration-reliability reproducibility repository

This repository reproduces the Python analyses, tables and figures for the regime-aware calibration and inverse-quantification study based on the CuNWs/Fe-BC amperometric glucose platform.

## What is reproduced
- raw-trace change-point detection and plateau extraction
- temporal-dependence diagnostics
- five calibration models: linear, fixed segmented, free segmented, Langmuir, Hill
- R², AICc and forward LOCO
- inverse LOCO for all models
- free-breakpoint profile analysis
- local inverse sensitivity and wild bootstrap
- 81-setting extraction robustness analysis
- concentration-level jackknife
- model-family recovery simulations
- sparse-versus-dense breakpoint simulations
- validation-hierarchy simulations
- supporting scan-rate, working-potential, interference and EIS calculations

## Installation
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
```

## Reproduce everything
```bash
python run_all.py
```

Figures are written to `outputs/figures/` and tables to `outputs/tables/`.

## Verify frozen results
```bash
pytest -q
```

Expected core results:
- change points: 111, 165, 213, 263, 319, 365, 411, 462, 514 s
- reconstruction RMSE ≈ 0.64 µA
- low slope ≈ 0.23655 µA/µM
- high slope ≈ 0.015152 µA/µM
- slope ratio ≈ 15.61×
- fixed-knot forward LOCO RMSE ≈ 8.32 µA

## Important interpretation
- The 500 µM boundary is a publication-informed reference boundary.
- Time points from one plateau are not treated as independent calibration levels.
- The 5 and 4000 µM LOCO cases are edge/extrapolation stress tests.
- Bootstrap and Monte Carlo iterations do not create new experimental replicates.
- The current ~36–37 s nominal-time/raw-trace offset is unresolved and should not be explained speculatively.

## GitHub/Zenodo release checklist
1. confirm all co-authors approve public redistribution of raw/processed data;
2. add the final author list and repository license;
3. create a tagged release (for example `v1.0.0-analytical-methods`);
4. archive that release on Zenodo and obtain a DOI;
5. cite the GitHub/Zenodo DOI in the manuscript Data Availability section.
