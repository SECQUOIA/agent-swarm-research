"""Load the author's pindyck_global.py definitions (steps 1-4 executed, step 5 functions defined,
nothing after) with its log redirected to /dev/null. Used only to test the author's psi_tm."""
import os
import sys

SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "open-instances-wave2", "small",
                                    "pindyck_global.py"))


def load():
    src = open(SRC).read()
    cut = src.index("th, JH = float_states(np.array([float(v) for v in pstr]))")
    src = src[:cut]
    old_log = 'LOG = open(os.path.join(ev.HERE, "logs", "pindyck_global.log"), "w")'
    assert old_log in src
    src = src.replace(old_log, 'LOG = open(os.devnull, "w")')
    ns = {"__file__": SRC, "__name__": "author_exec"}
    sys.path.insert(0, os.path.dirname(SRC))
    exec(compile(src, SRC, "exec"), ns)
    return ns
