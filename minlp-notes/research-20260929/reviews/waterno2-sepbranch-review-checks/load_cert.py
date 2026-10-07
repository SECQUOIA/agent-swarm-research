"""Load a certify_dp.py pickle without importing the authors' code.

The pickle stores an instance of dpcells.CellPlan; a stub class with the same
qualified name receives the attribute dict (no methods of the authors' class
are used)."""
import pickle
import sys
import types


class CellPlan:  # stub; only __dict__ is used
    pass


def load(path):
    mod = types.ModuleType("dpcells")
    mod.CellPlan = CellPlan
    saved = sys.modules.get("dpcells")
    sys.modules["dpcells"] = mod
    try:
        with open(path, "rb") as fh:
            return pickle.load(fh)
    finally:
        if saved is None:
            del sys.modules["dpcells"]
        else:
            sys.modules["dpcells"] = saved
