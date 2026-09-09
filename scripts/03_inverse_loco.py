
import sys
from pathlib import Path
import numpy as np, matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from cunw_calibration.io import *
from cunw_calibration.models import *
from cunw_calibration.plotstyle import savefig
a=np.genfromtxt(OUTPUT_TABLES/"reconstructed_calibration.csv",delimiter=",",names=True);c=a["concentration_uM"];y=a["extracted_current_uA"]
summary=[];detail=[];plt.figure(figsize=(8,5.5))
for model in FITTERS:
    pred=inverse_loco(c,y,model);valid=np.isfinite(pred);err=pred-c;interior=np.arange(1,len(c)-1);vint=valid[interior];eint=pred[interior][vint]-c[interior][vint]
    summary.append([model,valid.sum(),np.sqrt(np.mean(err[valid]**2)),np.mean(np.abs(err[valid])),vint.sum(),np.sqrt(np.mean(eint**2))])
    for ci,yi,pi in zip(c,y,pred):detail.append([model,ci,yi,pi if np.isfinite(pi) else "",pi-ci if np.isfinite(pi) else "","edge" if ci in (c.min(),c.max()) else "interior","valid" if np.isfinite(pi) else "no_finite_positive_inverse"])
    plt.plot(c[valid],pred[valid],marker="o",label=model)
write_csv(OUTPUT_TABLES/"inverse_LOCO_summary.csv",["model","valid_inverse_count","inverse_LOCO_RMSE_uM","inverse_LOCO_MAE_uM","valid_interior_count","interior_inverse_RMSE_uM"],summary)
write_csv(OUTPUT_TABLES/"inverse_LOCO_all_models.csv",["model","true_concentration_uM","heldout_current_uA","inverse_prediction_uM","inverse_error_uM","holdout_type","inverse_status"],detail)
plt.plot(c,c,linestyle="--",label="Ideal");plt.xscale("log");plt.yscale("symlog",linthresh=50);plt.xlabel("True concentration (µM)");plt.ylabel("LOCO inverse prediction (µM)");plt.legend(fontsize=8)
savefig(OUTPUT_FIGURES/"Figure4_inverse_LOCO_all_models.png")
for r in summary:print(r)
