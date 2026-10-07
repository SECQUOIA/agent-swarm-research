"""Compare the reviewer's own relaxation rows (own_relax) with the author's pf_model rows,
row by row and exactly; check the polar conversion at random points; check angle rows."""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
from fractions import Fraction as Fr
import mpmath as mp
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/powerflow")
import pf_model as pm
import own_relax as orl


def tfr(t):
    """exact Fraction of an mpmath mpf tuple (sign, man, exp, bc)"""
    sign, man, exp, bc = t
    v = Fr(man) * (Fr(2) ** exp)
    return -v if sign else v


def norm(r):
    return dict(lin={j: c for j, c in r["lin"].items() if c != 0}, Q={k: c for k, c in r["Q"].items() if c != 0},
                qy={j: c for j, c in r["qy"].items() if c != 0}, lb=r["lb"], ub=r["ub"])


def main(name):
    R = orl.build(name)
    M = pm.decode(name)
    names = [r["name"] for r in M["rows"]]
    mine = set(R["order"])
    angle = [r for r in M["rows"] if r["kind"] == "angle"]
    other = [r for r in M["rows"] if r["kind"] != "angle"]
    assert len(set(names)) == len(names)
    assert {r["name"] for r in other} == mine, (sorted({r['name'] for r in other} ^ mine))
    bad = [r["name"] for r in other if norm(r) != norm(R["rows"][r["name"]])]
    print(f"{name}: polar={R['info']['polar']} n={R['n']}; author rows {len(M['rows'])} "
          f"(angle {len(angle)}); non-angle rows identical to own construction: {not bad} {bad[:5]}")
    assert not bad
    assert M["ybox"] == R["ybox"], "y boxes differ"
    assert M["ys"] == R["ys"] and M["vmax2"] == R["vmax2"]
    assert M["obj"]["const"] == R["obj"]["const"] and M["obj"]["lin"] == R["obj"]["lin"] and M["obj"]["qy"] == R["obj"]["qy"]
    print(f"  y boxes ({len(R['ybox'])}), y list, vmax2 (sum {float(sum(R['vmax2']))}), objective: identical;"
          f" dropped reference row {R['info'].get('ref_dropped')}")
    if R["info"]["polar"]:
        w = orl.check_polar_identity(R)
        print(f"  polar flow rows: max |native - converted| at 3 random points (60 digits): {mp.nstr(w, 3)}")
        # angle rows: rebuild from own angle intervals and check tb >= tan(B0), ta <= tan(A0)
        ang = R["info"]["angle"]
        assert len(angle) == 2 * len(ang)
        worst = None
        for (kp, kq), (A0, B0) in ang.items():
            assert A0 is not None and B0 is not None and A0 <= B0
            ru = next(r for r in angle if r["name"] == f"A{kp}_{kq}u")
            rl = next(r for r in angle if r["name"] == f"A{kp}_{kq}l")
            E, F = (lambda k: 2 * k), (lambda k: 2 * k + 1)
            # ru: tb*WR - WI >= 0 ; WR = e_p e_q + f_p f_q ; WI = f_p e_q - e_p f_q
            tb = ru["Q"][(E(kp), E(kq))]
            assert ru["Q"] == {(E(kp), E(kq)): tb, (F(kp), F(kq)): tb, (E(kq), F(kp)) if E(kq) < F(kp) else (F(kp), E(kq)): Fr(-1),
                               (E(kp), F(kq)): Fr(1)} and ru["lb"] == 0 and ru["ub"] is None and not ru["lin"]
            ta = -rl["Q"][(E(kp), E(kq))]
            assert rl["Q"] == {(E(kp), E(kq)): -ta, (F(kp), F(kq)): -ta, (E(kq), F(kp)) if E(kq) < F(kp) else (F(kp), E(kq)): Fr(1),
                               (E(kp), F(kq)): Fr(-1)} and rl["lb"] == 0 and rl["ub"] is None and not rl["lin"]
            mp.iv.prec = 300
            ivA = mp.iv.mpf(A0.numerator) / A0.denominator
            ivB = mp.iv.mpf(B0.numerator) / B0.denominator
            halfpi = mp.iv.pi / 2
            assert tfr(ivB._mpi_[1]) < tfr(halfpi._mpi_[0]) and tfr((-halfpi)._mpi_[1]) < tfr(ivA._mpi_[0])
            tB, tA = mp.iv.tan(ivB), mp.iv.tan(ivA)
            ok = tfr(tB._mpi_[1]) <= tb and ta <= tfr(tA._mpi_[0])     # exact rational comparisons
            worst = min(worst or 1, tb - tfr(tB._mpi_[1]), tfr(tA._mpi_[0]) - ta)
            assert ok, ((kp, kq), A0, B0)
        print(f"  angle rows: {len(ang)} pairs; |A0|,|B0| < pi/2 and tb >= tan(B0), ta <= tan(A0) (300-bit intervals,"
              f" exact comparison): ok; smallest margin {float(worst):.2e}")
    return R, M


if __name__ == "__main__":
    for nm in sys.argv[1:]:
        main(nm)
