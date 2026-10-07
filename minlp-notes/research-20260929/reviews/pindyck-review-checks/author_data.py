"""Extract the author's certificate data by executing pindyck_global.py up to the end of its
branch and bound (step 5), with its log redirected to /dev/null and one line added to record
the leaf boxes. Nothing in the author's directory is written.

Saves author_data.pkl: CSH, W, gam, pmax, GCSL, GCSH, rng, lo0, hi0, LEAVES, splits.
"""
import os
import pickle
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "open-instances-wave2", "small", "pindyck_global.py"))
src = open(SRC).read()
cut = src.index("# ---------------- step 6:")
src = src[:cut]
old_log = 'LOG = open(os.path.join(ev.HERE, "logs", "pindyck_global.log"), "w")'
assert old_log in src
src = src.replace(old_log, 'LOG = open(os.devnull, "w")')
old_leaf = "        nbox += 1\n"
assert src.count(old_leaf) == 1
src = src.replace(old_leaf, "        nbox += 1\n        LEAVES.append(({k: v.copy() for k, v in lo.items()}, {k: v.copy() for k, v in hi.items()}, est))\n")
ns = {"__file__": SRC, "__name__": "author_exec", "LEAVES": []}
sys.path.insert(0, os.path.dirname(SRC))
exec(compile(src, SRC, "exec"), ns)
keep = {k: ns[k] for k in ["CSH", "CSL", "W", "gam", "pmax", "GCSL", "GCSH", "rng", "lo0", "hi0", "LEAVES", "splits"]}
pickle.dump(keep, open(os.path.join(HERE, "author_data.pkl"), "wb"))
print("leaves:", len(keep["LEAVES"]), "splits:", keep["splits"])
