import numpy as np, warnings, sys
warnings.filterwarnings("ignore")
sys.path.insert(0,'.')
from an2 import *
# --- Fab 3F52 epitope vs ligand groove
m=load("5E94"); E=aa(m["G"]); F=aa(m["A"])+aa(m["B"])
bF,_=buried_by(E,F)
fab=set(n for n,v in bF.items() if v>10)
m2=load("3IOL"); R=aa(m2["A"]); L=aa(m2["B"]); bG,_=buried_by(R,L); glp=set(n for n,v in bG.items() if v>10)
m3=load("3C5T"); R3=aa(m3["A"]); L3=aa(m3["B"]); bX,_=buried_by(R3,L3); ex=set(n for n,v in bX.items() if v>10)
print("Fab3F52 epitope residues (>10A2):",sorted(fab)); print("  n=",len(fab))
print("GLP-1 groove (3IOL):",sorted(glp)); print("Ex4(9-39) groove (3C5T):",sorted(ex))
print("overlap Fab&GLP-1:",sorted(fab&glp)," frac of GLP-1 groove covered by Fab epitope: %.2f"%(len(fab&glp)/len(glp)))
print("overlap Fab&Ex4:",sorted(fab&ex)," frac %.2f"%(len(fab&ex)/len(ex)))
tot_fab=sum(v for n,v in bF.items()); print("Fab buries ECD total %.0f A2"%tot_fab)

# --- superposition of 6LN2 (inactive, ECD closed) onto 6X18 (active)
def ca(model, chain, lo, hi):
    d={}
    for r in aa(model[chain]):
        if lo<=r.id[1]<=hi and 'CA' in r: d[r.id[1]]=r['CA'].coord.copy()
    return d
def kabsch(A,B):
    ca_,cb=A.mean(0),B.mean(0); H=(A-ca_).T@(B-cb); U,S,Vt=np.linalg.svd(H); d=np.sign(np.linalg.det(Vt.T@U.T))
    D=np.diag([1,1,d]); R=Vt.T@D@U.T; return R, cb-R@ca_
act=load("6X18"); ina=load("6LN2")
A=ca(act,"R",29,423); B=ca(ina,"A",29,423)
common=sorted(set(A)&set(B)); print("\ncommon CA residues 6X18/6LN2:",len(common))
# TMD residues 143..400 core with iterative outlier rejection
core=[n for n in common if 143<=n<=400]
for it in range(10):
    X=np.array([B[n] for n in core]); Y=np.array([A[n] for n in core])
    R,t=kabsch(X,Y); d=np.linalg.norm((X@R.T+t)-Y,axis=1)
    keep=[n for n,dd in zip(core,d) if dd<3.0]
    if len(keep)==len(core): break
    core=keep
print("core residues used:",len(core),"RMSD %.2f"%np.sqrt((d**2).mean()))
disp={n:np.linalg.norm(B[n]@R.T+t-A[n]) for n in common}
def rng(lo,hi): 
    v=[disp[n] for n in common if lo<=n<=hi]; return np.mean(v),np.max(v)
print("ECD (29-137)  mean/max Calpha displacement: %.1f / %.1f A"%rng(29,137))
# centroid shift of ECD
ecdA=np.mean([A[n] for n in common if n<=130],axis=0); ecdB=np.mean([B[n]@R.T+t for n in common if n<=130],axis=0)
print("ECD centroid shift (inactive->active): %.1f A"%np.linalg.norm(ecdA-ecdB))
# print displaced segments > 4 A
seg=[];cur=[]
for n in common:
    if n>=138 and disp[n]>4.0:
        if cur and n-cur[-1]>2: seg.append(cur);cur=[]
        cur.append(n)
if cur: seg.append(cur)
print("TMD segments with Calpha displacement >4 A (inactive->active):")
for s in seg: print("  %d-%d  max %.1f A (res %d)"%(s[0],s[-1],max(disp[n] for n in s),max(s,key=lambda n:disp[n])))
