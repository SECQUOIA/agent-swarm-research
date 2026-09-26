# Brainstorm 2: structural theorems that solvers cannot derive but can detect (2026-09-23)

Lens: generalize the nuclear (Perron–Frobenius) and waterno2 (moment curve) wins into
solver-level techniques of the form *detectable pattern + theorem + separation*.
Author: brainstorm agent. Status: proposals, pattern counts from a parser run over the
open instances, two numerical feasibility probes. Nothing here is independently reviewed.

## 0. Method and data

- Instances: the 538 rows of `minlplib-open-data/open.csv`, OSiL files in
  `~/.cache/minlplib/minlplib/osil/` (files over 40 MB skipped: hadamard_9,
  acopf_caseactivsg25k/70k and a few others; 480 parsed).
- Parser: `minlplib-open-data/osil.py`. Detectors written for this note (scratch copies in
  `/tmp/bs2/`, not kept in the repository):
  - *eigen pattern*: a continuous variable `lam` that occurs in exactly one bilinear term
    `lam * x_i` in each of at least 4 equality rows, where each row also contains at least two
    other members of the set `X = {x_i}`;
  - *curve pattern*: a variable that occurs in at least two distinct univariate nonlinear
    atoms (for example `x^2` and `x^3`, `sin x` and `cos x`, `exp x` and `x^2`);
  - *unbounded trig*: variables inside `sin`/`cos` with an infinite declared bound.
- Detector counts are rough: they are syntactic and were spot-checked, not audited.

## 1. The eight candidate directions

Each entry: pattern; theorem; how cuts or bounds are generated; instances and applications;
expected effect; what is known; risk.

### D1. Positive-definite kernel aggregation for point configurations (Delsarte–Yudin–Cohn–Elkies)

- **Pattern.** `N` point variables `x_i in R^d` with `||x_i||^2 = 1` (or a ball), and an
  objective or constraints that depend on the points only through a radial function of
  pairwise inner products or distances, summed over pairs or taken as a min/max. The model is
  symmetric under permutations of the points and under `O(d)`.
- **Theorem.** Schoenberg: for Gegenbauer polynomials `G_k^{(d)}`, the matrix
  `(G_k(<x_i,x_j>))_{ij}` is PSD, so `sum_{i,j} G_k(<x_i,x_j>) >= 0` for every configuration.
  Consequence (Delsarte–Yudin): if `h = sum_k h_k G_k` with `h_k >= 0` for `k >= 1` and
  `h(t) <= f(t)` on `[-1, 1)`, then `sum_{i != j} f(<x_i,x_j>) >= N^2 h_0 - N h(1)`.
  The same argument with `f` replaced by a feasibility indicator gives the Delsarte LP bound
  for codes (kissing numbers, Tammes). The three-point SDP (Bachoc–Vallentin) is stronger.
- **Cut/bound generation.** Detect the family; solve a small LP over `h` (one per `(N, d, f)`);
  certify `h <= f` on `[-1,1)` with an interval or Lipschitz argument; add the objective cut
  `obj >= bound` (or `obj <= bound` for max-min codes). Inside branch and bound the degree-`k`
  aggregated inequalities can be added as valid polynomial constraints in Gram variables, but
  the root objective cut is where the effect is.
- **Instances.** elec (4 open: elec25/50/100/200), knp (7), plus weaker fits: pointpack (3),
  maxmin, orth_d (2), ball_mk4_15, kall_* and ringpack only if the container is a sphere or
  ball (mostly it is not). Applications: point distribution on spheres (Thomson, Tammes),
  spherical codes, antenna and sensor placement, quadrature design, molecular and colloid
  models on spheres.
- **Effect.** Very large where it applies (probe in §2.1): elec gaps drop from 170–220% to
  0.03–0.07% with a probe bound (not exactly certified; see §4). For knp the
  earlier uncertified scout LP gave dual bounds 1.02–1.07 instead of the listed 4.0.
- **Known.** The mathematics is classical: Delsarte, Goethals and Seidel (1977); Yudin (1992);
  Kolushov and Yudin; Andreev; universal lower bounds by Boyvalenkov, Dragnev, Hardin, Saff and
  Stoyanova (arXiv:1503.07228); moment/SDP bounds for Riesz energy by de Laat
  (arXiv:1610.04905). I found no MINLP solver that detects the pattern and adds these bounds;
  MINLPLib's listed elec dual bounds are far weaker.
