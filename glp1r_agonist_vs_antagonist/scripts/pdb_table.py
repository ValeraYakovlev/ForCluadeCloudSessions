import json
r = json.load(open("work/glp1r_pdb_details.json"))
skip = ("Guanine","Nanobody","nanobody","Single-chain","scFv","Endolysin","Rubredoxin")
rows=[]
for e in r["data"]["entries"]:
    if e is None: continue
    cit = e.get("rcsb_primary_citation") or {}
    res = ((e.get("rcsb_entry_info") or {}).get("resolution_combined") or [None])[0]
    date = ((e.get("rcsb_accession_info") or {}).get("initial_release_date") or "")[:10]
    pols = [p["rcsb_polymer_entity"]["pdbx_description"] for p in e["polymer_entities"]]
    pols = [p for p in pols if not p.startswith(skip) and "Glucagon-like peptide 1 receptor" not in p and "Glucagon-like peptide-1 receptor" not in p]
    npl = ", ".join(n["pdbx_entity_nonpoly"]["comp_id"]+"="+(n["pdbx_entity_nonpoly"]["name"] or "") for n in (e.get("nonpolymer_entities") or []) if n["pdbx_entity_nonpoly"]["comp_id"] not in ("NAG","CLR","OLC","OLA","PLM","Y01","SOG","HOH","NA","ZN","CLA","PEG","GOL"))
    meth = e["exptl"][0]["method"] if e.get("exptl") else ""
    rows.append(f'{e["rcsb_id"]}\t{meth[:8]}\t{res}\t{date}\t{e["struct"]["title"]}\tPM{cit.get("pdbx_database_id_PubMed")}\t{cit.get("journal_abbrev")} {cit.get("year")}\t{"; ".join(pols)}\t{npl}')
open("work/glp1r_pdb_table.tsv","w").write("\n".join(rows))
print(len(rows))
