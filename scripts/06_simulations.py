
import sys
from pathlib import Path
import numpy as np, matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from cunw_calibration.io import *
from cunw_calibration.models import *
from cunw_calibration.plotstyle import savefig
rng=np.random.default_rng(load_config()["simulation"]["seed"]);sparse=np.array(load_config()["concentrations_uM"],float)
dense=np.array([5,50,100,150,200,300,400,500,650,800,1000,1250,1500,1750,2000,2500,3000,3500,4000.])
def seg(x):x=np.asarray(x,float);return 18.38539275+.23654670*x-.22139490*np.maximum(0,x-500)
truths={"Linear":lambda x:20+.04*np.asarray(x,float),"Segmented":seg,
"Langmuir":lambda x:13.77247083+192.57594563*np.asarray(x,float)/(479.31238219+np.asarray(x,float)),
"Hill":lambda x:30.07886340+147.68514925*((np.asarray(x,float)/347.63978836)**2.37971365)/(1+(np.asarray(x,float)/347.63978836)**2.37971365)}
rec=[];nrep=150
for dn,d in [("Sparse",sparse),("Dense",dense)]:
  for tn,tf in truths.items():
    counts={m:0 for m in FITTERS}
    for _ in range(nrep):
      yy=tf(d)+rng.normal(0,4,len(d));scores={}
      for m,f in FITTERS.items():
        try:fit=f(d,yy);scores[m]=aicc(yy,fit["predict"](d),PARAM_COUNT[m])
        except:scores[m]=np.inf
      counts[min(scores,key=scores.get)]+=1
    for m,n in counts.items():rec.append([dn,tn,m,n,100*n/nrep])
write_csv(OUTPUT_TABLES/"simulation_model_family_recovery.csv",["design","truth_family","selected_model","count","frequency_percent"],rec)
for dn in ["Sparse","Dense"]:
  T=list(truths);M=list(FITTERS);mat=np.zeros((len(T),len(M)))
  for r in rec:
    if r[0]==dn:mat[T.index(r[1]),M.index(r[2])]=r[4]
  plt.figure(figsize=(8,4.8));im=plt.imshow(mat,aspect="auto");plt.xticks(range(len(M)),M,rotation=25,ha="right");plt.yticks(range(len(T)),T);plt.colorbar(im,label="Selection (%)")
  for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):plt.text(j,i,f"{mat[i,j]:.0f}",ha="center",va="center",fontsize=8)
  savefig(OUTPUT_FIGURES/f"FigureS7_model_recovery_{dn.lower()}.png")
sim={}
for name,d in [("Sparse",sparse),("Dense",dense)]:
  ks=[];e2=[];e3=[]
  for _ in range(500):
    yy=seg(d)+rng.normal(0,4,len(d));fit=fit_free_segmented(d,yy,(150,1500));ks.append(fit["knot"])
    test=seg([2000,3000])+rng.normal(0,4,2)
    for val,true,arr in [(test[0],2000,e2),(test[1],3000,e3)]:arr.append(inverse_predict("Free-knot segmented",fit,val)-true)
  sim[name]=(np.asarray(ks),np.asarray(e2),np.asarray(e3))
write_csv(OUTPUT_TABLES/"simulation_sparse_dense_summary.csv",["design","knot_q2_5","knot_median","knot_q97_5","inverse_RMSE_2mM","inverse_RMSE_3mM"],
[[n,*np.percentile(v[0],[2.5,50,97.5]),np.sqrt(np.mean(v[1]**2)),np.sqrt(np.mean(v[2]**2))] for n,v in sim.items()])
plt.figure(figsize=(7,5));plt.hist(sim["Sparse"][0],bins=35,alpha=.55,label="Sparse");plt.hist(sim["Dense"][0],bins=35,alpha=.55,label="Dense");plt.axvline(500,linestyle="--");plt.legend();savefig(OUTPUT_FIGURES/"Figure6a_breakpoint_identifiability.png")
def ar1(n,rho,sigma):
  x=np.zeros(n);x[0]=rng.normal(0,sigma);sd=sigma*np.sqrt(max(0,1-rho*rho))
  for i in range(1,n):x[i]=rho*x[i-1]+rng.normal(0,sd)
  return x
grid=[]
for offsd in [0,1,3.5]:
  for rho in [0,.3,.6,.9]:
    rr=[];gg=[]
    for _ in range(150):
      cs=[];ys=[];groups=[];lo=rng.normal(0,offsd,len(sparse))
      for g,c in enumerate(sparse):
        yy=seg(c)+lo[g]+ar1(20,rho,.55);cs.extend([c]*20);ys.extend(yy);groups.extend([g]*20)
      cs=np.asarray(cs);ys=np.asarray(ys);groups=np.asarray(groups);idx=rng.permutation(len(cs));cut=int(.75*len(cs));tr,te=idx[:cut],idx[cut:]
      fit=fit_fixed_segmented(cs[tr],ys[tr],500);p=np.array([inverse_predict("Fixed-knot segmented",fit,v) for v in ys[te]]);rr.append(np.sqrt(np.mean((cs[te]-p)**2)))
      pp=[];tt=[]
      for g in np.unique(groups):
        tr=groups!=g;te=groups==g;fit=fit_fixed_segmented(cs[tr],ys[tr],500);pp.extend([inverse_predict("Fixed-knot segmented",fit,v) for v in ys[te]]);tt.extend(cs[te])
      gg.append(np.sqrt(np.mean((np.asarray(tt)-np.asarray(pp))**2)))
    grid.append([offsd,rho,np.median(rr),np.median(gg),np.median(gg)/np.median(rr)])
write_csv(OUTPUT_TABLES/"simulation_validation_hierarchy_grid.csv",["level_offset_SD_uA","rho","random_split_median_RMSE_uM","LOCO_median_RMSE_uM","LOCO_to_random_ratio"],grid)
mat=np.zeros((3,4));offs=[0,1,3.5];rhos=[0,.3,.6,.9]
for r in grid:mat[offs.index(r[0]),rhos.index(r[1])]=r[4]
plt.figure(figsize=(6.8,4.8));im=plt.imshow(mat,aspect="auto");plt.xticks(range(4),rhos);plt.yticks(range(3),offs);plt.colorbar(im,label="LOCO/random RMSE")
for i in range(3):
  for j in range(4):plt.text(j,i,f"{mat[i,j]:.2f}",ha="center",va="center")
savefig(OUTPUT_FIGURES/"FigureS9_validation_hierarchy.png")