- **Risk.** The mathematics carries little risk. Scope risk is real: sphere or ball
  containers only; square containers (pointpack, maxmin) need different bounds, and Oler's
  inequality is weaker than the listed bounds for pointpack10. Novelty is in the solver
  technique and certification, not in the theorem.

### D2. Matrix-function recognition: determinants and Perron roots hidden in polynomials

- **Pattern.** (a) A multilinear polynomial whose monomials are exactly the permutation
  products `prod_i b_{i,pi(i)}` with signs `sgn(pi)`: a Leibniz determinant of a matrix of
  variables. It can be confirmed by random evaluation against `det`. (b) The eigen pattern
  `lam x_i = sum_j a_ij(y) x_j` with `a_ij >= 0` (nuclear).
- **Theorems.** (a) Hadamard `|det A| <= prod_i ||a_i||`; for ±1 matrices of order `m` the
  Barba bound (`m` odd), the Ehlich–Wojtas bound (`m = 2 mod 4`) and the Ehlich bound
  (`m = 3 mod 4`); the bijection between 0/1 matrices of order `n` and ±1 matrices of order
  `n+1` (`D_{±1}(n+1) = 2^n D_{01}(n)`); integrality of `det` for integer matrices.
  Fischer and Oppenheim inequalities cover PSD cases. (b) Collatz–Wielandt min-max;
  Kingman/Cohen log-convexity of `rho` in log-parameters; monotonicity of `rho` in the entries
  of a nonnegative matrix.
- **Cut/bound generation.** (a) Objective cut `obj <= floor(bound)`; row-norm cuts
  `|det| <= prod ||a_i||` for bounded variable boxes. (b) Collatz–Wielandt cuts with test
  vectors `w` from the node's box, and the peaking-aware bound already used for nuclear.
- **Instances.** (a) hadamard_6..9 (4 open). (b) nuclear* (18 open; the stricter detector finds
  exactly the 18 nuclear instances, plus orth_d3m6_pl with 6 rows (probably not a true eigen
  system) and arki0004 (a GARCH recursion, not an eigen system; see D5)). Applications:
  D-optimal experimental design and weighing designs (determinant), reactor physics,
  Leslie-matrix population growth rates, epidemic `R0` (next-generation matrix), Markov-chain
  and Leontief models.
- **Effect.** Probe in §2.2: hadamard_7 and hadamard_9 close exactly (gap 0) from Hadamard and
  Ehlich–Wojtas; hadamard_6 closes exactly from Ehlich's bound plus integrality; hadamard_8
  drops from a listed dual 14267.6 to 65 (primal 56, gap 16%). The remaining gap is covered
  by the published optimality of 56 (order-9 ±1 value 14336), which rests on a combinatorial
  proof, not a closed-form bound. Nuclear results are in `benchmark-observations/nuclear-bounds.md`.
- **Known.** All determinant bounds are classical (Hadamard 1893; Barba 1933; Ehlich 1964;
  Wojtas 1964; survey by Browne et al., arXiv:2104.06756; OEIS A003432). I found no solver
  that recognizes a determinant in expanded form. For Perron roots in MINLP I found no
  prior cuts beyond this project's nuclear work (quick search only).
- **Risk.** MINLPLib breadth is small (22 instances). The determinant detector matters only
  for expanded determinants, which appear mainly in benchmark sets. The Perron part is
  broad in applications, and the parameterized form (entries depending on design variables,
  as in nuclear) is where a general theory could be new.

### D3. Joint curve hulls for variables with several univariate atoms (moment-curve generalization)

- **Pattern.** A variable `x` with several atoms `f_1(x), ..., f_m(x)` in different rows or with
  different signs, for example `(x, x^2, x^3)`, `(sin x, cos x)`, `(x^2, exp x)`, `(x^a, x^b)`.
  Solvers relax each atom separately, which loses the joint hull of the curve
  `{(x, f_1(x), ..., f_m(x))}`.
- **Theorem.** For Chebyshev systems (`1, x, ..., x^m`; `1, cos, sin` on an arc of length
  below `2 pi`; `1, x^a, x^b`) the hull of the curve over an interval is described by
  Karlin–Shapley/Krein moment theory: explicit facets (lower and upper principal
  representations) and, for polynomials, PSD Hankel conditions. The waterno2 success used the
  `(x, x^2, x^3)` case.
