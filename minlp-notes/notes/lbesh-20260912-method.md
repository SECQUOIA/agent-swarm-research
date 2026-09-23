# Logic-based extended supporting hyperplane algorithm (LB-ESH) for convex GDP

**Historical note; development update, 2026-09-19.** Current assumptions,
proofs, corrections, and implementation contracts are in the
[developed theory](lbesh-development-theory.md),
[implementation record](lbesh-development-implementation.md), and
[development log](lbesh-development-log.md). In particular, affine disjunct
cuts are established perspective OA cuts; finite convergence concerns global
and selected disjunct rows; an LP stopped on a resource/stall guard need not
be approximately hull-feasible. The current numerical implementation does
not provide exact-arithmetic certificates. Do not use the historical
"all fixed" or pending-benchmark statements below as current readiness claims.

Date: 2026-09-12. Status: method note with proofs of validity and finite
ε-convergence; prototype implemented in `code/minlp_solver_lab/lbesh/`;
benchmark results in the [closeout](research-20260912b-closeout.md), section 5.1. Novelty status: the scout
[`scout-20260912-convex-gdp-algorithms.md`](scout-20260912-convex-gdp-algorithms.md)
found no ESH variant for GDP in the literature; this is an unsuccessful
search, not a proof of novelty. The building blocks (ESH of Kronqvist,
Lundell, Westerlund 2016; Balas hull of polyhedral disjunctions; logic-based
OA of Türkay and Grossmann 1996) are established and credited.

## Problem class

Convex GDP with one level of disjunctions:

```
min   c^T x + sum_{i,k} gamma_ik lambda_ik
s.t.  h(x) <= 0,   A x <= b                              (global)
      for each i:  OR_k [ lambda_ik = 1,  g_ik(x) <= 0,  B_ik x <= d_ik ]
      sum_k lambda_ik = 1  (or >= 1),  Omega(lambda) linear
      x^L <= x <= x^U,  x_J integer,  lambda binary
```

with `h`, `g_ik` convex and differentiable on the box, every variable that
appears in a disjunction bounded (hull and big-M both need the box), and
every disjunction exclusive (`sum_k lambda_ik = 1`; OR disjunctions are
refused, because the Balas system with `x = sum_k nu_ik` would describe a
Minkowski sum rather than a union). A nonlinear convex objective is moved
into an epigraph row. Nonlinear equalities are excluded. Integer variables
may appear inside disjuncts: tangent cuts are valid for the continuous
relaxation of each disjunct set, which is all the arguments below use.

## Relaxations

**Hull relaxation** (Lee and Grossmann 2000): `x = sum_k nu_ik`,
`lambda_ik x^L <= nu_ik <= lambda_ik x^U`, `B_ik nu_ik <= d_ik lambda_ik`,
`cl(lambda_ik g_ik(nu_ik/lambda_ik)) <= 0`.

**Polyhedral logic relaxation used by LB-ESH.** Each nonlinear disjunct set
`S_ik = {x in box : g_ik(x) <= 0, B_ik x <= d_ik}` is replaced by a polyhedron
`P_ik = {x in box : B_ik x <= d_ik, a_l^T x <= b_l, l in L_ik}` whose extra
rows are supporting hyperplanes of `{g_ik <= 0}` (ESH cuts) or tangent
underestimator cuts (ECP/OA cuts). The master is the Balas hull of the
polyhedral disjunctions plus the global rows and their cuts. In the master,
a disjunct cut `a^T x <= b` becomes the affine row `a^T nu_ik <= b lambda_ik`.

**Lemma 1 (validity and exactness of the transform).**
(a) If `a^T x <= b` is valid for `S_ik`, then `a^T nu_ik <= b lambda_ik` is
valid for the hull relaxation of disjunction `i`, and hence for every
feasible point of the GDP written in disaggregated form (`nu_ik = x` when
`lambda_ik = 1`, `nu_ik = 0` otherwise).
(b) The projection of the Balas system for `{P_ik}_k` onto `x` equals
`conv(union_k P_ik)` (Balas 1979/1985, bounded polyhedra), which contains
`conv(union_k S_ik)`.

