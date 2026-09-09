
import numpy as np
from scipy.stats import f as f_dist
from .models import fit_fixed_segmented,fit_free_segmented
def profile_breakpoint(c,y,bounds=(100,1500),grid_points=3000,alpha=0.05):
    c=np.asarray(c,float); y=np.asarray(y,float); ks=np.linspace(bounds[0],bounds[1],grid_points); rss=[]
    for k in ks:
        X=np.column_stack([np.ones_like(c),c,np.maximum(0,c-k)]); b=np.linalg.lstsq(X,y,rcond=None)[0]
        rss.append(np.sum((y-X@b)**2))
    rss=np.asarray(rss); imin=int(np.argmin(rss)); rmin=float(rss[imin]); dof=max(1,len(c)-4)
    crit=rmin*(1+f_dist.ppf(1-alpha,1,dof)/dof); inside=ks[rss<=crit]
    return {"knot_best":float(ks[imin]),"support_low":float(inside.min()),"support_high":float(inside.max()),
            "rss_min":rmin,"grid_knot":ks,"grid_rss":rss,"critical_rss":crit}
def wild_bootstrap_slope_ratio(c,y,knot=500,n_boot=20000,seed=20260909):
    fit=fit_fixed_segmented(c,y,knot); yhat=fit["predict"](c); resid=y-yhat; rng=np.random.default_rng(seed); q=[]
    for _ in range(n_boot):
        yb=yhat+resid*rng.choice([-1.,1.],size=len(c)); fb=fit_fixed_segmented(c,yb,knot); b=fb["params"]
        low=b[1]; high=b[1]+b[2]
        if low>0 and high>0:q.append(low/high)
    q=np.asarray(q)
    return {"samples":q,"median":float(np.median(q)),"q2_5":float(np.percentile(q,2.5)),"q97_5":float(np.percentile(q,97.5))}
def jackknife_fixed_and_knot(c,y,knot=500,bounds=(100,1500)):
    out=[]
    for i in range(len(c)):
        keep=np.arange(len(c))!=i; ff=fit_fixed_segmented(c[keep],y[keep],knot); b=ff["params"]
        fk=fit_free_segmented(c[keep],y[keep],bounds); out.append((c[i],b[1],b[1]+b[2],b[1]/(b[1]+b[2]),fk["knot"]))
    return out
