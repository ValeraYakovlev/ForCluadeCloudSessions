import numpy as np, warnings, sys
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from an4 import *
# 1) independent inactive-state references: TM6 residue 346 shift vs 6X18
for pid in ("6LN2","5VEW","5VEX","6KJV","6KK1","6KK7"):
    m=load(pid)
    ch=[c.id for c in m if len(aa(c))>150][0]
    X={r.id[1]:r['CA'].coord.copy() for r in aa(m[ch]) if 'CA' in r and r.id[1]<=430}
    R,t,nc,rm=superpose_core(X,REF)
    d346=np.linalg.norm(X[346]@R.T+t-REF[346]) if 346 in X else float('nan')
    d215=np.linalg.norm(X[215]@R.T+t-REF[215]) if 215 in X else float('nan')
    print(f"{pid} chain {ch}: core {nc} rmsd {rm:.2f}; CA346 shift vs 6X18 {d346:.1f} A; CA215 {d215:.1f} A")
# 2) sensitivity of ECD/TMD burial to ECD boundary and SASA resolution
import an1
from Bio.PDB import ShrakeRupley
m=load("6X18")
for hi in (130,137,145):
    rows=an1.interface(m,"P","R",ecd_hi=hi)
    be=sum(r[3] for r in rows); bt=sum(r[4] for r in rows); ba=sum(r[5] for r in rows)
    n_nt=sum(r[3] for r in rows if r[0]<=17)
    print(f"ECD boundary <= {hi}: bur_ECD {be:.0f}  bur_TMD {bt:.0f}  all {ba:.0f}; residues 7-17 ECD burial {n_nt:.1f}; ECD fraction {be/ba:.2f}")
