"""Solver root bounds (Gurobi, NodeLimit=1, default cuts on) for orig and cuts forms.
python root_bounds.py out.jsonl f8x12 --caps uniform random --costs quad log --seeds 0 1 2 3 4"""
import argparse, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vertex_binarization"))
import gurobipy as gp
from instances import transport, netflow, transport_fc
from rowhull.strengthen import cut_loop, cut_ir
from sob.model import original_ir
import sob.backends as be

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("size")
ap.add_argument("--caps", nargs="+"); ap.add_argument("--costs", nargs="+"); ap.add_argument("--seeds", nargs="+", type=int)
a = ap.parse_args()


def root(ir):
    """Reuse the backend model builder but stop after the root node."""
    orig_model = gp.Model
    captured = {}

    class M(orig_model):
        def optimize(self, *args):
            self.Params.NodeLimit = 1
            super().optimize(*args)
            captured["bound"] = self.ObjBound
    gp.Model = M
    try:
        be.solve_gurobi(ir, 300, threads=4)
    except Exception as e:  # noqa: BLE001
        captured.setdefault("error", repr(e))
    finally:
        gp.Model = orig_model
    return captured.get("bound")


with open(a.out, "a") as fh:
    for cap in a.caps:
        for cost in a.costs:
            for seed in a.seeds:
                s = a.size
                if s.startswith("f"):
                    m, n = s[1:].split("x"); p = transport_fc(int(m), int(n), seed, cap, cost)
                elif s.startswith("g"):
                    m, n = s[1:].split("d")[0].split("n"); p = netflow(int(m), int(n), seed, cap, cost)
                else:
                    m, n = s.split("x"); p = transport(int(m), int(n), seed, cap, cost)
                cuts, extra, info = cut_loop(p)
                rec = {"name": p.name, "lp_termwise": info["bound0"], "lp_rowhull": info["bound"],
                       "gurobi_root_orig": root(original_ir(p)), "gurobi_root_cuts": root(cut_ir(p, cuts, extra))}
                fh.write(json.dumps(rec) + "\n"); fh.flush()
                print(rec, flush=True)
