# Perron–Frobenius / Collatz–Wielandt bounds for the nuclear* instances (18 open)

Date: 2026-09-22. Author: verification agent; saved by the coordinator from the
agent's output (the agent's harness blocked Markdown writes). Status: author
proofs and exact certificates; an [independent review](review-nuclear-bounds.txt)
reproduced all 18 certified values with separate code and found the proofs
correct; its corrections are applied below. Code:
`code/nuc_struct.py`, `code/nuc_verify.py`, `code/nuc_cuts.py`, `code/nuc_solve.py`,
`code/nuc_table.py`; data in `nuclear_cw_bounds.json|txt`, `nuclear_table.txt`,
`nuclear_runs/`.

Update (2026-09-23): the [follow-up assessment](../nuclear-global/assessment.md)
and its [independent review](../nuclear-global/review-assessment.txt) give exactly
certified root bounds that improve the bounds below by 0.22–1.25% on the seven
F1 instances (nuclearva 1.182044, vb 1.184036, vc 1.194607, vd 1.193068, ve
1.189370, vf 1.178376, nuclear14 1.196839, as upper bounds on `lam_T`), and six
improved primal points.

## 1. Model as written

nuclearva and nuclear14a were parsed in full; the other instances were checked
row by row by `code/nuc_verify.py`.

- Nodes `i = 1..N` (N = 14, 24, 25, 49, 104), time steps `t = 1..T` (T = 6, 8, 8, 9, 10).
  `phi_{i,t}` flux, `k_{i,t}` k-infinity, `lam_t` eigenvalue. Objective: `min -lam_T`.
- Eigen rows: `lam_t phi_{i,t} = sum_j G_ij k_{j,t} phi_{j,t}`; `G` has exact decimal
  entries, `G >= 0`, irreducible in all 18 instances.
- Burnup: `k_{i,t+1} = k_{i,t} - a phi_{i,t} k_{i,t}`, `a > 0` (.15288 for va, vb, vd, ve;
  .1862 vc; .1596 vf; .1092 for the 14 and 25 families; .09555 for 49; .084933 for 104).
- Normalization: `sum_i V_i phi_{i,t} k_{i,t} = 1` for every `t` (`V = 1`, or 0.5 on
  diagonal half-nodes in va–vf).
- Peaking: `phi_{i,t} k_{i,t} <= c` (c = 1/6 va; 0.15 vb–vf; 1/12 for 14; 0.08 for 25;
  1/24.5 for 49; 1/52 for 104).
- Sign bounds: `phi, k, lam >= 0` (OSiL default lower bound 0), so `phi >= 0` is
  imposed; `lam` has no upper bound. F2/F3 also have `phi >= phi_lb > 0` and `k >= 0.12`.
- Beginning-of-cycle `k`, three formulations:
  - F1 (va–vf, 14, 25, 49, 104; MacMINLP): fuel types with ages,
    `k_{i,1} = KF [fresh at i] + sum_g y_{i,g} kappa_g`, `kappa_g = sum_j V_j y_{j,pred(g)} k_{j,T}`;
    predecessor chains are acyclic and end in fresh fuel.
  - F2 (14a, 25a, 49a, 10a): `k_{i,1} = KF b0_i + sum_j b_ij k_{j,T}`, one source per node,
    each fuel to at most one node.
  - F3 (14b, 25b, 49b, 10b): `k_{i,1} = KF b0_i + sum_j z_ij`, `z_ij <= k_{j,T}`, `z_ij <= KF b_ij`.
  - In F1 the `kappa` variables (and the continuous copies of binaries in the
    14/25/49/104 F1 models) have lower bound `-INF`; each is set equal to a
    nonnegative expression, so this does not affect the proofs.
  - `KF = 1.2`, except vb, vd, ve, vf (1.25) and vc (1.26).
- Data anomaly: row e1233 of nuclear104 (e1025 of nuclear10a) has G entries
  .1066, .0672, 1.4042, .4532, 1.0312 (sum 3.06); every other row sums to
  `1 ± 3e-4` within the 104 family (the va–vf matrices have row sums from 0.67
  to 1.055; the reviewer confirmed the anomaly: row sum 3.0624, spectral radius 1.4569). Probably a typo in the source data. It inflates `rho(G)` to 1.457.

## 2. Bounds and proofs

