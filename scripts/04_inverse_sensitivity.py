
import sys
from pathlib import Path
import numpy as np, matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from cunw_calibration.io import *
from cunw_calibration.models import fit_fixed_segmented
from cunw_calibration.analysis import wild_bootstrap_slope_ratio
from cunw_calibration.plotstyle import savefig
cfg=load_config();a=np.genfromtxt(OUTPUT_TABLES/"reconstructed_calibration.csv",delimiter=",",names=True);c=a["concentration_uM"];y=a["extracted_current_uA"]
fit=fit_fixed_segmented(c,y,cfg["primary_knot_uM"]);b=fit["params"];sl=b[1];sh=b[1]+b[2];ratio=sl/sh
boot=wild_bootstrap_slope_ratio(c,y,500,cfg["bootstrap"]["n_iterations"],cfg["bootstrap"]["seed"])
write_csv(OUTPUT_TABLES/"inverse_sensitivity_summary.csv",["low_slope","high_slope","ratio","inverse_low","inverse_high","boot_median","boot_q2_5","boot_q97_5"],
[[sl,sh,ratio,1/sl,1/sh,boot["median"],boot["q2_5"],boot["q97_5"]]])
print(sl,sh,ratio,boot["q2_5"],boot["q97_5"])
plt.figure(figsize=(6.5,5));plt.bar(["≤500 µM",">500 µM"],[1/sl,1/sh]);plt.ylabel("dC/dI (µM/µA)")
savefig(OUTPUT_FIGURES/"Figure5_inverse_sensitivity.png")
