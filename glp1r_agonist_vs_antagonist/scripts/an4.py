import numpy as np, warnings, sys, json
warnings.filterwarnings("ignore")
sys.path.insert(0,'.')
import gemmi
from an2 import *
TM1="LFLYIIYTVGYALSF"
def find_chains(pid):
    st=gemmi.read_structure(f"work/pdb/{pid}.cif"); m=st[0]
    rec=None; peps=[]
    for ch in m:
        poly=ch.get_polymer()
        if len(poly)==0: continue
        seq=gemmi.one_letter_code([r.name for r in poly])
        if TM1 in seq or "ELTFYLQRG" in seq: 
            if rec is None or len(poly)>rec[1]: rec=(ch.name,len(poly))
        elif 8<=len(poly)<=45 and "QVQLV" not in seq: peps.append((ch.name,len(poly),seq[:40]))
    return rec, peps
def kabsch(A,B):
    ca_,cb=A.mean(0),B.mean(0); H=(A-ca_).T@(B-cb); U,S,Vt=np.linalg.svd(H); d=np.sign(np.linalg.det(Vt.T@U.T))
    R=Vt.T@np.diag([1,1,d])@U.T; return R, cb-R@ca_
def cadict(model,chain):
    return {r.id[1]:r['CA'].coord.copy() for r in aa(model[chain]) if 'CA' in r}
REF=cadict(load("6X18"),"R")
INA=cadict(load("6LN2"),"A")
def superpose_core(X, ref, lo=143, hi=400):
    common=[n for n in X if n in ref and lo<=n<=hi]
    core=common
    for it in range(12):
        A=np.array([X[n] for n in core]); B=np.array([ref[n] for n in core])
        R,t=kabsch(A,B); d=np.linalg.norm(A@R.T+t-B,axis=1)
        keep=[n for n,dd in zip(core,d) if dd<3.0]
        if len(keep)==len(core) or len(keep)<30: break
        core=keep
    return R,t,len(core),float(np.sqrt((d**2).mean()))
def analyse(pid, rchain, pchain=None, het=None):
    m=load(pid); X=cadict(m,rchain)
    R,t,nc,rm=superpose_core(X,REF)
    # state descriptors in 6X18 frame
    def disp_to(ref,n): return np.linalg.norm(X[n]@R.T+t-ref[n]) if n in X and n in ref else np.nan
    # distance of TM6 intracellular (346) and ECD centroid compared to active (6X18) vs inactive(6LN2 aligned onto 6X18)
    # inactive ref in 6X18 frame
    Ri,ti,_,_=superpose_core(INA,REF)
    INA_f={n:INA[n]@Ri.T+ti for n in INA}
    def dd(n,ref): 
        return np.linalg.norm(X[n]@R.T+t-ref[n]) if (n in X and n in ref) else np.nan
    res=dict(pid=pid,core=nc,rmsd=round(rm,2))
    for lab,n in (("TM6_346",346),("ECL1_215",215)):
        res[lab+"_to_active"]=round(dd(n,REF),1); res[lab+"_to_inactive"]=round(dd(n,INA_f),1)
    ecd=[n for n in X if n<=130 and n in REF]
    if ecd:
        cx=np.mean([X[n]@R.T+t for n in ecd],axis=0); ca=np.mean([REF[n] for n in ecd],axis=0); ci=np.mean([INA_f[n] for n in ecd if n in INA_f],axis=0)
        res["ECD_to_active"]=round(float(np.linalg.norm(cx-ca)),1); res["ECD_to_inactive"]=round(float(np.linalg.norm(cx-ci)),1)
    # ligand burial
    rec=aa(m[rchain]); E=[r for r in rec if r.id[1]<=137]; T=[r for r in rec if r.id[1]>137]
    lig=[]
    if pchain: lig+= aa(m[pchain])
    if het:
        for ch in m:
            for r in ch:
                if r.get_resname()==het: lig.append(r)
    if lig:
        def bur(lig, partner):
            # burial of ligand by partner, ligand residues all in group T (ids preserved & unique?)
            ids=[(r.get_resname(), r.id) for r in lig]
            s=Structure("t"); mm=Model(0); s.add(mm); c=Chain("T"); mm.add(c)
            for i,r in enumerate(lig):
                rr=r.copy(); rr.id=(' ',i+1,' '); c.add(rr)
            ShrakeRupley(probe_radius=1.4,n_points=200).compute(s,level="R"); a=sum(r.sasa for r in c)
            o=Chain("O"); mm.add(o)
            for i,r in enumerate(partner):
                rr=r.copy(); rr.id=(' ',i+1,' '); o.add(rr)
            ShrakeRupley(probe_radius=1.4,n_points=200).compute(s,level="R"); b=sum(r.sasa for r in c)
            return a-b, a
        be,a=bur(lig,E); bt,_=bur(lig,T)
        res["lig_free_SASA"]=round(a); res["bur_ECD"]=round(be); res["bur_TMD"]=round(bt)
        # ligand centroid in 6X18 frame and distance to GLP-1 His7 CA & F28 CA
        xyz=np.array([at.coord for r in lig for at in r if at.element!='H'])
        cen=xyz.mean(0)@R.T+t
        res["cent_to_H7"]=round(float(np.linalg.norm(cen-REF[None] if False else cen-np.array(ref_h7))),1)
    return res
m18=load("6X18"); ref_h7=m18["P"][7]['CA'].coord.copy()
CASES=[("6X18","R","P",None),("7KI0","R","P",None),("7FIM","R","P",None),("7LLL","R","P",None),("6B3J","R","P",None),
 ("9IVG","R","P",None),("6VCB","R","P","QW7"),("6X1A","R",None,"UK4"),("6X19","R",None,"UK1"),("6XOX","R",None,"V6G"),
 ("7S15","R",None,"82L"),("7RG9","R",None,None),("8WG7","R",None,None),("7C2E","R",None,"FFR"),("7X8R","R",None,"BYI")]
if __name__=="__main__":
    for pid,rc,pc,het in CASES:
        try:
            r=analyse(pid,rc,pc,het); print(json.dumps(r))
        except Exception as e: print(pid,"ERR",repr(e))
