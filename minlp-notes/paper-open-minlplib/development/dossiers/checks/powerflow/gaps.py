from fractions import Fraction as Fr
import json, math
def up(x, d):   # round up to d decimals
    q = -((-x.numerator * 10**d) // x.denominator); return q
def sci_up(x, sig=3):
    e = math.floor(math.log10(float(x))); s = Fr(10)**(e - sig + 1)
    q = -((-x) // s) if False else -(-x.numerator * s.denominator // (x.denominator * s.numerator))
    return f"{q}e{e-sig+1}"
data = {
 "powerflow0030p": ("576.8934134703742598676684", "576.8934122988004", "576.8934134704"),
 "powerflow0039p": ("41869.0515113202038027683845", "41869.05148485014", "41869.0515113203"),
 "powerflow0039r": ("41869.0515113209830932768582", "41869.05148327243", "41869.0515113210"),
}
for n, (ub, dual, pdisp) in data.items():
    U, Dd, P = Fr(ub), Fr(dual), Fr(pdisp)
    C = json.load(open(f"/tmp/pfdossier/data/{n}.sdpcert.json"))
    gap = U - Dd
    print(n, "abs gap", float(gap), "up:", sci_up(gap, 4), " rel(dual)", sci_up(gap / Dd, 4), " rel(|primal|)", sci_up(gap/U,4),
          "| display primal >= UB:", P >= U, " gap from displays", sci_up(P - Dd, 4), "rel", sci_up((P-Dd)/Dd, 3))
lb = {"powerflow0039p": "bb3t", "powerflow0039r": "bb3t"}
for n, t in lb.items():
    D = json.load(open(f"/tmp/pfdossier/data/{n}.{t}.json")); L = Fr(D["LB_exact"])
    U = Fr(data[n][0])
    print(n, "stored exact LB >= summary display:", L >= Fr(data[n][1]), " stored LB >= 41869.05148327244:", L >= Fr("41869.05148327244"),
          " gap using stored LB", sci_up(U - L, 4))
