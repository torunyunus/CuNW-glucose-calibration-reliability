# Data origin and provenance

Source study: A. Zeynalova, A. Ateş and K. O. Oskay, "Synergistic Enhancement of Glucose Sensing via Copper Nanowire-biochar Nanocomposites", Topics in Catalysis (2026), DOI: 10.1007/s11244-026-02297-y.

CSV mapping:
- `fig4b_amperometric_trace.csv`: `Amperometric response!B4:C1304`
- `published_calibration.csv`: `Amperometric response!N5:O10` + `R5:S8`
- `scan_rate_summary.csv`: `scan rate!H3:I7`
- `potential_selection.csv`: `Voltaj seçimi!D:E` (0.7 V), `F:G` (0.6 V), `H:I` (0.5 V)
- `interference_trace.csv`: `Amperometric!E2:F413`
- `eis_fitted_parameters.csv`: Table 2 of the source paper
- `nominal_dosing_schedule.csv`: nominal analyte-addition sequence clarified by the experimental group during manuscript preparation

## Corrected dosing chronology

The experimental group clarified that the cumulative glucose additions were nominally:
100 s → 5 µM,
150 s → 50 µM,
200 s → 100 µM,
250 s → 150 µM,
300 s → 200 µM,
350 s → 500 µM,
400 s → 2000 µM,
450 s → 3000 µM,
500 s → 4000 µM.

The algorithmically detected current transitions are 111, 165, 213, 263, 319, 365, 411, 462, and 514 s, corresponding to nominal-addition-to-detected-transition lags of 11, 15, 13, 13, 19, 15, 11, 12, and 14 s, respectively (range 11–19 s; median 13 s; mean 13.7 s).

This operational lag is not treated as a pure electrochemical kinetic response time. It can include solution mixing, response development, acquisition timing, and the location returned by the median-window change-point detector.

Before public release, confirm redistribution permission with all experimental data owners/authors.
