"""Leaf structure of bus L (0-based bus 29 in the author's order) read from the OSIL rows
directly (own reader), and a symbolic check of the leaf identity W_NN = F(Pg, Qg, W_LL)."""
import sys
from fractions import Fraction as Fr
import sympy as S
import own_relax as orl


def show(I, r):
    c = I["cons"][r]
    return f"{c['name']}: lb={c['lb']} ub={c['ub']} lin={ {I['names'][j]: str(a) for j, a in c['lin'].items()} } " \
           f"quad={ {(I['names'][i], I['names'][j]): str(a) for (i, j), a in c['quad'].items()} } nl={c['nl']}"


def main(name, N=1, L=29):
    R = orl.build(name)
    I, info = R["I"], R["info"]
    names = I["names"]
    if info["polar"]:
        busvars = {k: {v for v, kk in info["kv"].items() if kk == k} | {t for t, kk in info["kth"].items() if kk == k}
                   for k in (N, L)}
    else:
        busvars = {k: set(info["keys"][k]) for k in (N, L)}
    print(f"== {name}: bus N={N} vars {[names[j] for j in sorted(busvars[N])]}, bus L={L} vars {[names[j] for j in sorted(busvars[L])]}")

    def vars_of(t, acc):
        if t[0] == "var":
            acc.add(t[1]); return
        if t[0] == "num":
            return
        for c in t[1:]:
            vars_of(c, acc)
    touch = []
    for r, c in enumerate(I["cons"]):
        vs = set(c["lin"]) | {i for ij in c["quad"] for i in ij}
        if c["nl"] is not None:
            vars_of(c["nl"], vs)
        if vs & busvars[L]:
            touch.append(r)
    print(f"  OSIL rows touching bus L: {len(touch)}")
    ys_touch = set()
    for r in touch:
        c = I["cons"][r]
        print("   ", show(I, r)[:400])
        ys_touch |= set(c["lin"]) - busvars[L] - busvars[N]
    # rows containing the y variables defined by the bus-L flow rows (the flows out of L and generator rows)
    print(f"  y variables in those rows: {[names[j] for j in sorted(ys_touch)]}")
    for y in sorted(ys_touch):
        rr = [r for r, c in enumerate(I["cons"]) if y in c["lin"] or any(y in ij for ij in c["quad"])]
        for r in rr:
            if r not in touch:
                print(f"    row with {names[y]}: {show(I, r)[:300]}")
    return R


def symbolic():
    eN, fN, eL, fL, b, Pg, Qg, s_ = S.symbols("eN fN eL fL b Pg Qg s", real=True)
    WNN, WLL = eN**2 + fN**2, eL**2 + fL**2
    wR, wI = eN*eL + fN*fL, eN*fL - fN*eL
    assert S.expand(WNN*WLL - wR**2 - wI**2) == 0
    # with wR = WLL - Qg/b and wI = +-Pg/b:  WNN = (wR^2 + wI^2)/WLL
    F = s_ - 2*Qg/b + (Qg**2 + Pg**2)/(b**2*s_)
    assert S.simplify(((s_ - Qg/b)**2 + (Pg/b)**2)/s_ - F) == 0
    # convexity: Hessian of (p^2+q^2)/s on s>0 is psd (perspective); check its leading minors
    p, q = S.symbols("p q", real=True); sp = S.symbols("sp", positive=True)
    g = (p**2 + q**2)/sp
    H = S.hessian(g, (p, q, sp))
    print("  symbolic: Lagrange identity ok; F = ((W_LL - Qg/b)^2 + Pg^2/b^2)/W_LL ok;",
          "Hessian of (p^2+q^2)/s:", H.tolist(), "det", S.simplify(H.det()), "2x2 minor", S.simplify(H[:2, :2].det()))


if __name__ == "__main__":
    for nm in sys.argv[1:]:
        main(nm)
    symbolic()
