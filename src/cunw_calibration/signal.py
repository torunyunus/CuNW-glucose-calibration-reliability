
import numpy as np
from scipy.signal import find_peaks

def change_score(t,y,half_window_s=8.0):
    t=np.asarray(t,float); y=np.asarray(y,float); score=np.full_like(y,np.nan)
    for i,ti in enumerate(t):
        pre=y[(t>=ti-half_window_s)&(t<ti)]
        post=y[(t>ti)&(t<=ti+half_window_s)]
        if len(pre)>=4 and len(post)>=4: score[i]=np.median(post)-np.median(pre)
    return score

def detect_change_points(t,y,half_window_s=8.0,min_separation_s=30.0,n_events=9,
                         time_min_s=90.0,time_max_s=550.0,prominence=0.5):
    t=np.asarray(t,float); score=change_score(t,y,half_window_s)
    dt=float(np.median(np.diff(t))); dist=max(1,int(round(min_separation_s/dt)))
    valid=(t>=time_min_s)&(t<=time_max_s)&np.isfinite(score)
    work=np.where(valid,score,-np.inf)
    peaks,_=find_peaks(work,distance=dist,prominence=prominence)
    peaks=[p for p in peaks if score[p]>0][:n_events]
    return t[peaks],score,np.asarray(peaks,int)

def extract_plateaus(t,y,change_points,delay_s=20.0,duration_s=20.0,next_event_safety_s=8.0,
                     nominal_addition_times=None,addition_safety_s=1.0):
    """Extract chronology-aware steady-state plateaus.

    When nominal_addition_times is supplied, each non-final plateau ends no
    later than one sample before the next physical analyte addition.
    """
    t=np.asarray(t,float); y=np.asarray(y,float); cps=np.asarray(change_points,float)
    nominal=None if nominal_addition_times is None else np.asarray(nominal_addition_times,float)
    if nominal is not None and len(nominal)!=len(cps):
        raise ValueError("nominal_addition_times must match change_points length")
    means=[]; sds=[]; rhos=[]; neffs=[]; wins=[]
    for j,cp in enumerate(cps):
        nxt=cps[j+1] if j+1<len(cps) else cp+delay_s+duration_s+10
        st=cp+delay_s
        en=min(cp+delay_s+duration_s,nxt-next_event_safety_s)
        if nominal is not None and j+1<len(cps):
            en=min(en,nominal[j+1]-addition_safety_s)
        yy=y[(t>=st)&(t<=en)]
        if len(yy)<5: raise ValueError(f"Plateau {j} too short after chronology cap")
        rho=np.corrcoef(yy[:-1],yy[1:])[0,1] if len(yy)>2 else np.nan
        neff=len(yy)*(1-rho)/(1+rho) if np.isfinite(rho) and rho>-0.999 else np.nan
        means.append(np.mean(yy)); sds.append(np.std(yy,ddof=1)); rhos.append(rho); neffs.append(neff); wins.append((st,en,len(yy)))
    return {"mean":np.asarray(means),"sd":np.asarray(sds),"rho1":np.asarray(rhos),
            "neff_ar1":np.asarray(neffs),"windows":wins}
