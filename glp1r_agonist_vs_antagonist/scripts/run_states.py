import sys, json, warnings
warnings.filterwarnings("ignore"); sys.path.insert(0,'.')
from an4 import *
out=[]
for pid,rc,pc,het in CASES:
    try: out.append(analyse(pid,rc,pc,het))
    except Exception as e: out.append({"pid":pid,"err":repr(e)})
json.dump(out,open("work/states.json","w"),indent=1)
print(len(out))
