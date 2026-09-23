from pathlib import Path
from PIL import Image, ImageDraw
import shutil

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"outputs"/"figures"
OUT_MAIN=ROOT/"outputs"/"submission_figures"/"main"
OUT_SUPP=ROOT/"outputs"/"submission_figures"/"supplementary"
OUT_MAIN.mkdir(parents=True,exist_ok=True)
OUT_SUPP.mkdir(parents=True,exist_ok=True)

def composite(paths,out,gap=30,pad=30):
    imgs=[Image.open(p).convert("RGB") for p in paths]
    labels=[f"({chr(97+i)})" for i in range(len(imgs))]
    H=max(im.height for im in imgs)
    norm=[]
    for im in imgs:
        if im.height!=H:
            im=im.resize((round(im.width*H/im.height),H),Image.Resampling.LANCZOS)
        norm.append(im)
    W=sum(im.width for im in norm)+gap*(len(norm)-1)+2*pad
    canvas=Image.new("RGB",(W,H+2*pad),"white")
    x=pad
    d=ImageDraw.Draw(canvas)
    for lab,im in zip(labels,norm):
        canvas.paste(im,(x,pad))
        d.text((x+12,pad+10),lab,fill="black")
        x+=im.width+gap
    canvas.save(out,dpi=(300,300))

# Data-derived submission figures
composite([SRC/"Figure2a_raw_trace_reconstruction.png",SRC/"Figure2b_extracted_vs_published.png"],OUT_MAIN/"Figure_2.png")
composite([SRC/"Figure3a_model_comparison.png",SRC/"Figure3b_breakpoint_profile.png"],OUT_MAIN/"Figure_3.png")
shutil.copy2(SRC/"Figure4_inverse_LOCO_all_models.png",OUT_MAIN/"Figure_4.png")
shutil.copy2(SRC/"Figure5_inverse_sensitivity.png",OUT_MAIN/"Figure_5.png")
composite([SRC/"Figure6a_breakpoint_identifiability.png",SRC/"FigureS9_validation_hierarchy.png"],OUT_MAIN/"Figure_6.png")

mapping={
"FigureS1_parameter_grid.png":"Figure_S1.png",
"FigureS2_breakpoint_grid.png":"Figure_S2.png",
"FigureS3_jackknife_ratio.png":"Figure_S3.png",
"FigureS4_jackknife_breakpoint.png":"Figure_S4.png",
"Figure4_inverse_LOCO_all_models.png":"Figure_S6.png",
"FigureS7_model_recovery_sparse.png":"Figure_S7.png",
"FigureS7_model_recovery_dense.png":"Figure_S8.png",
"FigureS9_validation_hierarchy.png":"Figure_S9.png",
}
for src,dst in mapping.items():
    shutil.copy2(SRC/src,OUT_SUPP/dst)

# Main Figure 1 (conceptual workflow) and Supplementary Figure S5
# (supporting electrochemistry composite) are supplied separately as static
# source assets in the manuscript submission package.
print("Data-derived submission figures assembled.")
