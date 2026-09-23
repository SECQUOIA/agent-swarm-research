"""Print OSiL rows in readable form: python show.py name [row_from row_to]"""
import sys, os
from osil_eval import Model
M = Model(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{sys.argv[1]}.osil"))
a, b = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, M.m)
def row(r):
    lin = M.objlin if r == -1 else M.lin[r]
    t = [f"{c}*{M.vnames[j]}" for j, c in lin.items()]
    t += [f"{c}*{M.vnames[i]}*{M.vnames[j]}" for i, j, c in M.quad.get(r, [])]
    if r in M.nl: t.append("NL")
    return " + ".join(t)
if a == -1:
    print("OBJ", M.objsense, row(-1)); a = 0
for r in range(a, min(b, M.m)):
    print(M.cnames[r], M.clb[r], "<=", row(r), "<=", M.cub[r])