**(K) `k_{i,t} <= KF` at every feasible point.** Burnup gives
`k_{i,t+1} = k_{i,t}(1 - a phi_{i,t}) <= k_{i,t}` because `phi, k >= 0`, so it suffices
to show `k_{i,1} <= KF`. F3: `k_{i,1} <= KF (b0_i + sum_j b_ij) = KF` by the node row.
F2: burn is strictly positive (`phi >= phi_lb > 0`, `k >= 0.12`); if
`max_i k_{i,1} > KF` were attained at a reloaded node, it would equal
`k_{j,T} < k_{j,1} <= max`, a contradiction. F1: `kappa_g` is a `V`-weighted
average (the fuel-row coefficients were checked equal to the weights) of
`k_{j,T} <= k_{j,1} = kappa_{pred(g)}`; induction on age gives `kappa <= KF`.

**(CW) `lam_T <= KF max_i (G w)_i / w_i` for any `w > 0`.** The normalization
makes `phi_T != 0`, so `lam_T` is an eigenvalue of `G diag(k_T) >= 0`; then
`lam_T <= rho(G diag(k_T)) <= max_i (G diag(k_T) w)_i / w_i <= KF max_i (G w)_i / w_i`.
This needs neither `phi >= 0` nor irreducibility. The value is certified in
exact rational arithmetic with a rational `w`.

**(P) Peaking-aware bound.** Let `p = phi_T k_T` (componentwise), so `p` lies in
`P = {0 <= p <= c, V^T p = 1}`. For `y >= 0` with `y^T p > 0` for every `p` in `P`
(the certificates for nuclearvd and nuclearve have one zero entry of `y`; the
reviewer verified this condition exactly for both), `lam_T y^T phi_T = y^T G p`, and
`phi_i >= p_i / KF` by (K). Hence `lam_T <= KF max_{p in P} y^T G p / y^T p`.
`y` is chosen by LP bisection; the value is certified exactly by Dinkelbach
iteration with an exact fractional knapsack over the rationals. With `y` the
left Perron vector it is at least as strong as (CW).

Why an assignment-MILP variant does not help (informal argument, not a proof): without a per-node lower bound
on burnup, a relaxation can keep every node near `k = KF`, absorbing the fixed
total burn `a (T - 1)` in low-power nodes, so it gives about `KF rho(G)`, even
with the valid total-burn equalities `sum_i V_i k_{i,t+1} = sum_i V_i k_{i,t} - a`.

## 3. Results

Proven bounds are certified in exact arithmetic (`nuclear_cw_bounds.json|txt`).
The table reports the objective `-lam_T`; its proven-bound column is the certified
upper bound on `lam_T` rounded up to six decimals (so the printed objective
bound is rounded down and remains valid).
Solver runs: 300 s, one thread, Gurobi 13.0.3 and SCIP 10.0. The "cuts"
configuration adds, for every `t`: `k_{i,t} <= KF`; `lam_t <= nu_t` with
`nu_t >= sum_j G_ij w_j k_{j,t} / w_i` for all `i` (a linear form of the
Collatz–Wielandt maximum); `sum_i V_i k_{i,t+1} = sum_i V_i k_{i,t} - a`; and
`lam_T <=` the proven bound. All are valid by (K), (CW) and the row sums.

