import json, urllib.request
ids = json.load(open("work/glp1r_ids.json"))
gql = """
query($ids:[String!]!){ entries(entry_ids:$ids){
  rcsb_id
  struct{title}
  exptl{method}
  rcsb_entry_info{resolution_combined experimental_method}
  rcsb_accession_info{initial_release_date}
  rcsb_primary_citation{title pdbx_database_id_DOI pdbx_database_id_PubMed journal_abbrev year rcsb_authors}
  polymer_entities{ rcsb_polymer_entity{pdbx_description} entity_poly{pdbx_seq_one_letter_code_can rcsb_entity_polymer_type} rcsb_polymer_entity_container_identifiers{auth_asym_ids} rcsb_entity_source_organism{ncbi_scientific_name}}
  nonpolymer_entities{ pdbx_entity_nonpoly{comp_id name} }
}}"""
req = urllib.request.Request("https://data.rcsb.org/graphql", data=json.dumps({"query":gql,"variables":{"ids":ids}}).encode(), headers={"Content-Type":"application/json"})
r = json.load(urllib.request.urlopen(req, timeout=120))
json.dump(r, open("work/glp1r_pdb_details.json","w"))
for e in r["data"]["entries"]:
    cit = e.get("rcsb_primary_citation") or {}
    res = (e["rcsb_entry_info"].get("resolution_combined") or [None])[0]
    pol = "; ".join(p["rcsb_polymer_entity"]["pdbx_description"] for p in e["polymer_entities"])
    npl = ", ".join(n["pdbx_entity_nonpoly"]["comp_id"] for n in (e.get("nonpolymer_entities") or []))
    print(f'{e["rcsb_id"]} | {e["exptl"][0]["method"]} | {res} | {e["rcsb_accession_info"]["initial_release_date"][:10]} | {e["struct"]["title"]} | pubmed={cit.get("pdbx_database_id_PubMed")} {cit.get("journal_abbrev")} {cit.get("year")} | POL: {pol[:200]} | NP: {npl}')
