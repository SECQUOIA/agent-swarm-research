"""B&B on the chiral chain.  Usage: python3 run_chiral.py B G EV D RULE EPS n   (class P_D) -> one JSON line."""
import sys, json
from chiral import chain
from polychain import bb, poly_class
b, g, ev = map(float, sys.argv[1:4]); d = int(sys.argv[4]); rule = sys.argv[5]; eps = float(sys.argv[6]); n = int(sys.argv[7])
r = bb(chain(n, b, g, ev), poly_class(d), eps, 0.0, rule=rule, timelimit=10800)
print(json.dumps(dict(family="chiral", b=b, g=g, ev=ev, cls=f"P{d}", rule=rule, eps=eps, n=n, **r)), flush=True)
