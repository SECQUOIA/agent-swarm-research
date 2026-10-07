"""Load a cell-slope certificate pickle without importing the authors' code.

The pickle stores an instance of cs.State; a stub class with the same
qualified name receives the attribute dict (no method of the authors' class
is used)."""
import gzip
import pickle
import sys
import types


class State:  # stub; only __dict__ is used
    pass


def load(path):
    mod = types.ModuleType("cs")
    mod.State = State
    saved = sys.modules.get("cs")
    sys.modules["cs"] = mod
    try:
        opener = gzip.open if path.endswith(".gz") else open
        with opener(path, "rb") as fh:
            return pickle.load(fh).__dict__
    finally:
        if saved is None:
            del sys.modules["cs"]
        else:
            sys.modules["cs"] = saved
