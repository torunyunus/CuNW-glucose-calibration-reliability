
import sys
from pathlib import Path
import numpy as np, matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from cunw_calibration.io import *
from cunw_calibration.signal import detect_change_points,extract_plateaus
from cunw_calibration.plotstyle import savefig

cfg=load_config()
t,y=load_trace()
c,pub=load_published_calibration()
nominal_t,nominal_c=load_nominal_schedule()
cc=cfg["change_point"]; pc=cfg["plateau"]

cps,score,idx=detect_change_points(
    t,y,cc["score_half_window_s"],cc["min_event_separation_s"],9,90,550,cc["peak_prominence_uA"]
)
pl=extract_plateaus(
    t,y,cps,pc["delay_s"],pc["duration_s"],pc["next_event_safety_s"],
    nominal_addition_times=nominal_t,addition_safety_s=1.0
)

rows=[]
for ci,cp,mu,sd,rho,neff,win,p in zip(c,cps,pl["mean"],pl["sd"],pl["rho1"],pl["neff_ar1"],pl["windows"],pub):
    rows.append([ci,cp,win[0],win[1],win[2],mu,sd,rho,neff,p,mu-p])
write_csv(OUTPUT_TABLES/"reconstructed_calibration.csv",
["concentration_uM","change_point_s","plateau_start_s","plateau_end_s","n_time_points","extracted_current_uA","plateau_sd_uA","rho1","neff_ar1","published_current_uA","difference_uA"],rows)

print("Change points:",cps.tolist())
print("MAE",np.mean(np.abs(pl["mean"]-pub)),"RMSE",np.sqrt(np.mean((pl["mean"]-pub)**2)))
print("Median rho1",np.median(pl["rho1"]),"Median N_eff",np.median(pl["neff_ar1"]))

plt.figure(figsize=(10,5));plt.plot(t,y,linewidth=1)
for cp in cps: plt.axvline(cp,linestyle="--",linewidth=.8)
for (st,en,_),mu in zip(pl["windows"],pl["mean"]): plt.hlines(mu,st,en,linewidth=2)
plt.xlabel("Time (s)");plt.ylabel("Current (µA)")
plt.title("Raw amperometric trace and chronology-aware plateaus")
savefig(OUTPUT_FIGURES/"Figure2a_raw_trace_reconstruction.png")

plt.figure(figsize=(6,5));plt.scatter(pub,pl["mean"])
lims=[min(pub.min(),pl["mean"].min())-2,max(pub.max(),pl["mean"].max())+2]
plt.plot(lims,lims,linestyle="--")
plt.xlabel("Published current (µA)");plt.ylabel("Extracted current (µA)")
savefig(OUTPUT_FIGURES/"Figure2b_extracted_vs_published.png")
