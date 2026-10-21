"""Solvent exposure (Shrake-Rupley, probe 1.4 A, relative to max ASA) of the reconstructed Baker hotspots in the isolated ECD,
plus UniProt-vs-model sequence differences in the 5VAI receptor ECD. Needs work/pdb/{5VAI,6X18,7DUQ,7FIN}.cif, network for UniProt."""
import warnings, urllib.request; warnings.filterwarnings("ignore")
from Bio.PDB import MMCIFParser, ShrakeRupley
from Bio.SeqUtils import seq1
MAXASA = {'ALA':129,'ARG':274,'ASN':195,'ASP':193,'CYS':167,'GLN':225,'GLU':223,'GLY':104,'HIS':224,'ILE':197,'LEU':201,'LYS':236,'MET':224,'PHE':240,'PRO':159,'SER':155,'THR':172,'TRP':285,'TYR':263,'VAL':174}
def ecd(pid, chain, lo, hi):
    m = MMCIFParser(QUIET=True).get_structure(pid, f"work/pdb/{pid}.cif")[0]; ch = m[chain]
    for r in list(ch):
        if r.id[0] != " " or not (lo <= r.id[1] <= hi): ch.detach_child(r.id)
    for c in list(m):
        if c.id != chain: m.detach_child(c.id)
    ShrakeRupley(probe_radius=1.4, n_points=200).compute(m, level="R")
    return {r.id[1]: (r.resname, r.sasa / MAXASA.get(r.resname, 200)) for r in ch}
for pid, lo, hi in (("6X18", 29, 128), ("7DUQ", 29, 128), ("5VAI", 29, 140)):
    g = ecd(pid, "R", lo, hi); hyd = sorted([v[1] for v in g.values() if v[0] in ("LEU","ILE","VAL","MET","PHE","TRP","TYR")], reverse=True)
    print(pid, "L123 %.2f rank %d/%d | L118 %s" % (g[123][1], 1 + sum(y > g[123][1] for y in hyd), len(hyd), round(g[118][1], 2) if 118 in g else "n/a"))
gi = ecd("7FIN", "R", 30, 140); print("7FIN M67 %.2f" % gi[67][1])
U = "".join(urllib.request.urlopen("https://rest.uniprot.org/uniprotkb/P43220.fasta", timeout=60).read().decode().split("\n")[1:])
m = MMCIFParser(QUIET=True).get_structure("x", "work/pdb/5VAI.cif")[0]
print("5VAI R ECD residues differing from UniProt:", [(n, seq1(r.resname), U[n-1]) for r in m["R"] if r.id[0] == " " and 29 <= (n := r.id[1]) <= 140 and seq1(r.resname) != U[n-1]])
