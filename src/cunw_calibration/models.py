
import numpy as np
from scipy.optimize import least_squares,minimize_scalar
def fit_linear(c,y):
    c=np.asarray(c,float); y=np.asarray(y,float)
    X=np.column_stack([np.ones_like(c),c]); b=np.linalg.lstsq(X,y,rcond=None)[0]
    return {"params":b,"predict":lambda x:b[0]+b[1]*np.asarray(x,float)}
def fit_fixed_segmented(c,y,knot=500.0):
    c=np.asarray(c,float); y=np.asarray(y,float)
    X=np.column_stack([np.ones_like(c),c,np.maximum(0,c-knot)]); b=np.linalg.lstsq(X,y,rcond=None)[0]
    return {"params":b,"knot":float(knot),"predict":lambda x:b[0]+b[1]*np.asarray(x,float)+b[2]*np.maximum(0,np.asarray(x,float)-knot)}
def fit_free_segmented(c,y,knot_bounds=(100.0,1500.0)):
    c=np.asarray(c,float); y=np.asarray(y,float)
    def sse(k):
        X=np.column_stack([np.ones_like(c),c,np.maximum(0,c-k)])
        b=np.linalg.lstsq(X,y,rcond=None)[0]; return float(np.sum((y-X@b)**2))
    r=minimize_scalar(sse,bounds=knot_bounds,method="bounded"); k=float(r.x)
    X=np.column_stack([np.ones_like(c),c,np.maximum(0,c-k)]); b=np.linalg.lstsq(X,y,rcond=None)[0]
    return {"params":b,"knot":k,"predict":lambda x:b[0]+b[1]*np.asarray(x,float)+b[2]*np.maximum(0,np.asarray(x,float)-k)}
def fit_langmuir(c,y):
    c=np.asarray(c,float); y=np.asarray(y,float); p0=[max(0,float(y.min())-5),float(y.max()-y.min()+20),500.]
    def pred(p,x):
        x=np.asarray(x,float); return p[0]+p[1]*x/(p[2]+x)
    r=least_squares(lambda p:pred(p,c)-y,p0,bounds=([-100,0,1e-6],[500,1000,1e5]),max_nfev=100000)
    p=r.x; return {"params":p,"predict":lambda x:pred(p,x)}
def fit_hill(c,y):
    c=np.asarray(c,float); y=np.asarray(y,float); p0=[max(0,float(y.min())-5),float(y.max()-y.min()+20),500.,1.]
    def pred(p,x):
        x=np.asarray(x,float); z=(x/p[2])**p[3]; return p[0]+p[1]*z/(1+z)
    r=least_squares(lambda p:pred(p,c)-y,p0,bounds=([-100,0,1e-3,0.1],[500,1000,1e5,5]),max_nfev=100000)
    p=r.x; return {"params":p,"predict":lambda x:pred(p,x)}
FITTERS={"Single linear":fit_linear,"Fixed-knot segmented":fit_fixed_segmented,
         "Free-knot segmented":fit_free_segmented,"Langmuir":fit_langmuir,"Hill":fit_hill}
PARAM_COUNT={"Single linear":2,"Fixed-knot segmented":3,"Free-knot segmented":4,"Langmuir":3,"Hill":4}
def r2(y,yhat):
    y=np.asarray(y,float); yhat=np.asarray(yhat,float)
    return 1-np.sum((y-yhat)**2)/np.sum((y-y.mean())**2)
def aicc(y,yhat,k):
    y=np.asarray(y,float); yhat=np.asarray(yhat,float); n=len(y); rss=max(float(np.sum((y-yhat)**2)),1e-300)
    return n*np.log(rss/n)+2*k+2*k*(k+1)/(n-k-1)
def inverse_predict(model,fit,current):
    y=float(current)
    if model=="Single linear":
        b=fit["params"]; return (y-b[0])/b[1]
    if model in ("Fixed-knot segmented","Free-knot segmented"):
        b=fit["params"]; k=fit["knot"]; Ik=b[0]+b[1]*k
        if y<=Ik: return (y-b[0])/b[1]
        return (y-(b[0]-b[2]*k))/(b[1]+b[2])
    if model=="Langmuir":
        I0,A,K=fit["params"]; num=y-I0; den=I0+A-y
        return np.nan if num<=0 or den<=0 else K*num/den
    if model=="Hill":
        I0,A,K,n=fit["params"]; num=y-I0; den=I0+A-y
        return np.nan if num<=0 or den<=0 else K*(num/den)**(1/n)
def forward_loco(c,y,model):
    preds=[]; errs=[]; fitter=FITTERS[model]
    for j in range(len(c)):
        keep=np.arange(len(c))!=j; fit=fitter(c[keep],y[keep]); p=float(fit["predict"]([c[j]])[0])
        preds.append(p); errs.append(p-y[j])
    return np.asarray(preds),np.asarray(errs)
def inverse_loco(c,y,model):
    preds=[]; fitter=FITTERS[model]
    for j in range(len(c)):
        keep=np.arange(len(c))!=j; fit=fitter(c[keep],y[keep]); preds.append(inverse_predict(model,fit,y[j]))
    return np.asarray(preds,float)