*Proof.* (a) For `lambda_ik > 0`, `cl(lambda g(nu/lambda)) <= 0` gives
`nu_ik/lambda_ik in S_ik` (the linear rows scale likewise), so
`a^T (nu_ik/lambda_ik) <= b`. For `lambda_ik = 0` the (finite) bounds force
`nu_ik = 0` and the row reads `0 <= 0`. (b) is Balas' theorem for bounded
polyhedra; containment follows from `P_ik ⊇ S_ik`. ∎

No ε-perspective approximation appears anywhere; this is the practical
difference from running a MINLP ESH/OA solver on the hull-reformulated
MINLP, whose nonlinear rows are perspective functions that are
nondifferentiable at `lambda = 0` and are usually approximated (Furman,
Sawaya, Grossmann 2020).

## Algorithm

1. **Interior points.** For each disjunct with nonlinear rows solve
   `min t s.t. g_ikj(x) <= t, B_ik x <= d_ik, A x <= b, x in box`
   (unbounded coordinates get an artificial box; the global rows are
   optional, they only centre the point); keep `xbar_ik` if `t < 0` (Slater
   point with margin `delta_ik = -t`). Likewise a global point `xbar` for the
   non-epigraph rows of `h`. If no strict interior point exists, that group
   of rows uses ECP cuts (tangent at the master point), which are valid by
   convexity. Epigraph rows always use tangent cuts (they are supporting
   hyperplanes of the epigraph).
2. **Initial cuts.** Tangent cuts at the starting point of every nonlinear
   row (keeps the master bounded).
3. **LP phase.** Solve the LP relaxation of the master. For every disjunct
   with `lambda_ik >= lambda_tol` form `p_ik = nu_ik/lambda_ik`; for every
   row `j` with `g_ikj(p_ik) > eps`, bisect on `[xbar_ik, p_ik]` to the
   boundary point `z_j` of `{g_ikj <= 0}` and add the supporting hyperplane
   of that row at `z_j` as a disjunct cut (one line search per violated row).
   Same for the global rows with `x_hat`. Repeat until no violation, a
   stall test, or an iteration cap.
