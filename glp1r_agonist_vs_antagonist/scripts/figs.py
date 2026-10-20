import numpy as np, warnings, sys, json
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
import an1
from an2 import load, aa
from an4 import cadict, superpose_core, REF, INA
BG="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; GRID="#e6e5e0"; C1="#2a78d6"; C2="#eb6834"
rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.edgecolor":INK2,"axes.labelcolor":INK2,"xtick.color":INK2,"ytick.color":INK2,"text.color":INK})

# ---- Fig 1: per-residue burial of GLP-1(7-36) in 6X18
m=an1.load("6X18"); rows=an1.interface(m,"P","R")
res=[r[0] for r in rows]; nm=[r[1] for r in rows]; be=np.array([r[3] for r in rows]); bt=np.array([r[4] for r in rows])
one={'HIS':'H','ALA':'A','GLU':'E','GLY':'G','THR':'T','PHE':'F','SER':'S','ASP':'D','VAL':'V','TYR':'Y','LEU':'L','GLN':'Q','LYS':'K','ILE':'I','TRP':'W','ARG':'R'}
lab=[f"{one[n]}{r}" for n,r in zip(nm,res)]
fig,ax=plt.subplots(figsize=(10,4.2),dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
x=np.arange(len(res)); w=0.8
ax.bar(x,bt,w,color=C2,label="Buried by TMD + extracellular loops (receptor residues > 137)",edgecolor=BG,linewidth=1)
ax.bar(x,be,w,bottom=bt,color=C1,label="Buried by ECD (receptor residues 29–137)",edgecolor=BG,linewidth=1)
# bars are overlapping-by-definition (non-additive) -> draw side by side instead
ax.cla(); ax.set_facecolor(BG)
ax.bar(x-0.2,bt,0.38,color=C2,label="by TMD + extracellular loops (receptor residues > 137)")
ax.bar(x+0.2,be,0.38,color=C1,label="by ECD (receptor residues 29–137)")
ax.set_xticks(x); ax.set_xticklabels(lab,rotation=90,fontsize=8)
ax.set_ylabel("Buried surface of the residue, Å²")
ax.yaxis.grid(True,color=GRID,linewidth=0.8); ax.set_axisbelow(True)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.axvspan(-0.6,10.5,color=C2,alpha=0.07,lw=0); ax.axvspan(16.5,len(res)-0.4,color=C1,alpha=0.07,lw=0)
ax.text(5,188,"N-terminal module 7–17\n≈ 890 Å² on TMD/ECL, 0 contacts with ECD",ha="center",va="top",fontsize=9,color=INK)
ax.text(23.6,188,"C-terminal helix 24–36 in the ECD groove\n≈ 530 Å² on ECD",ha="center",va="top",fontsize=9,color=INK)
ax.set_ylim(0,195)
ax.legend(loc="upper center",bbox_to_anchor=(0.5,-0.28),ncol=2,frameon=False,fontsize=9)
ax.set_title("GLP-1(7–36) in the active GLP-1R–Gs complex (PDB 6X18): which receptor domain buries which peptide residue",fontsize=10.5,loc="left",color=INK)
fig.tight_layout(); fig.savefig("figs/fig1_burial_6X18.png",facecolor=BG); plt.close(fig)
json.dump({"res":res,"label":lab,"bur_ecd":be.round(1).tolist(),"bur_tmd":bt.round(1).tolist()},open("work/fig1_data.json","w"))

# ---- Fig 2: CA displacement inactive(6LN2) -> active(6X18)
act=load("6X18"); ina=load("6LN2")
A=cadict(act,"R"); B=cadict(ina,"A")
R,t,nc,rm=superpose_core(B,A)
common=sorted(set(A)&set(B))
d=np.array([np.linalg.norm(B[n]@R.T+t-A[n]) for n in common])
fig,ax=plt.subplots(figsize=(10,3.8),dpi=200); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
cn=np.array(common)
col=np.where(cn<=137,C1,C2)
ax.vlines(cn,0,d,color=col,linewidth=1.6)
ax.set_xlabel("GLP-1R residue (UniProt P43220 numbering)"); ax.set_ylabel("Cα displacement, Å")
ax.yaxis.grid(True,color=GRID,linewidth=0.8); ax.set_axisbelow(True)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.annotate("ECD: centroid moves 16 Å\n(closed → open)",xy=(85,np.mean(d[cn<=137])),xytext=(60,34.5),fontsize=9,ha="center",va="bottom",color=INK,arrowprops=dict(arrowstyle="-",color=INK2,lw=0.8))
ax.annotate("ECL1 / top of TM2–TM3\nup to 15.5 Å (res 215)",xy=(215,15.5),xytext=(185,28),fontsize=9,ha="center",color=INK,arrowprops=dict(arrowstyle="-",color=INK2,lw=0.8))
ax.annotate("TM6 intracellular end:\nres 346 moves 18.7 Å",xy=(346,18.7),xytext=(335,29),fontsize=9,ha="center",color=INK,arrowprops=dict(arrowstyle="-",color=INK2,lw=0.8))
ax.set_ylim(0,40)
ax.set_title("Inactive full-length GLP-1R (6LN2, closed ECD) → active GLP-1–Gs complex (6X18), TMD core superposed (145 Cα, RMSD 1.2 Å)",fontsize=10,loc="left")
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0],[0],color=C1,lw=2,label="ECD (29–137)"),Line2D([0],[0],color=C2,lw=2,label="TMD + loops (> 137)")],loc="upper right",frameon=False,fontsize=9)
fig.tight_layout(); fig.savefig("figs/fig2_inactive_to_active.png",facecolor=BG); plt.close(fig)
print("ok", len(common), d.max(), "ECD mean",d[cn<=137].mean())
