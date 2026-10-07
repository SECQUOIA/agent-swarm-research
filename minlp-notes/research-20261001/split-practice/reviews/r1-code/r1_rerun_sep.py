"""Reviewer r1: rerun the stream's own separators on a few stored points
(uses the stream code on purpose; independent checks are in r1_bruteforce.py
and r1_hard.py).  Usage: python3 reviews/r1-code/r1_rerun_sep.py OUT.jsonl file...
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "code"))
from exp_separate import analyse, _clean  # noqa: E402
out = sys.argv[1]
with open(out, "w") as f:
    for p in sys.argv[2:]:
        rec = analyse(p)
        f.write(json.dumps(_clean(rec)) + "\n"); f.flush()
        print(rec["file"], rec["ratio"]["ratio"], rec["ratio"]["complete"], [(K, rec[f"grb{K}"]["q"], rec[f"grb{K}"]["status"]) for K in (1, 3, 10)],
              {k: rec["thm3"].get(k) for k in ("q", "q_at_Y", "vmax_digits", "error")} if "thm3" in rec else None, flush=True)
