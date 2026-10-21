"""Independent position check of the Baker hotspots: map GCGR/GIPR hotspots onto GLP1R by ECD alignment
(BLOSUM62, global) and measure the minimum distance of the GLP1R equivalents (and Leu118/Leu123) to GLP-1 in 6X18.
Needs work/pdb/6X18.cif and network access to UniProt."""
import urllib.request, warnings; warnings.filterwarnings("ignore")
from Bio import Align
from Bio.Align import substitution_matrices
from Bio.PDB import MMCIFParser, NeighborSearch
def seq(acc):
    t = urllib.request.urlopen(f"https://rest.uniprot.org/uniprotkb/{acc}.fasta", timeout=60).read().decode()
    return "".join(t.split("\n")[1:])
G, GC, GI = seq("P43220"), seq("P47871"), seq("P48546")
al = Align.PairwiseAligner(); al.substitution_matrix = substitution_matrices.load("BLOSUM62")
al.open_gap_score = -10; al.extend_gap_score = -0.5; al.mode = "global"
def mapping(other, lo, hi):
    a = al.align(G[23:139], other[lo - 1:hi])[0]; m = {}
    for (s1, e1), (s2, e2) in zip(*a.aligned):
        for k in range(e1 - s1): m[s2 + k + lo] = s1 + k + 24
    return m
mGC, mGI = mapping(GC, 26, 136), mapping(GI, 22, 138)
st = MMCIFParser(QUIET=True).get_structure("x", "work/pdb/6X18.cif")[0]
ns = NeighborSearch(list(st["P"].get_atoms()))
def mind(rn):
    d = [float(a - b) for a in st["R"][rn] for b in ns.search(a.coord, 8.0)]
    return round(min(d), 1) if d else None
for h in (33, 36, 87):
    e = mGC[h]; print(f"GCGR {GC[h-1]}{h} -> GLP1R {G[e-1]}{e}", mind(e))
e = mGI[67]; print(f"GIPR M67 -> GLP1R {G[e-1]}{e}", mind(e))
print("GLP1R Leu123", mind(123), "Leu118", mind(118))