- **Cut/bound generation.** Separate a point `(x*, f*)` from the curve hull by an LP over
  facet-defining secants (few breakpoints for `m <= 3`) or by a tiny SDP with an
  eigenvector-derived linear cut.
- **Instances (detector).** Genuine multi-atom variables in about 30 open instances: waterno2 (5;
  `x^2, x^3`), gams02 (192 variables with `x^2, x^3`), ghg_2veh/3veh, chp_partload, super3t,
  4stufen, beuster, uselinear, ex8_1_4/5, ex8_4_2, ex8_5_*, ex8_6_1 (`x^3, x^6`), feedtray,
  wastepaper5/6, water/waterx, rocket (4; `exp, x^2`), lnts (4) and truck (`sin, cos`),
  kriging_peaks (`exp, sqrt`), blendgap (`erf, exp`). (The detector also flags
  transswitch and lukvle, but those are only `x^2` written in two ways.)
  Applications: water and gas networks (friction laws), process models with polynomial
  correlations, trajectory models with `(sin, cos)` of a heading angle.
- **Effect.** Proven large on waterno2 (Gurobi dual above MINLPLib's best known). Unknown on
  the others; the gams02 gap is only 2.7%, rocket gaps are 1.4–818% (rocket400 with an 8x gap).
- **Known.** The hull of the moment curve is classical (Karlin–Studden). The generic solver
  technique "detect a variable's curve and add joint-hull cuts" is not in SCIP; SCIP
  and BARON treat atoms separately. Recent related work: axis-aligned and simultaneous-hull
  relaxations (arXiv:2603.18458).
- **Risk.** Medium-low. The gain requires the atoms to pull in different directions;
  if all atoms of `x` lie in one row, a univariate envelope of that row's polynomial suffices.

### D4. Periodicity and rotation symmetry for trigonometric models (automatic polar-to-rectangular lifting)

- **Pattern.** Angle variables that occur only inside `sin`/`cos`, often only through differences
  `theta_i - theta_j`, with infinite bounds. The detector finds 5,686 unbounded trig variables
  in each of 9 powerflow and 9 transswitch instances, plus deb (5), var_con (2) and truck.
- **Theorems.** (i) Periodicity: if `theta` occurs only in `2 pi`-periodic functions, restricting
  it to `[-pi, pi)` is exact. (ii) Rotation invariance: if the model depends only on differences,
  one angle can be fixed to 0. (iii) Lifting: `V_i V_j cos(theta_i - theta_j) = e_i e_j + f_i f_j`
  with `e = V cos theta` and `f = V sin theta`, which exposes the rectangular QCQP and its
  SOC/QC relaxations. (iv) The joint hull of `(cos, sin)` on an arc is a circular segment
  (D3).
- **Cut/bound generation.** Presolve reformulation plus arc-hull cuts; angle-difference bounds
  from line data.
- **Instances.** powerflow polar variants: `p` versions have dual bounds 0 or near 0 (for
  example powerflow0030p: dual 0, while the rectangular 0030r has dual 575.2 against primal
  576.9); transswitch p/r (18, most with dual 0); deb (5, dual 0). Applications: AC power
  flow and switching, robotics and kinematics, trajectory design.
- **Effect.** Potentially large on the polar variants, since the rectangular forms of the
  same models have small gaps. Switching binaries in transswitch are a separate obstacle.
- **Known.** The polar/rectangular equivalence and QC relaxations are well known in power
  systems (Coffrin, Hijazi, Van Hentenryck). What is missing is automatic detection in general
  solvers. This is mostly implementation, with little new theory.
- **Risk.** Low mathematical risk, low novelty. The effect is limited to the gap between the
  polar and rectangular forms.

### D5. Monotone (Metzler / nonnegative) implicit recursions: comparison bounds

- **Pattern.** Recursions `z_{t+1} = A(p) z_t + b(p)` or implicit systems `F(z, p) = 0` whose
  Jacobian in `z` is a Z-matrix/M-matrix (Metzler dynamics), with parameters `p` in a box.
  Examples: full discretizations of cooperative ODEs (catmix; parts of methanol, gasoil,
  pinene), GARCH variance recursions (arki0004: `h_t = omega + sum alpha eps^2 + sum beta h`
  with 1,038 rows), the nuclear burnup recursion, potential-flow networks with monotone
  head loss.
- **Theorem.** Kamke–Müller comparison, discrete version: if `A(p) >= 0` entrywise and is
  monotone in `p`, then `z_t(p)` is monotone in `p` and in the initial state, so state bounds
  come from simulating two extreme parameter vectors. For M-matrix implicit systems, the
  inverse-positivity of the Jacobian gives the same monotonicity.
- **Cut/bound generation.** Presolve: detect the sign pattern, run two forward simulations,
  and install finite state bounds. Optionally add secant cuts along the monotone map.
- **Instances.** Discretized dynamic models: 51 open, 26 with infinite gap (scout §2.2; no state
  bounds in the files). arki0002/0004/0011–0014 (econometric likelihoods; arki0004 has dual
  -3058.5 against primal 323.5).
- **Effect.** Turns missing bounds into finite ones, which is what currently blocks
  relaxations. For least-squares estimation (gasoil, methanol, pinene) the objective bound 0
  is already valid, so the dual-bound gain may be small; for control (catmix) it can turn an
  infinite gap into a finite one.
- **Known.** Continuous-time differential-inequality bounds are well developed (Scott and
  Barton; Harwood et al. on invariants, MCSS 2020). Full-discretization MINLPs do not use
  them. Novelty is moderate (discrete-time, detection from the algebraic model).
- **Risk.** Medium: many kinetic models are not cooperative, and bounds from extreme
  parameters can be loose over wide parameter boxes.

### D6. Linear first integrals (conservation laws) in discretized dynamics

- **Pattern.** In time-stepped rows `x_{t+1} = x_t + h S r(x_t, u_t)`, a vector `w` with
  `w^T S = 0` exists (stoichiometric conservation), or `w^T S <= 0` holds together with
  nonnegativity (for example catmix: `x1 + x2` is nonincreasing).
- **Theorem.** `w^T x_t = w^T x_0` (or monotone) for every feasible trajectory; with positive
  invariance of the nonnegative orthant this gives a simplex-type box for every state.
- **Cut/bound generation.** Compute the left null space of the rate-coefficient pattern from the
  rows (linear algebra on the Jacobian sparsity with symbolic rates); add the invariant rows
  and the derived bounds.
- **Instances.** Same dynamic family as D5 (catmix 4, methanol 4, gasoil 4, pinene 3,
  popdynm 4, among others).
- **Effect.** Finite state bounds, as in D5; the objective effect depends on the instance.
- **Known.** Standard in reaction-network theory and in dynamic-optimization bounding
  (Harwood, Scott and Barton). It is not automated in MINLP presolve.
- **Risk.** Low mathematical risk; the gain may be only finite but weak bounds.

### D7. Hidden integer-valued forms in binary polynomial models (integrality and parity)

- **Pattern.** A polynomial in binaries whose value, or whose component forms, are integers with
  known residues: `det` of a 0/1 matrix is an integer; in low-autocorrelation models each
  correlation `C_k = sum_i s_i s_{i+k}` is an integer with `C_k = N - k (mod 2)`, and mod-4
  residues depend on sequence end points.
- **Theorem.** Integrality, parity and mod-4 identities; for a convex function of an integer
  form, the integer hull of `(C, C^2)` (secants between consecutive feasible residues).
- **Cut/bound generation.** Introduce `C_k` as integer variables with parity constraints and
  secant cuts, or round the objective bound to the lattice of attainable values.
- **Instances.** autocorr_bern (29 open, gaps 13–650%), hadamard (4; integrality is used in
  D2), possibly sporttournament.
- **Effect.** Unknown. I could not reproduce the exact autocorr_bern objective: in ±1 form
  it has only degree-2 and degree-4 terms and a constant of -14560 (autocorr_bern30-15), but
  it is not `sum_k w_k C_k^2` for the plain open or cyclic autocorrelations. The model of
  Liers et al. (2010) uses a tunable interaction range, which needs checking.
- **Known/caveat.** MINLPLib's page for autocorr_bern30-15 now lists a PQCR dual bound equal to
  the primal (-15744), so `open.csv` may be stale for at least this instance. For
  autocorr_bern60-60, PQCR's dual (-496,399) is much higher than the listed best (-2,627,102
  from BARON), for reasons not checked here. Dedicated binary polynomial methods (PQCR,
  QCR-type) are the competition here.
