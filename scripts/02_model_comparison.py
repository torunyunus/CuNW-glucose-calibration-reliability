
import sys
from pathlib import Path
import numpy as np, matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from cunw_calibration.io import *
from cunw_calibration.models import *
from cunw_calibration.analysis import profile_breakpoint
from cunw_calibration.plotstyle import savefig
a=np.genfromtxt(OUTPUT_TABLES/"reconstructed_calibration.csv",delimiter=",",names=True);c=a["concentration_uM"];y=a["extracted_current_uA"]
res=[];xp=np.linspace(0,4000,800);plt.figure(figsize=(8,5.5));plt.scatter(c,y,label="Extracted")
for model,fitter in FITTERS.items():
    fit=fitter(c,y);yh=fit["predict"](c);_,e=forward_loco(c,y,model)
    res.append([model,r2(y,yh),aicc(y,yh,PARAM_COUNT[model]),np.sqrt(np.mean(e**2))]);plt.plot(xp,fit["predict"](xp),label=model)
write_csv(OUTPUT_TABLES/"model_comparison_forward.csv",["model","R2","AICc","forward_LOCO_RMSE_uA"],res)
plt.xlabel("Concentration (µM)");plt.ylabel("Current (µA)");plt.legend(fontsize=8);savefig(OUTPUT_FIGURES/"Figure3a_model_comparison.png")
prof=profile_breakpoint(c,y,tuple(load_config()["free_knot_search_uM"]))
write_csv(OUTPUT_TABLES/"breakpoint_profile_summary.csv",["knot_best_uM","support_low_uM","support_high_uM","rss_min","critical_rss"],
[[prof["knot_best"],prof["support_low"],prof["support_high"],prof["rss_min"],prof["critical_rss"]]])
print(prof["knot_best"],prof["support_low"],prof["support_high"])
plt.figure(figsize=(7,5));plt.plot(prof["grid_knot"],prof["grid_rss"]);plt.axhline(prof["critical_rss"],linestyle="--")
plt.axvline(prof["knot_best"],linestyle="--");plt.axvline(500,linestyle=":");plt.xlabel("Breakpoint (µM)");plt.ylabel("RSS")
savefig(OUTPUT_FIGURES/"Figure3b_breakpoint_profile.png")
