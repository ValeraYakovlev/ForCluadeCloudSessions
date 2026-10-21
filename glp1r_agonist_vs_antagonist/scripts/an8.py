import numpy as np, warnings, sys
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from an2 import *
groove=[29,30,32,35,36,39,67,68,69,88,89,90,91,121,123,128]
def sasa_res(res):
    s=Structure("t"); m=Model(0); s.add(m); c=Chain("A"); m.add(c)
    for r in res: c.add(r.copy())
    ShrakeRupley(probe_radius=1.4,n_points=300).compute(s,level="R")
    return {r.id[1]:r.sasa for r in c}
def groove_acc(label, res_all, ecd_only=False):
    full=sasa_res(res_all)
    ecd=[r for r in res_all if r.id[1]<=137]
    iso=sasa_res(ecd)
    g_full=sum(full.get(n,0) for n in groove); g_iso=sum(iso.get(n,0) for n in groove)
    print(f"{label}: groove SASA in context {g_full:.0f} A2 vs ECD-alone {g_iso:.0f} A2 -> accessible fraction {g_full/g_iso:.2f}; per-res (ctx/iso): "+" ".join(f"{n}:{full.get(n,0):.0f}/{iso.get(n,0):.0f}" for n in groove if iso.get(n,0)>5 and full.get(n,0)<0.6*iso.get(n,0)))
for pid,ch in (("6LN2","A"),("6X18","R"),("5VEW",None)):
    if ch is None: continue
    m=load(pid); res=aa(m[ch])
    if pid=="6X18":
        # remove peptide: only receptor chain
        pass
    groove_acc(pid,res)
# 5E94 chain G ECD alone vs 3IOL ECD alone sanity
m=load("3IOL"); iso=sasa_res(aa(m["A"])); print("3IOL ECD alone groove SASA %.0f"%sum(iso.get(n,0) for n in groove))
