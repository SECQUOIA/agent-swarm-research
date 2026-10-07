"""Mutation test: crosscheck.py must reject slightly wrong point files.

Usage: python3 mutation_test.py   (uses lnts50; writes and removes ./mut/)
"""
import json
import os
import shutil
import subprocess
from fractions import Fraction as Q

base = json.load(open("points/lnts50_point.json"))
os.makedirs("mut", exist_ok=True)


def run(tag, P, expect_ok):
    json.dump(P, open("mut/lnts50_point.json", "w"))
    r = subprocess.run(["python3", "crosscheck.py", "--points", "mut", "50"], capture_output=True, text=True)
    last = (r.stderr.strip().splitlines() or [""])[-1]
    ok = r.returncode == 0
    print(f"{tag}: crosscheck {'passed' if ok else 'failed'} ({'as expected' if ok == expect_ok else 'UNEXPECTED'})"
          + ("" if ok else f" | {last[:90]}"))
    return ok == expect_ok


copy = lambda: json.loads(json.dumps(base))
res = []
P = copy()
P["fixed_controls"]["x2"] = str(Q(P["fixed_controls"]["x2"]) + Q(1, 10**45))
res.append(run("fixed control x2 + 1e-45", P, False))
P = copy()
d = P["unknowns_box"]["x257"]
d["centre"] = str(Q(d["centre"]) + 2 * Q(d["radius"]))
res.append(run("h centre + 2 radii", P, False))
P = copy()
e = P["enclosures"][52]
e[1], e[2] = str(Q(e[1]) + Q(1, 10**55)), str(Q(e[2]) + Q(1, 10**55))
res.append(run("enclosure of state x53 + 1e-55", P, False))
res.append(run("unchanged copy", copy(), True))
shutil.rmtree("mut")
print("all as expected" if all(res) else "SOME UNEXPECTED")
