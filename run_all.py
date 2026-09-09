from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "01_reconstruct_calibration.py",
    "02_model_comparison.py",
    "03_inverse_loco.py",
    "04_inverse_sensitivity.py",
    "05_robustness_jackknife.py",
    "06_simulations.py",
    "07_supporting_electrochem.py",
]

for script in SCRIPTS:
    print(f"\n=== Running {script} ===", flush=True)
    runpy.run_path(str(ROOT / "scripts" / script), run_name="__main__")

print("\nAll analyses completed.", flush=True)