4. **MILP phase (multi-tree).** Solve the master MILP (with a MIP gap well
   below the target tolerance); its proven bound (`ObjBound`) is a lower
   bound. Separate the integral point as in step 3 (active disjuncts have
   `p_ik = x_hat`). Solve the reduced NLP with the disjuncts fixed (only the
   selected disjuncts' constraints are present; `gdp.fix_disjuncts`) for an
   incumbent, and add the tangent cuts at its solution. Stop when
   `UB - LB <= tol`, when the master is infeasible or cut off, or when the
   master point is `eps`-feasible (then it is an `eps`-feasible solution with
   objective equal to the master value; if no reduced NLP ever succeeded the
   run is reported as stalled without an exact incumbent).
5. **Single-tree variant.** One branch-and-cut run of the master; lazy
   constraints at integer-feasible nodes implement step 4 (cuts and reduced
   NLP incumbents, passed back as heuristic solutions); optional user cuts
   at fractional nodes implement step 3 with `lambda_tol = 0.05`.

The big-M master is supported as a comparison baseline: a disjunct cut
`a^T x + c <= 0` becomes `a^T x + c <= M_a (1 - lambda_ik)` with `M_a` the
interval upper bound of the left-hand side on the box.

## Theorem (finite ε-convergence of the multi-tree algorithm)

Assume the box is bounded, all `g_ik` and `h` are convex and differentiable
with `L`-Lipschitz values on the box, and every nonlinear row either belongs
to a group with a Slater point `xbar` of margin `delta > 0` (all rows of the
group satisfy `g_j(xbar) <= -delta`) or uses ECP cuts. Fix `eps > 0` and
suppose every master MILP is solved to optimality. Then, unless the loop
stops earlier by `UB - LB <= tol` or by master infeasibility, the multi-tree
LB-ESH reaches after finitely many master solves a master point that violates
every nonlinear row by at most `eps`, and every master value is a valid lower
bound on the GDP optimum.

*Proof sketch.* Validity of the bound follows from Lemma 1 and from the
validity of every cut (supporting hyperplanes and tangents of convex
functions; for a disjunct row the cut is valid on the continuous relaxation
of `S_ik`, which suffices). For termination, consider an iteration where a
row `r` of an active disjunct (or of the global group) has
`g_r(x_hat) > eps` at the master point `x_hat`. Put
`phi(t) = g_r(xbar + t (x_hat - xbar))`, a convex differentiable function
with `phi(0) <= -delta`, `phi(s) = 0` at the bisection point
`z = xbar + s (x_hat - xbar)`, `s in (0,1)`, and `phi(1) > eps`. By
convexity `phi'(s) >= (phi(s) - phi(0))/s >= delta`. The cut
`grad g_r(z)^T (x - z) <= 0` is violated at `x_hat` by
`(1 - s) phi'(s) >= (1 - s) delta`. Lipschitz continuity gives
`eps < phi(1) - phi(s) <= L (1 - s) D`, `D` the box diameter, so the
violation is at least `eta = eps delta / (L D) > 0` while the cut normal has
norm at most `L`. Hence every later master point lies at Euclidean distance
at least `eta / L` from `x_hat` (in the coordinates of that disjunct, with
`lambda = 1`). A bounded set contains only finitely many points pairwise
`eta/L` apart, so finitely many iterations can have a violation above `eps`
in that row; there are finitely many rows and disjuncts. For ECP rows the
standard ECP argument applies (the tangent at `x_hat` cuts off `x_hat` by its
violation `> eps`, normal bounded by `L`). ∎

For the hull LP phase with fractional `lambda_ik >= lambda_tol`, the same
argument applies to `p_ik` and the transformed cut is violated at
`(nu, lambda)` by `lambda_ik eta >= lambda_tol eta`, so the hull LP phase
also terminates finitely for fixed `lambda_tol`. For the big-M master the
transformed cut may be satisfied at a fractional point (`M (1 - lambda)`
absorbs the violation), so the big-M LP phase is only guarded by the stall
test and the iteration cap.

**Remark (what the LP phase delivers).** The LP-phase value is always a
lower bound on the hull relaxation value, since `P_ik ⊇ S_ik`. At exit the
LP point satisfies `g_ikj(nu_ik/lambda_ik) <= eps` for `lambda_ik >=
lambda_tol` and `h(x) <= eps`, i.e. it is an approximately feasible point of
the perspective hull relaxation; no claim is made that the finite cut set is
dense, so the hull relaxation value is approached only in that
approximate-feasibility sense.

## What is and is not claimed

- Claimed: validity of the master bound, exactness of the affine transform
  of disjunct cuts, and finite ε-convergence under the stated hypotheses.
- Independent review ([review-20260912-lbesh.md](review-20260912-lbesh.md))
  found three blocking implementation defects (OR disjunctions in the hull
  master, fixed-variable rows losing their constant, big-M cuts with
  infinite `M` silently dropped) and several should-fix items (lower bound
  from `ObjVal`, sense of reported values, hypotheses missing from this
  note). All were fixed on 2026-09-12: OR disjunctions and unbounded cut
  variables are now refused, fixed-variable rows keep their constant, the
  multi-tree bound uses `ObjBound` with a MIP gap of `1e-6`, reported values
  carry the original sense, and the note was amended as above.
- Not claimed: superiority over existing solvers; that is the subject of the
  pending benchmark on GDPlib and GDP-derived MINLPLib instances against
  GDPopt (LOA, LBB), MindtPy (OA, LP/NLP-B&B) on big-M and hull MINLPs, and
  SHOT, DICOPT, SBB, BARON, SCIP, Gurobi 13 on the same MINLPs.

## Implementation notes

`code/minlp_solver_lab/lbesh/`: `structure.py` (extraction from a Pyomo GDP
model, logical constraints converted with `core.logical_to_linear`),
`nlfunc.py` (sympy-lambdified values and gradients with Pyomo fallback),
`master.py` (gurobipy master: hull or big-M), `solver.py` (driver; multi-tree
and single-tree). First check on a synthetic two-disjunction convex GDP with
exp and quadratic rows: hull/multi, hull/single, big-M/multi, big-M/single
all return 6.5948367 within 1e-7 of BARON's 6.5948368 on the big-M MINLP.
