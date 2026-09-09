
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from cunw_calibration.io import *
from cunw_calibration.supporting import *
scan=scan_rate_metrics();pot=potential_metrics();itf=interference_metrics();eis=eis_ratios()
write_csv(OUTPUT_TABLES/"supporting_scan_rate.csv",["model","slope","intercept","R2","LOOCV_RMSE_uA"],
[["I~v",scan["linear_v"]["slope"],scan["linear_v"]["intercept"],scan["linear_v"]["r2"],scan["linear_v"]["loocv_rmse"]],
["I~sqrt(v)",scan["sqrt_v"]["slope"],scan["sqrt_v"]["intercept"],scan["sqrt_v"]["r2"],scan["sqrt_v"]["loocv_rmse"]]])
write_csv(OUTPUT_TABLES/"supporting_potential.csv",["potential_V","mean_uA","drift_uA_s","detrended_sd_uA"],[[p,d["mean_uA"],d["drift_uA_s"],d["detrended_sd_uA"]] for p,d in sorted(pot.items())])
write_csv(OUTPUT_TABLES/"supporting_interference.csv",["interferent","normalized_percent"],[[k,v] for k,v in itf["normalized_percent"].items()])
write_csv(OUTPUT_TABLES/"supporting_eis_ratios.csv",["parameter","ratio"],[[k,v] for k,v in eis.items()])
print(scan);print(pot);print(itf);print(eis)
