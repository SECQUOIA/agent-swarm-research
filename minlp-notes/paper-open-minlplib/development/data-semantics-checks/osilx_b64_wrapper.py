"""Patched reader for the data-semantics audit: every numeric string that is not
binary64-exact is replaced by the exact decimal expansion of its binary64 value
(reading (c)); binary64-exact strings are kept unchanged. Everything else is osilx."""
import os
from fractions import Fraction
from osilx_orig import *  # noqa: F401,F403
import osilx_orig as _o

MODE = os.environ.get("OSIL_READING", "b64")
STATS = {"changed": 0, "kept": 0}


def _b64(s):
    if not isinstance(s, str) or _o.isinf(s):
        return s
    try:
        q = Fraction(s)
    except (ValueError, ZeroDivisionError):
        return s
    f = Fraction(float(s))
    if f == q:
        STATS["kept"] += 1
        return s
    STATS["changed"] += 1
    n, d = f.numerator, f.denominator
    k = d.bit_length() - 1
    assert d == 1 << k
    return f"{n * 5 ** k}e-{k}"


def _tree(t):
    if t is None:
        return None
    if t[0] == "num":
        return ("num", _b64(t[1]))
    if t[0] == "var":
        return ("var", t[1], _b64(t[2]))
    return (t[0],) + tuple(_tree(c) for c in t[1:])


def read(path):
    I = _o.read(path)
    if MODE != "b64":
        return I
    I["lb"] = [_b64(s) for s in I["lb"]]
    I["ub"] = [_b64(s) for s in I["ub"]]
    rows = I["cons"] + [I["obj"]]
    for c in rows:
        for key in ("lb", "ub", "constant"):
            if key in c:
                c[key] = _b64(c[key])
        c["lin"] = {j: _b64(v) for j, v in c["lin"].items()}
        c["quad"] = [(i, j, _b64(v)) for i, j, v in c["quad"]]
        c["nl"] = _tree(c["nl"])
    print(f"[osilx-b64] {os.path.basename(path)}: changed {STATS['changed']} numeric strings, kept {STATS['kept']}", flush=True)
    return I
