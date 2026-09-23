# Independent check of scout claims: polygon, knp, mpbp_06, waternd_shamir

Date: 2026-09-22. Author: independent verification agent. The coordinator saved
this report from the agent's output because the agent's harness blocked
writing Markdown files. No scout code was reused. `code/osil_eval.py` is a new
OSiL parser and evaluator that reads every bound and coefficient as a decimal
string and evaluates in float, mpmath (any precision) or exact sympy
arithmetic. Listed bounds come from `../scouting/minlplib-open-data/open.csv`.
Gaps use the MINLPLib convention `|p - d| / min(|p|, |d|)`, which reproduces
the listed gaps.

These are benchmark observations based on classical theorems and exact
constructions. They are not new mathematics.

## Summary

| Instance | Listed primal / dual | Result | Status |
|---|---|---|---|
| polygon25 | -0.7797510481 / -5.7997 | regular 25-gon feasible, objective -0.780232078883181; optimal by Reinhardt | solved, gap 0 |
| polygon75 | -0.7844637573 / -24.874 | regular 75-gon feasible, objective -0.784823993232737; optimal | solved, gap 0 |
| polygon50 | -0.7838751084 / -15.268 | primal -0.784053075884516 (49-gon, one vertex doubled); dual -0.784156496533871 | gap 18.5 -> 1.32e-4 |
| polygon100 | -0.7850561376 / -33.999 | primal -0.785068630140769; dual -0.785081551496788 | gap 42.3 -> 1.65e-5 |
| knp3-12 | 1.105572809 / 2.2807 | icosahedron `2 - 2/sqrt 5` (exact); optimal (Fejes Tóth 1943) | solved; listed primal is optimal |
| knp4-24 | 1.0 / 3.676 | 24-cell gives 1 exactly (= listed primal); optimality is the open 24-cell conjecture | dual open |
| knp5-40 | 0.9848552014 / 4.0 | D5 gives 1 exactly (+0.01514) | primal improved; dual open |
| knp5-41..44 | 0.969..0.945 / 4.0 | a dual below 1 would prove the kissing number `tau_5 <= N - 1` (`tau_5` known only to lie in 40..44) | see Section 2 |
| mpbp_06 | none | SCIP 10.0 and Gurobi 13.0.3 both report optimal 337.155 | confirmed by two solvers |
| waternd_shamir | 419000 / none | SCIP 10.0 reports optimal 419000 | confirmed by one solver |

## 1. polygon

Model (verified by parsing): variables `r_1..r_N` and `theta_1..theta_N`;
`r_N` has upper bound 0, so vertex `N` is at the origin and the polygon has `N`
vertices; `0 <= r <= 1`, `0 <= theta <= 3.14159265358979` (a decimal about
3e-15 below pi), `theta_N` fixed at that decimal; `theta_i <= theta_{i+1}`;
for all `i < j`, `r_i^2 + r_j^2 - 2 r_i r_j cos(theta_j - theta_i) <= 1`, that is
`|P_i - P_j|^2 <= 1` (the pairs `(i, N)` give `|P_i| <= 1`). Objective:
`min -1/2 sum_{i<N} r_i r_{i+1} sin(theta_{i+1} - theta_i)`, minus the area of the
fan polygon `O, P_1, ..., P_{N-1}`.

Construction (`code/polygon.py`, `polygon_out.txt`): for odd `m`,
`V_k = c (w^k - 1)` with `w = e^{2 pi i / m}` and `|c| = 1/(2 cos(pi/2m))` is a
regular `m`-gon with `V_0 = 0`. In polar form `r_k = sin(k pi/m)/cos(pi/2m)` and
`theta_k = k pi/m`, inside the bounds. The distances are
`|V_i - V_j| = sin(pi |i-j|/m)/cos(pi/2m)`, with maximum exactly 1 at
`|i - j| = (m ± 1)/2`. For even `N`, use `m = N - 1` and duplicate vertex 1 (a
zero-length edge, allowed because `theta_1 = theta_2`). 60-digit check: maximum
row violation 1.6e-61 (3.1e-61 for N = 100), no bound violation, exactly `m`
rows with `|d^2 - 1| < 1e-40`; the objective equals `-A_reg(m)` to 20 digits,
where `A_reg(m) = (m/2) R^2 sin(2 pi/m)`, `R = 1/(2 cos(pi/2m))`.

