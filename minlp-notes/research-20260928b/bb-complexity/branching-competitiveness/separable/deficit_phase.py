"""The deficit rule is not competitive within a phase (revision after the review; the
counterexample is the review's, re-derived here with this note's engine).
x: m = t^2 exactly (QuadCoord); z: tent H = max(0, (1-eps) t, (1+eps) t - eps), m_z = H - t^2.
Prints the size of deficit's first phase (x-splits with z = [0,1]) and checks that the strip
[0,1] x [2/5, 3/5] is valid, so a certificate exists in which exactly one box meets the phase
segment [0,1] x {1/2} (n_P = 1); the remaining boxes lie in z <= 2/5 or z >= 3/5."""
from fractions import Fraction as Fr
from sepexact import Coord, QuadCoord, run

for k in range(3, 11):
    eps = Fr(1, 10 ** k)
    x = QuadCoord(0)
    z = Coord([Fr(0), Fr(1, 2), Fr(1)], [Fr(0), (1 - eps) / 2, Fr(1)])
    Fz, yz, wz = z.node(Fr(0), Fr(1))
    r = run([x, z], eps, "deficit", record=True)
    phase1 = sum(1 for box, y, i, ph in r["internal"] if i == 0 and box[1] == (Fr(0), Fr(1)))
    ro = run([x, z], eps, "omega", record=True)
    ophase1 = sum(1 for box, y, i, ph in ro["internal"] if i == 0 and box[1] == (Fr(0), Fr(1)))
    strip = x.F(Fr(0), Fr(1)) + z.F(Fr(2, 5), Fr(3, 5)) + eps
    Nx = x.greedy_count_bracket(eps)
    print(f"eps=1e-{k}: root z-minimizer {yz}, F_z {Fz}, w_z {wz}; deficit first-phase internal nodes {phase1}, "
          f"deficit total nodes {r['nodes']}; omega first-phase {ophase1}, omega total {ro['nodes']}; "
          f"strip [0,1]x[2/5,3/5] value+eps = {strip} (valid: {strip >= 0}); N_x(eps) in {Nx}", flush=True)
