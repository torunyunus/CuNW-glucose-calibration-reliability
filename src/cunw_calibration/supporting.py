
import csv,numpy as np
from .io import DATA_RAW
def linear_fit(x,y):
    X=np.column_stack([np.ones_like(x),x]); b=np.linalg.lstsq(X,y,rcond=None)[0]; yh=X@b
    return b,yh,1-np.sum((y-yh)**2)/np.sum((y-y.mean())**2)
def scan_rate_metrics():
    a=[]
    with open(DATA_RAW/"scan_rate_summary.csv",newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):a.append((float(r["scan_rate_mV_s"]),float(r["current_uA"])))
    a=np.asarray(a); v,I=a[:,0],a[:,1]
    def loocv(x):
        p=[]
        for i in range(len(x)):
            keep=np.arange(len(x))!=i;b,_,_=linear_fit(x[keep],I[keep]);p.append(b[0]+b[1]*x[i])
        return float(np.sqrt(np.mean((I-np.asarray(p))**2)))
    b1,_,r1=linear_fit(v,I); b2,_,r2=linear_fit(np.sqrt(v),I)
    return {"linear_v":{"slope":b1[1],"intercept":b1[0],"r2":r1,"loocv_rmse":loocv(v)},
            "sqrt_v":{"slope":b2[1],"intercept":b2[0],"r2":r2,"loocv_rmse":loocv(np.sqrt(v))}}
def potential_metrics(tmin=200,tmax=249):
    rows={}
    with open(DATA_RAW/"potential_selection.csv",newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):rows.setdefault(float(r["potential_V"]),[]).append((float(r["time_s"]),float(r["current_uA"])))
    out={}
    for p,arr in rows.items():
        a=np.asarray(arr); mask=(a[:,0]>=tmin)&(a[:,0]<=tmax);t,y=a[mask,0],a[mask,1]
        b,yh,_=linear_fit(t,y);out[p]={"mean_uA":float(np.mean(y)),"drift_uA_s":float(b[1]),"detrended_sd_uA":float(np.sqrt(np.sum((y-yh)**2)/max(1,len(y)-2)))}
    return out
def _step(event,window=15,exclude=2):
    a=[]
    with open(DATA_RAW/"interference_trace.csv",newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):a.append((float(r["time_s"]),float(r["current_uA"])))
    a=np.asarray(a);x=a[:,0]-event;y=a[:,1];mask=(np.abs(x)<=window)&(np.abs(x)>=exclude);xx=x[mask];yy=y[mask]
    H=(xx>0).astype(float);X=np.column_stack([np.ones_like(xx),xx,H]);b=np.linalg.lstsq(X,yy,rcond=None)[0];return float(b[2])
def interference_metrics(window=15,exclude=2):
    ev={"Glc1":60,"AA":110,"UA":160,"Maltose":210,"NaCl":260,"Glc2":300};steps={k:_step(t,window,exclude) for k,t in ev.items()}
    ref=abs(steps["Glc2"]); return {"steps_uA":steps,"normalized_percent":{k:100*abs(steps[k])/ref for k in ["AA","UA","Maltose","NaCl"]}}
def eis_ratios():
    d={}
    with open(DATA_RAW/"eis_fitted_parameters.csv",newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):d[r["electrode"]]={k:float(r[k]) for k in ["Ru","Rct","Y0","n","Wd","chi2"]}
    a=d["CuNWs"];b=d["CuNWs_FeBC"];return {k:b[k]/a[k] for k in a}
