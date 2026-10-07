"""Floating-point cross-check with SCIP's own OSiL reader (evidence only, not proof).

Loads the cached OSIL with pyscipopt (SCIP 10), sets every variable to the
double nearest to its box centre (points/chainN_box.json), sets SCIP's
auxiliary objective variable to the double nearest to the exact objective,
and asks SCIP to check the solution with a tight feasibility tolerance. This
confirms that SCIP reads the model the same way as verify_points.py (variable
order, rows, objective), independently of our OSIL reader.

Usage: python3 scip_crosscheck.py 50 100 200 400
"""
import json
import os
import sys

import pyscipopt

HERE = os.path.dirname(os.path.abspath(__file__))
OSIL = os.path.join(os.path.expanduser("~/.cache/minlplib/minlplib/osil"), "chain%d.osil")

for N in [int(a) for a in sys.argv[1:]]:
    box = json.load(open("%s/points/chain%d_box.json" % (HERE, N)))
    fobj = float(box["objective_enclosure_decimal"][1])
    # case "point": the point itself; negative controls: the auxiliary objective
    # variable 1e-11 below the objective, and one u coordinate moved by 1e-9.
    for case in ("point", "objvar-1e-11", "u_5+1e-9"):
        m = pyscipopt.Model()
        m.hideOutput()
        m.readProblem(OSIL % N)
        m.setParam("numerics/feastol", 1e-13)
        byname = {v.name: v for v in m.getVars()}
        assert len(byname) == 2 * N + 3 and "nlobjvar" in byname
        sol = m.createSol()
        for v in box["variables"]:
            val = float(v["centre"])
            if case == "u_5+1e-9" and v["index"] == N + 1 + 5:
                val += 1e-9
            m.setSolVal(sol, byname[v["name"]], val)
        m.setSolVal(sol, byname["nlobjvar"], fobj - (1e-11 if case == "objvar-1e-11" else 0))
        ok = m.checkSol(sol, printreason=False, completely=True, checkbounds=True,
                        checkintegrality=True, checklprows=True, original=True)
        print("chain%d feastol=1e-13 case=%s SCIP checkSol=%s" % (N, case, ok), flush=True)
