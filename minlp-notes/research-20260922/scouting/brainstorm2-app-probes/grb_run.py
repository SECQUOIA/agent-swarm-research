from pathlib import Path as _CleanupPath
_NOTES_ROOT = _CleanupPath(__file__).resolve().parent.joinpath('../../..').resolve()

import sys
sys.path.insert(0,(str(_NOTES_ROOT) + '/research-20260922/benchmark-observations/code'))
from osil_eval import Model
from grb_build import build
name, tl = sys.argv[1], float(sys.argv[2])
M = Model(f"{_CleanupPath.home()}/.cache/minlplib/minlplib/osil/{name}.osil")
g, x = build(M)
g.Params.TimeLimit = tl; g.Params.Threads = int(sys.argv[3]) if len(sys.argv)>3 else 4; g.Params.OutputFlag = 0
g.optimize()
pb = g.ObjVal if g.SolCount else None
print(name, "status", g.Status, "primal", pb, "dual", g.ObjBound, "nodes", g.NodeCount, "time", g.Runtime, flush=True)