- **Risk.** High on effect, and the family is narrow.

### D8. Homogeneity and scaling symmetry: normalization detection

- **Pattern.** Constraint blocks that are positively homogeneous in a group of variables
  (eigen equations, ratio/proportion models, pooling with proportions, pairwise-energy
  objectives with scale-free constraints), together with one normalization row.
- **Theorem.** Scaling symmetry: any normalization that meets every orbit is exact, so the
  solver can choose the normalization that gives the tightest relaxation (for example
  `max_i x_i = 1` instead of `sum V_i phi_i k_i = 1` in eigen models, which gives
  `x in [0,1]` bounds), and homogeneous degree arguments give objective scaling bounds.
- **Instances.** nuclear (18), pooling proportion formulations (about 30), a few others.
  Counts are not verified.
- **Effect.** Small to moderate (it changes bounds, not the relaxation class).
- **Known.** Scaling symmetry is used by hand in modeling; I found no automatic treatment in
  solvers.
- **Risk.** Low novelty and uncertain effect.

## 2. Feasibility probes for the top two

### 2.1 D1 on elec (Thomson problem, Coulomb energy on the unit sphere in R^3)

The model was checked in elec25: points `x_i` with `||x_i||^2 = 1` (equality rows), objective
`sum_{i<j} 1/||x_i - x_j||`, minimize. With `t = <x_i, x_j>`, `f(t) = (2 - 2t)^{-1/2}`, and
Legendre polynomials (the Gegenbauer case for `d = 3`), the LP

