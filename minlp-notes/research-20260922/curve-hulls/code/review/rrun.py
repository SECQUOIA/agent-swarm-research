"""Reviewer's reproduction run: python rrun.py <instance> <orig|sub|cuts> <timelimit> [seed]
Uses rbuild (independent builder) and, for 'cuts', the author's saved cuts/<instance>.json as static rows."""
import json, os, sys, time
import rbuild

name, mode, tl = sys.argv[1], sys.argv[2], float(sys.argv[3])
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
HERE = os.path.dirname(os.path.abspath(__file__))
m, x, y, z, P = rbuild.build(name, "orig" if mode == "orig" else "sub")
ncuts = 0
if mode == "cuts":
    cuts = json.load(open(os.path.join(HERE, "..", "cuts", f"{name}.json")))
    rbuild.add_cuts(m, x, y, z, cuts)
    ncuts = len(cuts)
m.Params.TimeLimit = tl
m.Params.Seed = seed
m.Params.OutputFlag = 1
m.Params.LogFile = os.path.join(HERE, f"{name}_{mode}_{int(tl)}_s{seed}.log")
m.Params.LogToConsole = 0
t0 = time.time()
m.optimize()
print(json.dumps({"name": name, "mode": mode, "tl": tl, "seed": seed, "ncuts": ncuts, "nsel": len(y),
                  "status": m.Status, "dual": m.ObjBound, "primal": m.ObjVal if m.SolCount else None,
                  "nodes": m.NodeCount, "time": time.time() - t0}), flush=True)
