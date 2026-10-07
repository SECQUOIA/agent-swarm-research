"""Time distribution of SCIP on random grid pairs (exploration)."""
import sys, json, random, time
import numpy as np
sys.path.insert(0, "..")
import core, tasks, plan
from dpcells import CellPlan
cfg = json.load(open(sys.argv[3] if len(sys.argv) > 3 else "logs/plan1.json"))
T = 6
tasks.init(T, cfg["implied"], True)
D = tasks._W["D"]
P = CellPlan(T, plan.load_slopes(D, cfg), 0.0, [core.level_box(D, t) for t in range(T - 1)])
for l in range(T - 1):
    P.grid(l, cfg["breaks"])
random.seed(int(sys.argv[1]))
pairs = [(t, random.randrange(P.nrow(t)), random.randrange(P.ncol(t))) for t in [random.randrange(1, 5) for _ in range(int(sys.argv[2]))]]
for key, t, cin, cout, lin, lout, mu, tl in plan.est_tasks(P, pairs, cfg):
    _, r = tasks.scip_task((key, t, cin, cout, lin, lout, mu, tl))
    print(t, "%.2fs" % r["time"], r["status"], r["est"], flush=True)