| instance | listed primal | listed dual | listed gap | proven bound | gap (listed primal, proven bound) | Gurobi dual: no cuts / cuts | SCIP dual: no cuts / cuts | best primal in these runs (max viol) |
|---|---|---|---|---|---|---|---|---|
| nuclearva | -1.01423 | -1e+06 | 9.86e+05 | -1.184634 | 0.168 | -1.69e+04 / -1.15500 | none / -1.18463 | -1.00694 (1.2e-07) |
| nuclearvb | -1.03134 | -1e+06 | 9.7e+05 | -1.195181 | 0.159 | -803 / -1.16551 | none / -1.19518 | -1.02267 (4.6e-15) |
| nuclearvc | -1.00485 | none | inf | -1.204743 | 0.199 | -8.34e+03 / -1.17762 | none / -1.20474 | -0.99826 (1.1e-14) |
| nuclearvd | -1.04165 | none | inf | -1.205524 | 0.157 | -596 / -1.19143 | none / -1.20552 | -1.03676 (1.3e-15) |
| nuclearve | -1.03764 | -1e+06 | 9.64e+05 | -1.202431 | 0.159 | -1.13e+03 / -1.18547 | none / -1.20243 | -1.03403 (1.2e-08) |
| nuclearvf | -1.02409 | -1e+06 | 9.76e+05 | -1.193331 | 0.165 | -713 / -1.16593 | none / -1.19333 | -1.02019 (1.2e-08) |
| nuclear14 | -1.12969 | -1e+06 | 8.85e+05 | -1.200010 | 0.0622 | -2.41e+05 / -1.20001 | none / -1.20001 | -1.12158 (4.2e-10) |
| nuclear14a | -1.12963 | -12.24085 | 9.84 | -1.200010 | 0.0623 | -10.82498 / -1.19634 | -12.25606 / -1.20001 | -1.11821 (5.8e-09) |
| nuclear14b | -1.12759 | -1.19830 | 0.0627 | -1.200010 | 0.0642 | -1.43642 / -1.19619 | -2.23187 / -1.19990 | -1.11922 (3.9e-11) |
| nuclear25 | -1.12066 | none | inf | -1.200005 | 0.0708 | -1e+06 / -1.20000 | none / -1.20000 | -1.10583 (6.0e-13) |
| nuclear25a | -1.12070 | -12.26952 | 9.95 | -1.200005 | 0.0708 | -12.31747 / -1.19675 | -12.31986 / -1.19991 | -1.08464 (2.3e-13) |
| nuclear25b | -1.11580 | -1.19662 | 0.0724 | -1.200005 | 0.0755 | -1.53437 / -1.19679 | -10.84723 / -1.19991 | -1.10806 (1.3e-08) |
| nuclear49 | -1.15142 | none | inf | -1.199970 | 0.0422 | none / -1.19997 | none / -1.19997 | -1.13801 (7.3e-07) |
| nuclear49a | -1.15149 | -12.35896 | 9.73 | -1.199970 | 0.0421 | -12.35986 / -1.19985 | -12.35979 / -1.19992 | none |
| nuclear49b | -1.14692 | -1.20177 | 0.0478 | -1.199970 | 0.0463 | -12.35954 / -1.19985 | -8.61011 / -1.19992 | -1.13151 (3.3e-15) |
| nuclear10a | none | -12.33361 | inf | -1.202131 | inf | -12.33432 / -1.20210 | -521 / -1.20211 | none |
| nuclear10b | -1.16521 | -4.87040 | 3.18 | -1.202131 | 0.0317 | -12.28620 / -1.20207 | -519 / -1.20211 | none |
| nuclear104 | none | none | inf | -1.202131 | inf | none / -1.20213 | none / -1.20213 | none |

Observations:
- The proven bounds make every gap finite where a feasible value is known (not
  for nuclear10a and nuclear104, which have no known feasible point): 16–20% on va–vf, 4–7.5% on the
  14/25/49 families, 3.2% on 10b. Listed gaps were infinite, about 1e6, or about 10.
- They improve the listed dual bound on every instance except 14b and 25b,
  where the listed values 1.1983 and 1.1966 are about 0.2% better. On 49b the
  bound 1.19997 beats the listed 1.20177.
- The origin of the b-variant listed dual bounds is not explained here (an
  earlier explanation was unsupported and has been removed).
- Gurobi with the cuts goes beyond the constant bound (va 1.1550, vb 1.1655,
  vc 1.1776, vd 1.1914, ve 1.1855, vf 1.1659, 14a 1.1963, 14b 1.1962, 25a
  1.1968, 25b 1.1968). Without the cuts Gurobi's dual bounds were -1.7e4 to -596
  on va–vf and about -12 on the a-variants; SCIP had no finite dual bound on
  va–vf, 14, 25 or 49. SCIP with the cuts stays essentially at the added cap.
  Solver bounds are floating-point claims, not certificates.
- No new primal values beat the listed ones; the 104-node instances got no
  primal point in 300 s.

## 4. Literature (via a research subagent; not re-read by the author)

- Quist, de Klerk, Roos, Terlaky, van Geemert, Hoogenboom, Illés, "Finding
  optimal nuclear reactor core reload patterns using nonlinear optimization
  and search heuristics", Engineering Optimization 32(2):143–176, 1999: the
  model behind the instances; no bounds; global optimality called "extremely
  difficult" to guarantee.
- de Klerk, Roos, Terlaky, Illés et al., "Optimization of nuclear reactor
  reloading patterns", Annals of OR 69:65–84, 1997: `k_eff` fixed to 1,
  burn-up maximized; a 1-norm (maximum column sum of `G`) bound on the eigen
  equation bounds burn-up 15–20% above the best solutions; a Shor SDP is
  proposed but not solved.
- No Perron–Frobenius or Collatz–Wielandt bounds on `k_eff` were found for
  reload patterns. Quist's 2000 thesis was not checked. The bounds for these
  instances therefore appear new, but the search was not exhaustive, and the
  mathematics is classical.
