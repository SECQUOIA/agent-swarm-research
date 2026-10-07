"""Search small pump-like MINLPs on which SCIP with DEFAULT settings claims a
wrong optimum because of the binary64 inconsistency fl(L)^3 != fl(L^3).

Model with n pumps i (all data are short decimals):
  b_i binary; L_i <= s_i <= 1; L_i^3 <= p_i <= 1; 0 <= q_i <= Q_i; 0 <= w_i <= 1
  cube_i:  p_i = s_i^3
  speed_i: s_i - (1 - L_i) b_i <= L_i          (pump off => s_i = L_i)
  flow_i:  q_i - K_i (s_i - L_i) - M_i b_i <= 0  (flow needs the pump on)
  pow_i:   w_i - p_i - b_i >= -1               (w_i >= p_i if the pump is on)
  demand:  sum_i q_i >= D
  min  sum_i (C_i w_i + F_i b_i)
For each instance the default run is compared with a run using
constraints/nonlinear/varboundrelax = b (a different, here unaffected path).
A candidate is printed if the default 'optimal' value exceeds the other
run's incumbent by more than 1e-4; candidates are then checked exactly.
usage: [ORACLE=master] [FUZZ_N=n] python3 fuzz.py N_INSTANCES SEED OUTDIR
"""
import os
import random
import sys

import pyscipopt as ps

LS = ["0.6", "0.7", "0.85"]
CUBE = {"0.6": "0.216", "0.7": "0.343", "0.85": "0.614125"}


def make(rng, n):
    vars_, rows, obj = [], [], {}
    data = []
    for i in range(n):
        L = rng.choice(LS)
        Q = rng.choice(["0.5", "0.8", "1"])
        K = rng.choice(["1", "2", "3"])
        M = rng.choice(["0.1", "0.2", "0.3"])
        C = rng.choice(["1", "2", "3", "5"])
        Fc = rng.choice(["0", "0.1", "0.2", "0.5"])
        data.append((L, Q, K, M, C, Fc))
        vars_ += [(f"b{i}", "binary", "0", "1"), (f"s{i}", "continuous", L, "1"),
                  (f"p{i}", "continuous", CUBE[L], "1"), (f"q{i}", "continuous", "0", Q),
                  (f"w{i}", "continuous", "0", "1")]
        obj[f"w{i}"] = C
        obj[f"b{i}"] = Fc
        one_minus_L = str(round(1 - float(L), 2))
        rows.append(f"  [nonlinear] <cube{i}>: -1*<p{i}> +1*<s{i}>*<s{i}>*<s{i}> == 0;")
        rows.append(f"  [linear] <speed{i}>: +1<s{i}> -{one_minus_L}<b{i}> <= {L};")
        # q - K s - M b <= -K L
        KL = str(round(float(K) * float(L), 4))
        rows.append(f"  [linear] <flow{i}>: +1<q{i}> -{K}<s{i}> -{M}<b{i}> <= -{KL};")
        rows.append(f"  [linear] <pow{i}>: +1<w{i}> -1<p{i}> -1<b{i}> >= -1;")
    D = rng.choice(["0.3", "0.5", "0.7", "0.9", "1.2"])
    rows.append("  [linear] <demand>: " + " ".join(f"+1<q{i}>" for i in range(n)) + f" >= {D};")
    L_ = ["STATISTICS", "  Problem name     : fuzz", "OBJECTIVE", "  Sense            : minimize", "VARIABLES"]
    for name, typ, lo, hi in vars_:
        L_.append(f"  [{typ}] <{name}>: obj={obj.get(name, '0')}, original bounds=[{lo},{hi}]")
    L_ += ["CONSTRAINTS"] + rows + ["END"]
    return "\n".join(L_) + "\n"


ORACLE = os.environ.get("ORACLE")  # e.g. "master": solve with run_binary.py's binaries instead of PySCIPOpt


def solve(path, prm):
    if ORACLE:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
        import run_binary
        r = run_binary.run(ORACLE, path, prm, timelimit=60)
        st = "optimal" if r["status"].startswith("problem is solved [optimal") else r["status"]
        return (st, r["dual"], r["primal"] if r["primal"] is not None else float("inf"), r["nodes"])
    m = ps.Model()
    m.hideOutput()
    m.readProblem(path)
    m.setParam("limits/time", 60)
    for k, v in prm.items():
        m.setParam(k, v)
    m.optimize()
    r = (m.getStatus(), m.getDualbound(), m.getPrimalbound() if m.getNSols() else float("inf"), m.getNNodes())
    m.freeProb()
    return r


def main():
    N, seed, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    os.makedirs(out, exist_ok=True)
    rng = random.Random(seed)
    found = 0
    for k in range(N):
        n = int(os.environ.get("FUZZ_N", "0")) or rng.choice([2, 3, 4])
        path = os.path.join(out, f"fuzz_{seed}_{k}.cip")
        open(path, "w").write(make(rng, n))
        d = solve(path, {})
        r = solve(path, {"constraints/nonlinear/varboundrelax": "b"})
        bad = d[0] == "optimal" and d[1] > r[2] + 1e-4
        if bad:
            found += 1
            print(f"CANDIDATE {path}: default {d}  varboundrelax=b {r}", flush=True)
        else:
            os.unlink(path)
    print(f"# {found} candidates in {N} instances (seed {seed})")


if __name__ == "__main__":
    main()
