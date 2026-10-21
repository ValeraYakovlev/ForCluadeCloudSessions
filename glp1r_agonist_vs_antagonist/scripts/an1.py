import numpy as np, warnings
warnings.filterwarnings("ignore")
from Bio.PDB import MMCIFParser, ShrakeRupley, NeighborSearch
from Bio.PDB.Structure import Structure
from Bio.PDB.Model import Model
import copy

P = MMCIFParser(QUIET=True)
def load(pid): return P.get_structure(pid, f"work/pdb/{pid}.cif")[0]

def sasa_of(atoms_residues, probe=1.4):
    """SASA per residue for a list of residues placed in a fresh model (no hetero water)."""
    s = Structure("t"); m = Model(0); s.add(m)
    from Bio.PDB.Chain import Chain
    c = Chain("X"); m.add(c)
    for r in atoms_residues:
        c.add(r.copy())
    sr = ShrakeRupley(probe_radius=probe, n_points=200)
    sr.compute(s, level="R")
    return {r.id: r.sasa for r in c}

def aa_res(chain, lo=None, hi=None):
    out=[]
    for r in chain:
        if r.id[0]!=' ': continue
        n=r.id[1]
        if lo is not None and n<lo: continue
        if hi is not None and n>hi: continue
        out.append(r)
    return out

def interface(model, pep_chain, rec_chain, ecd_hi=137, pep_lo=None):
    pep = aa_res(model[pep_chain]); rec = aa_res(model[rec_chain])
    ecd = [r for r in rec if r.id[1]<=ecd_hi]; tmd=[r for r in rec if r.id[1]>ecd_hi]
    # SASA of peptide alone, with ECD, with TMD, with all rec
    # compute in a combined structure but we need unique residue ids -> use list-of-residue approach with chain-specific renumbering
    def comb(pep, others):
        s = Structure("t"); m = Model(0); s.add(m)
        from Bio.PDB.Chain import Chain
        cp = Chain("P"); m.add(cp)
        for r in pep: cp.add(r.copy())
        if others:
            co = Chain("O"); m.add(co)
            for i,r in enumerate(others):
                rr = r.copy(); rr.id=(' ',i+1,' '); co.add(rr)
        sr = ShrakeRupley(probe_radius=1.4, n_points=200); sr.compute(s, level="R")
        return {r.id[1]: r.sasa for r in cp}
    a = comb(pep, []); e = comb(pep, ecd); t = comb(pep, tmd); al = comb(pep, rec)
    rows=[]
    ns_ecd = NeighborSearch([at for r in ecd for at in r])
    ns_tmd = NeighborSearch([at for r in tmd for at in r])
    for r in pep:
        n=r.id[1]
        def cont(ns):
            res=set()
            for at in r:
                for nb in ns.search(at.coord, 4.0, 'R'): res.add(nb.id[1])
            return sorted(res)
        ce, ct = cont(ns_ecd), cont(ns_tmd)
        rows.append((n, r.get_resname(), a[n], a[n]-e[n], a[n]-t[n], a[n]-al[n], ce, ct))
    return rows

if __name__=="__main__":
    m = load("6X18")
    rows = interface(m, "P", "R")
    print("6X18 GLP-1(7-36) vs receptor (ECD<=137, TMD>137). bSASA in A^2")
    print("res name  SASAfree  bur_ECD  bur_TMD  bur_all   nECDcontacts nTMDcontacts  TMDresidues")
    tot=[0,0,0]
    for n,nm,a,be,bt,ba,ce,ct in rows:
        print(f"{n:3d} {nm} {a:8.1f} {be:7.1f} {bt:7.1f} {ba:7.1f}   {len(ce):2d} {len(ct):2d}   {ct if len(ct)<14 else str(ct[:14])+'...'}")
        tot[0]+=be; tot[1]+=bt; tot[2]+=ba
    print("TOTAL bur ECD %.0f TMD %.0f all %.0f"%tuple(tot))