Dual bounds. Reinhardt, "Extremale Polygone gegebenen Durchmessers",
Jahresber. DMV 31 (1922) 251–270: for odd `n`, the regular `n`-gon has maximum
area among `n`-gons of diameter 1. Applicability: the angles are ordered in
`[0, pi)`, so every sine is nonnegative and the fan triangles do not overlap;
their total area is at most the area of the convex hull, which has at most `N`
vertices and diameter at most 1; polygons with fewer vertices are limits of
`N`-gons of diameter at most 1. Odd `N`: the optimal value is exactly
`-A_reg(N)`. Even `N`: an `N`-gon is a degenerate `(N+1)`-gon, which gives the
dual bound `-A_reg(N+1)`. The upper bound on `theta` below pi only shrinks the
feasible set. The isodiametric inequality (Bieberbach, Jahresber. DMV 24
(1915) 247–250; area at most pi/4 for diameter 1) gives the weaker dual bound
-0.785398163397448 and listed-primal gaps 7.24e-3, 1.94e-3, 1.19e-3, 4.36e-4,
confirming the scout.

| N | listed primal | our primal | our dual | listed gap | our gap |
|---|---|---|---|---|---|
| 25 | -0.7797510481 | -0.780232078883181 | -0.780232078883181 | 6.44 | 0 |
| 50 | -0.7838751084 | -0.784053075884516 | -0.784156496533871 | 18.5 | 1.32e-4 |
| 75 | -0.7844637573 | -0.784823993232737 | -0.784823993232737 | 30.7 | 0 |
| 100 | -0.7850561376 | -0.785068630140769 | -0.785081551496788 | 42.3 | 1.65e-5 |

Caveats: better even-`n` constructions exist in the literature and were not
reproduced (Mossinghoff, DCG 2006; Bingane and Audet). Even-`n` optima are
known only for `n <= 12` (Graham 1975; Audet, Hansen and Messine 2002;
Henrion and Messine 2013). Optimality here rests on a theorem plus an exact
construction, not on a solver.

## 2. knp

Model (verified): `||x_i||^2 = 4`, `x` in `[-2,2]^D`, and
`||x_i - x_j||^2 - 4 objvar >= 0` for all pairs; maximize `objvar`. Hence the
optimum is `max over N-point codes of min_{i<j} ||x_i - x_j||^2 / 4 = 2 - 2 cos(theta_min)`,
and `objvar >= 1` exactly when `N <= tau_D` (the kissing number).

Exact sympy checks (`code/knp.py`, `knp_out.txt`), all rows and bounds hold
exactly: knp3-12 (icosahedron) `2 - 2 sqrt5/5 = 1.10557280900008`; knp4-24
(Hurwitz units `(±2,0,0,0)` and `(±1,±1,±1,±1)`) 1; knp5-40 (D5 roots scaled by
`sqrt 2`) 1.

Dual side: knp3-12 is the Tammes problem for 12 points, solved by Fejes Tóth
(1943), so the optimum is exactly 1.1055728090000841. knp4-24: Musin proved
`tau_4 = 24`, but optimality of the 24-point code is the open 24-cell
conjecture (Musin, arXiv:1712.04099); D4 is not universally optimal (Cohn,
Conway, Elkies and Kumar 2007). knp5-40: no known proof that D5 is an optimal
40-point code. knp5-41..44: a dual bound below 1 would prove `tau_5 <= N - 1`,
which is open (`tau_5 <= 44` from Bachoc–Vallentin 2008 and
Mittelmann–Vallentin 2010); an objective of at least 1 would be a new kissing
configuration. The scout's Delsarte numbers were not re-checked and remain
uncertified.

## 3. mpbp_06 and waternd_shamir

`code/scip_check.py`: SCIP 10.0 through PySCIPOpt 6.2.1 reading the OSiL, one
thread, default settings. `code/grb_check.py`: Gurobi 13.0.3 with a separate
model builder (`grb_build.py`), `NonConvex = 2`, one thread. Every incumbent was
evaluated by `osil_eval` in float and 50-digit arithmetic over all bounds, rows
and integrality.

| Instance | Run | Status | Time | Nodes | Objective | Max violation |
|---|---|---|---|---|---|---|
| mpbp_06 (max) | SCIP feastol 1e-6 | optimal | 31.7 s | 5426 | 337.155041061 | 5.0e-7 (e154) |
| mpbp_06 | SCIP feastol 1e-9 | optimal | 36.5 s | 4256 | 337.155000061 | 9.5e-10 |
| mpbp_06 | Gurobi 13 | optimal, gap 0 | 6.2 s | 1018 | 337.155000112 | 9.7e-9 |
| waternd_shamir (min) | SCIP 1e-6 | optimal | 7.6 s | 5121 | 419000 | 7.5e-7 (e12) |
| waternd_shamir | SCIP 1e-9 | optimal | 5.7 s | 3163 | 419000 | 5.4e-13 |

Integrality violation is 0 in every run. The extra 4e-5 in mpbp_06 at feastol
1e-6 is tolerance slack. The waternd_shamir objective is an integer-cost
combination of binaries, so 419000 is exact for the returned point.
"Optimal" is a floating-point claim from spatial branch and bound, not an exact
certificate; waternd_shamir was checked only with SCIP.
