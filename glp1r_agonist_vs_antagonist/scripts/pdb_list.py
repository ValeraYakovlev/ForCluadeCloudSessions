import json, urllib.request, sys
q = {
 "query": {"type":"terminal","service":"text",
   "parameters":{"attribute":"rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
                 "operator":"exact_match","value":"P43220"}},
 "return_type":"entry",
 "request_options":{"paginate":{"start":0,"rows":300},"sort":[{"sort_by":"rcsb_accession_info.initial_release_date","direction":"asc"}]}
}
req = urllib.request.Request("https://search.rcsb.org/rcsbsearch/v2/query", data=json.dumps(q).encode(), headers={"Content-Type":"application/json"})
r = json.load(urllib.request.urlopen(req, timeout=60))
ids = [x["identifier"] for x in r["result_set"]]
print(len(ids), r.get("total_count"))
json.dump(ids, open("glp1r_ids.json","w"))
print(ids)
