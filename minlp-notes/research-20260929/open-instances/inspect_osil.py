"""Print a compact structural dump of an OSIL instance (first rows, objective)."""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../..'))
import sys
sys.path.insert(0, _REPRO_ROOT + "/research-20260922/scouting/minlplib-open-data")
import osil
name = sys.argv[1]; nshow = int(sys.argv[2]) if len(sys.argv) > 2 else 6
I = osil.read(_repro_os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
nv = len(I["vt"]); print(name, "nvars", nv, "ncons", I["ncons"], "sense", I["sense"])
from collections import Counter
print("var types", Counter(I["vt"]))
print("bounds", Counter((I["lb"][j], I["ub"][j]) for j in range(nv)).most_common(8))
def show(r):
    row = I["rows"][r]
    lin = {I["names"][k]: v for k, v in row["lin"].items()}
    q = [(I["names"][i], I["names"][j], c) for i, j, c in row["quad"]]
    print(r, row.get("name"), "lb", row["lb"], "ub", row["ub"], "lin", dict(list(lin.items())[:12]), "nlin", len(lin), "quad", q[:8], "nq", len(q), "nl", str(row["nl"])[:600])
show(-1)
for r in list(range(nshow)) + list(range(max(nshow, I["ncons"] - 3), I["ncons"])):
    show(r)
print("first vars", [(I["names"][j], I["lb"][j], I["ub"][j]) for j in range(min(8, nv))])
print("last vars", [(I["names"][j], I["lb"][j], I["ub"][j]) for j in range(max(0, nv - 5), nv)])
