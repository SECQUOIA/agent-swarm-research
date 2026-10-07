"""Negative controls: the verifier must reject damaged point files."""
import copy, json, os, tempfile
from fractions import Fraction as Fr
import verify

src = verify.PTS
tmp = tempfile.mkdtemp()
verify.PTS = tmp


def run(name, mutate, label):
    P = json.load(open(os.path.join(src, name + ".json")))
    mutate(P)
    json.dump(P, open(os.path.join(tmp, name + ".json"), "w"))
    try:
        verify.main(name)
        print(f"NEGATIVE CONTROL NOT REJECTED: {label}")
    except AssertionError as e:
        print(f"rejected as expected ({label}): {str(e)[:90]}")


def shift_centre(P):
    v = "x5"
    P["free"][v] = str(Fr(P["free"][v]) + Fr(1, 10**44))


def bump_bound(P):
    P["fixed"]["x29"]["value"] = str(Fr(21, 20) + Fr(1, 10**30))


def drop_row(P):
    P["system"] = P["system"][:-1]
    k = sorted(P["free"])[0]
    P["fixed"][k] = {"value": P["free"].pop(k)}


def swap_side(P):
    for d in P["system"]:
        if d["row"] == "e208":
            d["side"] = "lb"


def big_radius(P):
    P["radius"] = "1e-3"


import contextlib, io
for lab, f in [("centre shifted by 1e-44 > radius", shift_centre), ("x29 above its bound by 1e-30", bump_bound),
               ("one row removed from S, one free var fixed at its centre", drop_row), ("e208 taken at its lower side", swap_side),
               ("radius 1e-3", big_radius)]:
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        try:
            run("powerflow0030p", f, lab)
        except Exception as e:
            print(f"rejected with {type(e).__name__} ({lab}): {str(e)[:90]}")
    print([l for l in buf.getvalue().splitlines() if "rejected" in l or "NOT REJECTED" in l][0])
