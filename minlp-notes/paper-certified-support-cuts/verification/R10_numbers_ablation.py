#!/usr/bin/env python3
"""R10 (numbers lens): recompute Table 2 (U1, U2, U3) from the per-cut entries
of evidence/ablation-uncertified.json and evidence/ablation-global-solve.json.

Wrong: constant exceeds the exact certified value by more than
1e-6 max(1, |certified|), recomputed exactly here from the hex constant and the
rational certified value. Cuts off / optimum: taken from the per-cut row checks
(removed points; removed_known_witness). Standard library only.
"""
import json
import os
from collections import defaultdict
from fractions import Fraction as Q

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "..", "evidence")


def hexq(s):
    return Q(float.fromhex(s)) if isinstance(s, str) else Q(s)


def material(u, cert):
    return u - cert > Q(1, 10**6) * max(Q(1), abs(cert))


def main():
    U = json.load(open(os.path.join(EV, "ablation-uncertified.json")))
    G = json.load(open(os.path.join(EV, "ablation-global-solve.json")))
    stats = defaultdict(lambda: defaultdict(int))
    models = defaultdict(lambda: defaultdict(set))
    fam_cuts = defaultdict(int)
    fam_models = defaultdict(set)
    mism = 0
    for c in U["cuts"]:
        if not c.get("exact_certificate"):
            continue
        fam = c["family"]
        fam_cuts[fam] += 1
        fam_models[fam].add(c["name"])
        cert = Q(c["certified"])
        for u in ("u1", "u2"):
            m = material(hexq(c[u]), cert)
            if m != bool(c.get(u + "_material")):
                mism += 1
            if m:
                stats[(fam, u)]["wrong"] += 1
                models[(fam, u)]["wrong"].add(c["name"])
            rows = c.get(u + "_rows") or {}
            if rows.get("removed"):
                stats[(fam, u)]["off"] += 1
                models[(fam, u)]["off"].add(c["name"])
            if rows.get("removed_known_witness"):
                stats[(fam, u)]["opt"] += 1
    print(f"exact-certificate cuts: " + ", ".join(f"{f}: {n} cuts, {len(fam_models[f])} models" for f, n in fam_cuts.items())
          + f"; material flag mismatches {mism}")
    lower = [c for c in U["cuts"] if not c.get("exact_certificate")]
    print(f"cuts without exact certificate: {len(lower)}, parts {sorted({c['part'] for c in lower})}, methods {sorted({c['method'] for c in lower})}")
    gst = defaultdict(lambda: defaultdict(int)); gmod = defaultdict(lambda: defaultdict(set))
    gm = 0
    keys = set()
    for c in G["cuts"]:
        fam = c["family"]
        cert = Q(c["certified"])
        for u in ("u3", "u3p", "u3s"):
            if c.get(u) is None:
                gst[(fam, u)]["no_value"] += 1
                continue
            m = material(hexq(c[u]), cert)
            if m != bool(c.get(u + "_material")):
                gm += 1
            if m:
                gst[(fam, u)]["wrong"] += 1
                gmod[(fam, u)]["wrong"].add(c["name"])
                if u == "u3":
                    keys.add((c["name"], tuple(c["coefficients"])))
            rows = c.get(u + "_rows") or {}
            if rows.get("removed"):
                gst[(fam, u)]["off"] += 1
                gmod[(fam, u)]["off"].add(c["name"])
            if rows.get("removed_known_witness"):
                gst[(fam, u)]["opt"] += 1
    print(f"global-solve cuts {len(G['cuts'])}; material flag mismatches {gm}")
    for fam in ("minlplib", "path"):
        for u in ("u1", "u2"):
            s = stats[(fam, u)]; m = models[(fam, u)]
            print(f"  {fam:8s} {u}: wrong {s['wrong']} ({len(m['wrong'])} models) cuts off {s['off']} ({len(m['off'])} models) optimum {s['opt']}"
                  f"  share wrong {s['wrong']/fam_cuts[fam]:.4f}")
        for u in ("u3", "u3p", "u3s"):
            s = gst[(fam, u)]; m = gmod[(fam, u)]
            print(f"  {fam:8s} {u}: wrong {s['wrong']} ({len(m['wrong'])} models {sorted(m['wrong'])}) cuts off {s['off']} ({len(m['off'])}) optimum {s['opt']} no_value {s['no_value']}")
    print(f"  distinct U3-wrong cuts (name, direction): {len(keys)}")
    # nvs02 U3 details
    for c in G["cuts"]:
        if c.get("u3_material"):
            print("   U3 wrong:", c["name"], c["run_id"], "excess", c.get("u3_excess_float"), "status", (c.get("gurobi") or {}).get("status"),
                  "mip_gap", (c.get("gurobi") or {}).get("mip_gap"))
            break
    # path sample size and distinct
    p = [c for c in U["cuts"] if c["family"] == "path"]
    print(f"  path sample {len(p)}, distinct (name, coefficients) {len({(c['name'], tuple(c['coefficients'])) for c in p})}, instances {len({c['name'] for c in p})}")
    # tenfold tolerance
    for fam in ("minlplib", "path"):
        for u in ("u1", "u2"):
            n = sum(1 for c in U["cuts"] if c.get("exact_certificate") and c["family"] == fam and
                    hexq(c[u]) - Q(c["certified"]) > Q(1, 10**5) * max(Q(1), abs(Q(c["certified"]))))
            print(f"  {fam} {u} wrong at tolerance 1e-5: {n}")


if __name__ == "__main__":
    main()
