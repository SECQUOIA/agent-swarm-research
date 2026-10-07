"""Readable dump of an OSIL instance (verifier's own; uses osilx reader + common.fmt)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "wave2-small-verification"))
from common import load, fmt
name = sys.argv[1]
m = load(name)
N = m["names"]
print("nvars", len(N), "ncons", len(m["cons"]))
from collections import Counter
print(Counter(m["vt"]))
for i, n in enumerate(N):
    if m["lb"][i] not in ("0",) or m["ub"][i] not in ("INF", "1"):
        print("var", i, n, m["vt"][i], m["lb"][i], m["ub"][i])
o = m["obj"]
print("OBJ", o["sense"], "const", o["constant"], {N[k]: v for k, v in o["lin"].items()}, o["quad"], o["nl"] and fmt(o["nl"], N))
for r, c in enumerate(m["cons"]):
    s = " + ".join("%s*%s" % (v, N[k]) for k, v in c["lin"].items())
    if c["quad"]:
        s += " + " + " + ".join("%s*%s*%s" % (cc, N[i], N[j]) for i, j, cc in c["quad"])
    if c["nl"] is not None:
        s += " + " + fmt(c["nl"], N)
    print("row", r, c["name"], c["lb"], "<=", s, "(+%s)" % c["constant"] if c["constant"] != "0" else "", "<=", c["ub"])