`max (N^2 h_0 - N h(1)) / 2  s.t.  h = sum_{k<=K} h_k P_k,  h_k >= 0 (k >= 1),  h <= f on a grid`

was solved with Gurobi. The resulting `h` was then checked on 2,000,001 points of
`[-1, 1 - 1e-9]` with the Lipschitz margin `L = sum_k h_k k(k+1)/2` (valid because
`|P_k'| <= k(k+1)/2` and `f` is increasing). The maximum violation `v` was then subtracted
from `h`, which keeps the bound valid. The subtraction lowers `h_0` and `h(1)` by the same `v`.
The last cell `[1 - 1e-9, 1)` is safe because `f >= 2.2e4` there, far above `h(1)`.
Rounding error in floating-point evaluation is not controlled; exact certification would
take rational or interval evaluation.

| instance | listed primal | listed dual | safe LP bound (K = 40) | new gap |
|---|---|---|---|---|
| elec25 | 243.8128 | 90.23 | 243.636 | 0.07% |
| elec50 | 1055.1823 | 359.03 | 1054.813 | 0.03% |
| elec100 | 4448.3506 | 1429.50 | 4447.077 | 0.03% |
| elec200 | 18438.8769 | 5744.71 | 18431.748 | 0.04% |

The listed gaps (170–221%) drop to 0.03–0.07%, with bounds from a well-known theorem that
generic solvers cannot derive. K = 20 gives nearly the same values (18418.98 for elec200). With
knp (earlier uncertified LP, listed dual 4.0 -> 1.02–1.07) this family covers 11 open
instances with gap reductions of one to four orders of magnitude.

Probe code (scratch, `/tmp/bs2/yudin.py`, abridged):

```python
t = grid on [-1, 0.999] plus points near 1; P[i,k] = P_k(t_i) (numpy legendre)
LP: h_0 free, h_k >= 0; sum_k P[i,k] h_k <= f(t_i); maximize (N^2 h_0 - N sum_k h_k)/2
check: viol = max_i ( h(tt_i) + L*dt - f(tt_i) ) on 2e6+1 points; bound uses h - viol
```

### 2.2 D2 on hadamard_6..9 (maximum determinant of a 0/1 matrix)

Check: for n = 6 and 7 the constraint polynomial equals `det(B)` (row-major 0/1 matrix `B`) on
200 random 0/1 matrices, and the objective is `max objvar` with `objvar <= det(B)`.
hadamard_8 and _9 have the same generator (files of 7 MB and 74 MB, not evaluated).
With `m = n + 1` and `D_{01}(n) = D_{±1}(m) / 2^n`, plus integrality of `det`:

| instance | listed primal | listed dual | classical bound (0/1 units) | rounded | status |
|---|---|---|---|---|---|
| hadamard_6 (m = 7, 3 mod 4) | 9 | 25 | Ehlich: 9.165 | 9 | closed |
| hadamard_7 (m = 8) | 32 | 721 | Hadamard: 4096/2^7 = 32 | 32 | closed |
| hadamard_8 (m = 9, odd) | 56 | 14267.6 | Barba: sqrt(17) 8^4/2^8 = 65.97 | 65 | gap 16% |
| hadamard_9 (m = 10, 2 mod 4) | 144 | none | Ehlich–Wojtas: 18 * 8^4/2^9 = 144 | 144 | closed |

