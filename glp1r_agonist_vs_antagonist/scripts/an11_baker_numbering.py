"""Check of the Baker et al. hotspot numbering: is 'GLP1R Leu95 / GIPR Met32' the 1-based index of the
resolved receptor chain (truncated target) rather than the UniProt number?  Needs work/pdb/*.cif."""
import warnings; warnings.filterwarnings("ignore")
from Bio.PDB import MMCIFParser
from Bio.SeqUtils import seq1
TESTS = {"GLP1R": (["5VAI", "6X18", "7DUQ", "6VCB"], "R", [95], "L"),
         "GIPR":  (["7FIN"], "R", [32], "M")}
for name, (ids, chain, idxs, expect) in TESTS.items():
    for pid in ids:
        m = MMCIFParser(QUIET=True).get_structure(pid, f"work/pdb/{pid}.cif")[0]
        rs = [r for r in m[chain] if r.id[0] == " " and "CA" in r]
        seq = "".join(seq1(r.resname) for r in rs)
        print(name, pid, [(i, seq[i - 1], rs[i - 1].id[1]) for i in idxs], "expected", expect)
