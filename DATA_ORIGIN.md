# Data origin and provenance

Source study: A. Zeynalova, A. Ateş and K. O. Oskay, "Synergistic Enhancement of Glucose Sensing via Copper Nanowire-biochar Nanocomposites", Topics in Catalysis (2026), DOI: 10.1007/s11244-026-02297-y.

CSV mapping:
- `fig4b_amperometric_trace.csv`: `Amperometric response!B4:C1304`
- `published_calibration.csv`: `Amperometric response!N5:O10` + `R5:S8`
- `scan_rate_summary.csv`: `scan rate!H3:I7`
- `potential_selection.csv`: `Voltaj seçimi!D:E` (0.7 V), `F:G` (0.6 V), `H:I` (0.5 V)
- `interference_trace.csv`: `Amperometric!E2:F413`
- `eis_fitted_parameters.csv`: Table 2 of the source paper
- `nominal_dosing_schedule.csv`: nominal sequence supplied by the experimental group

Open issue: the nominal dosing clock and raw-trace event clock differ by ~36–37 s. This is under investigation and is not assigned a causal explanation in the code.

Before public release, confirm redistribution permission with all experimental data owners/authors.
