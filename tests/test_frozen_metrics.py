
import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"src"))
from cunw_calibration.io import *
from cunw_calibration.signal import *
from cunw_calibration.models import *

def baseline():
    cfg=load_config(); t,y=load_trace(); c,pub=load_published_calibration(); nominal_t,_=load_nominal_schedule()
    cps,_,_=detect_change_points(t,y,8,30,9,90,550,.5)
    pl=extract_plateaus(t,y,cps,20,20,8,nominal_addition_times=nominal_t,addition_safety_s=1.0)
    return c,pub,cps,pl

def test_change_points():
    _,_,cps,_=baseline()
    assert np.allclose(cps,[111,165,213,263,319,365,411,462,514])

def test_reconstruction_rmse():
    _,pub,_,pl=baseline()
    assert abs(np.sqrt(np.mean((pl["mean"]-pub)**2))-.6255)<.01

def test_fixed_segmented_slopes():
    c,_,_,pl=baseline()
    b=fit_fixed_segmented(c,pl["mean"],500)["params"]
    assert abs(b[1]-.2368051)<1e-5
    assert abs((b[1]+b[2])-.0151276)<1e-5
    assert abs(b[1]/(b[1]+b[2])-15.6539)<.02

def test_forward_loco_fixed():
    c,_,_,pl=baseline()
    _,e=forward_loco(c,pl["mean"],"Fixed-knot segmented")
    assert abs(np.sqrt(np.mean(e**2))-8.3863)<.05
