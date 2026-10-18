"""Publication tables and blue heatmaps for the variance-inclusive AICc update."""
import sys
from pathlib import Path
import numpy as np
import csv
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from cunw_calibration.io import OUTPUT_TABLES, OUTPUT_FIGURES
from cunw_calibration.models import FITTERS, PARAM_COUNT, aicc

with open(OUTPUT_TABLES / 'simulation_model_family_recovery.csv', newline='') as stream:
    df = list(csv.DictReader(stream))
families = ['Linear', 'Segmented', 'Langmuir', 'Hill']
models = list(FITTERS)
for design, number in [('Sparse', 7), ('Dense', 8)]:
    matrix = np.array([[float(next(r['frequency_percent'] for r in df if r['design'] == design and r['truth_family'] == f and r['selected_model'] == m))
                        for m in models] for f in families])
    fig, ax = plt.subplots(figsize=(8.8, 5.5), dpi=250)
    fig.subplots_adjust(left=.16, right=.92, bottom=.20, top=.97)
    im = ax.imshow(matrix, aspect='auto', cmap='Blues', vmin=0, vmax=100)
    ax.set_xticks(range(5), ['Single linear', 'Fixed-knot\nsegmented', 'Free-knot\nsegmented', 'Langmuir', 'Hill'])
    ax.set_yticks(range(4), families)
    ax.set_xlabel('Selected model', labelpad=8)
    ax.set_ylabel('Generating response family', labelpad=8)
    ax.set_xticks(np.arange(-.5, 5, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 4, 1), minor=True)
    ax.grid(which='minor', color='white', linewidth=2)
    ax.tick_params(which='both', length=0)
    for i in range(4):
        for j in range(5):
            ax.text(j, i, f'{matrix[i,j]:.0f}', ha='center', va='center', fontweight='bold', color='white' if matrix[i,j] > 50 else '#182333')
    fig.colorbar(im, ax=ax, fraction=.036, pad=.03, label='AICc selection frequency (%)')
    fig.savefig(OUTPUT_FIGURES / f'Figure_S{number}_AICc_corrected.png', dpi=250)
    plt.close(fig)

cal = np.genfromtxt(OUTPUT_TABLES / 'reconstructed_calibration.csv', delimiter=',', names=True)
c = cal['concentration_uM']; y = cal['extracted_current_uA']
rows = []
for model, fitter in FITTERS.items():
    fit = fitter(c, y)
    rows.append([model, PARAM_COUNT[model], PARAM_COUNT[model] + 1,
                 aicc(y, fit['predict'](c), PARAM_COUNT[model])])
with open(OUTPUT_TABLES / 'AICc_parameter_count_audit.csv', 'w', newline='') as stream:
    writer = csv.writer(stream)
    writer.writerow(['model', 'mean_parameters', 'total_parameters_including_variance', 'AICc'])
    writer.writerows(rows)
fit = FITTERS['Fixed-knot segmented'](c, y)
with open(OUTPUT_TABLES / 'AICc_reference_knot_sensitivity.csv', 'w', newline='') as stream:
    writer = csv.writer(stream)
    writer.writerow(['model', 'total_parameters_with_variance_and_reference_knot', 'AICc'])
    writer.writerow(['Fixed-knot segmented', 5, aicc(y, fit['predict'](c), 4)])
