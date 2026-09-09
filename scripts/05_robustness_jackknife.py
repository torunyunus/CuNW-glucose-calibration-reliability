
import sys
from pathlib import Path
import numpy as np, matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from cunw_calibration.io import *
from cunw_calibration.signal import detect_change_points,extract_plateaus
from cunw_calibration.models import fit_fixed_segmented,fit_free_segmented
from cunw_calibration.analysis import jackknife_fixed_and_knot
from cunw_calibration.plotstyle import savefig
t,y=load_trace();c,pub=load_published_calibration();grid=[]
for w in [6,8,10]:
  for sep in [25,30,35]:
    cps,_,_=detect_change_points(t,y,w,sep,9,90,550,.5)
    for delay in [15,20,25]:
      for dur in [15,20,25]:
        pl=extract_plateaus(t,y,cps,delay,dur,8);ff=fit_fixed_segmented(c,pl["mean"],500);b=ff["params"];fk=fit_free_segmented(c,pl["mean"],(100,1500))
        grid.append([w,sep,delay,dur,np.sqrt(np.mean((pl["mean"]-pub)**2)),b[1]/(b[1]+b[2]),fk["knot"]])
write_csv(OUTPUT_TABLES/"parameter_grid_results.csv",["score_window_s","min_event_separation_s","plateau_delay_s","plateau_duration_s","published_RMSE_uA","slope_ratio","free_breakpoint_uM"],grid)
a=np.asarray(grid,float);print(a[:,4].min(),a[:,4].max(),a[:,5].min(),a[:,5].max(),a[:,6].min(),a[:,6].max())
plt.figure(figsize=(7,5));plt.scatter(a[:,4],a[:,5]);plt.xlabel("RMSE (µA)");plt.ylabel("Slope ratio");savefig(OUTPUT_FIGURES/"FigureS1_parameter_grid.png")
plt.figure(figsize=(7,5));plt.hist(a[:,6],bins=20);plt.axvline(500,linestyle=":");savefig(OUTPUT_FIGURES/"FigureS2_breakpoint_grid.png")
cfg=load_config();cc=cfg["change_point"];pc=cfg["plateau"];cps,_,_=detect_change_points(t,y,8,30,9,90,550,.5);pl=extract_plateaus(t,y,cps,20,20,8)
jk=jackknife_fixed_and_knot(c,pl["mean"],500,(100,1500));write_csv(OUTPUT_TABLES/"jackknife_results.csv",["left_out_concentration_uM","low_slope","high_slope","slope_ratio","free_breakpoint_uM"],jk)
j=np.asarray(jk,float);print(j[:,3].min(),j[:,3].max(),j[:,4].min(),j[:,4].max())
plt.figure(figsize=(7,5));plt.plot(j[:,0],j[:,3],marker="o");plt.xscale("log");savefig(OUTPUT_FIGURES/"FigureS3_jackknife_ratio.png")
plt.figure(figsize=(7,5));plt.plot(j[:,0],j[:,4],marker="o");plt.xscale("log");plt.axhline(500,linestyle=":");savefig(OUTPUT_FIGURES/"FigureS4_jackknife_breakpoint.png")
