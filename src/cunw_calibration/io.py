
from pathlib import Path
import csv,json
import numpy as np
REPO_ROOT=Path(__file__).resolve().parents[2]
DATA_RAW=REPO_ROOT/"data"/"raw"
DATA_DERIVED=REPO_ROOT/"data"/"derived"
OUTPUT_FIGURES=REPO_ROOT/"outputs"/"figures"
OUTPUT_TABLES=REPO_ROOT/"outputs"/"tables"

def load_config():
    return json.loads((REPO_ROOT/"config.json").read_text(encoding="utf-8"))

def read_numeric_csv(path,columns):
    rows=[]
    with open(path,newline="",encoding="utf-8") as f:
        for row in csv.DictReader(f): rows.append([float(row[c]) for c in columns])
    return np.asarray(rows,float)

def load_trace():
    a=read_numeric_csv(DATA_RAW/"fig4b_amperometric_trace.csv",["time_s","current_uA"])
    return a[:,0],a[:,1]

def load_published_calibration():
    a=read_numeric_csv(DATA_RAW/"published_calibration.csv",["concentration_uM","published_current_uA"])
    return a[:,0],a[:,1]

def load_nominal_schedule():
    a=read_numeric_csv(DATA_RAW/"nominal_dosing_schedule.csv",["nominal_time_s","cumulative_concentration_uM"])
    return a[:,0],a[:,1]

def write_csv(path,header,rows):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(header); w.writerows(rows)