The Ehlich value for m = 7 uses s = 5, r = 1, v = 2, u = 3:
`det^2 <= 4^2 * 8^3 * 12^2 * (1 - 3/8 - 4/12) = 344064`, so `det <= 586.6`, and
`586.6 / 64 = 9.165`. This matches Wikipedia's "9 is 98.2% of the Ehlich bound". The
optimum 56 for n = 8 (±1 order 9: 14336) is established in the literature (credited to
Ehlich and Zeller in the survey tables; I did not check the original). So all four
instances are resolved by published results, three of them by one-line closed-form
bounds. Like polygon25/75, this is a benchmark fact from classical mathematics. The
solver-level part is recognizing a determinant in expanded Leibniz form.

## 3. Ranking

Score = (effect where it applies) x (breadth in MINLPLib and applications) x (novelty as a
solver technique) / risk.

1. **D1 PD-kernel aggregation**: probed; probe bounds (floating point with a Lipschitz
   margin, not exactly certified; see §4) cut elec gaps from about 200% to
   below 0.1%, and the earlier uncertified scout LP cut knp duals from 4.0 to about 1.05;
   about 11 open instances directly and a clear application class. The theorem is
   classical; the new part is detection, certification and use in a solver.
2. **D2 Matrix-function recognition (determinants and Perron roots)**: probed; hadamard closes
   3 of 4 exactly and the fourth goes from a 254x gap to 16%. With nuclear, 22 open instances.
   Breadth in applications (design of experiments, population and epidemic models, reactor
   physics) is larger than in MINLPLib. The parameterized Perron case offers new theory.
3. **D3 Joint curve hulls**: proven once (waterno2), about 30 candidate open instances, cheap
   separation; next step is a probe on rocket400, gams02 and the ex8 instances.
4. **D4 Periodicity and rotation lifting for trig**: large effect likely on polar power-flow
   variants (dual 0 against rectangular duals within 0.3%), but mostly implementation.
5. **D5 Monotone recursions (comparison bounds)**: addresses the "no state bounds" blocker for
   26 infinite-gap dynamic instances and the econometric arki models; the effect on
   objective bounds is uncertain.
6. **D6 Conservation laws**: cheap, same family as D5; likely finite but weak bounds.
7. **D7 Hidden integer forms and parity**: 29 autocorr instances, but the objective could
   not be reconstructed, the data may be stale, and PQCR is strong competition.
8. **D8 Homogeneity normalization**: small, uncertain effect.

## 4. Caveats

- Probe bounds are floating-point with a Lipschitz safety margin; exact rational
  certification of the elec bounds has not been done. For hadamard the bounds are closed-form
  and exact, but hadamard_8 and _9 were not evaluated against `det` directly.
- Detector counts are syntactic and approximate.
- `open.csv` may be out of date (autocorr_bern30-15 now has a matching PQCR dual on the
  MINLPLib page).
- Literature checks were short web searches; "not found" means not found in those searches.

## Sources

- Hadamard's maximal determinant problem (bounds, tables): https://en.wikipedia.org/wiki/Hadamard%27s_maximal_determinant_problem
- Browne et al., A survey of the Hadamard maximal determinant problem: https://arxiv.org/pdf/2104.06756
- OEIS A003432 (maximal determinant of 0/1 matrices): https://oeis.org/A003432
- Boyvalenkov, Dragnev, Hardin, Saff, Stoyanova, Universal lower bounds for potential energy of spherical codes: https://arxiv.org/pdf/1503.07228
- de Laat, Moment methods in energy minimization: https://arxiv.org/pdf/1610.04905
- Asymptotic LP lower bounds for Riesz and Gauss energies (Mathematika): https://www.cambridge.org/core/journals/mathematika/article/abs/asymptotic-linear-programming-lower-bounds-for-the-energy-of-minimizing-riesz-and-gauss-configurations/6DEB11C2C24C46F0DD05FB7C0C314872
- Exploiting nonlinear invariants and path constraints for reachable-set enclosures (MCSS 2020): https://link.springer.com/article/10.1007/s00498-020-00254-y
- Axis-aligned relaxations for MINLP: https://arxiv.org/html/2603.18458
- MINLPLib instance pages: https://www.minlplib.org/autocorr_bern30-15.html, https://www.minlplib.org/autocorr_bern60-60.html
