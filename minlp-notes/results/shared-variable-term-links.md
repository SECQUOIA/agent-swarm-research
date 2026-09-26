# Linking the auxiliary variables of univariate terms that share a variable

Date: 2026-09-21. Status: exploratory computational note by the root agent,
closed on the user's instruction to finish open work without starting new
lines. The [literature check](../notes/shared-variable-terms-literature.md) was
done by a separate agent. An [independent review](../notes/review-shared-variable-term-links.md)
of the note and code found the added constraints valid (checked at native
incumbents of 18 instances), confirmed the `waterno2` bounds and the SCIP error
with its own model builder and evaluator, and found two errors in the first
version of this note: a sign error that turned a weak upper bound on the
maximization instance `pricing050` into an "invalid bound", and a wrong volume
number. Both are corrected below. Code and raw results:
`code/shared_variable_terms/`.

## Summary

Factorable solvers give every univariate term `f_a(x)` its own auxiliary
variable `t_a` and its own envelope over the bounds of `x`. When several
different univariate functions of the *same* variable occur in a model, the
auxiliary variables satisfy exact one-dimensional relations that the
term-by-term relaxation ignores, for example

```
s = sin(x), c = cos(x):            s^2 + c^2 = 1
t_p = x^p, t_q = x^q:             t_q = t_p^(q/p)
(p,q != 0; x >= 0 for positive powers, x > 0 if a power is negative)
```

Adding such a relation as a redundant constraint lets any solver convexify the
planar curve `(f_a(x), f_b(x))`. It is the shared-variable counterpart of the
[row hull](row-hull-separable-concave.md), which treats terms linked by a
conservation row.

- The hull theory is known: Ballerstein's thesis (ETH 2013, Chapter 5, with
  Michaels and Weismantel) gives the simultaneous hull of vectors of univariate
  convex functions and SCIP separators for it, without automatic detection and
  with one library instance. Convexifying the relation-only link on the
  actual planar curve gives the projection of that hull onto `(t_a, t_b)`;
  intersecting this projection with the individual envelopes can be weaker
  than the full simultaneous hull. The nonconvex equality itself is not that
  projection. For sine/cosine, the circle identity alone can include points
  outside the angle interval's arc, whose chord is not implemented here.
  For `(x^2, x^3)` on `[1,2]` the
  relaxation volume is `3/20 = 0.1500` term by term, 0.0730 when the
  individual term envelopes are intersected with the planar hull of
  `t_3 = t_2^(3/2)` on `t_2 in [1,4]` (the region between that curve and its
  chord; numerical integration, reviewer's value in
  `review/volume.py`; the first version said 0.1497 and 0.0729) and 0.0055
  for the hull (Ballerstein's value).
- What this note adds is automatic detection across constraints, a
  solver-independent reformulation, and a library-wide look. A scan finds a
  variable with at least two distinct univariate subexpressions in 189 of 1,594
  parsed MINLPLib instances; many of those pairs are the same function written
  twice or affinely related, and the two rules implemented here (sine/cosine of
  a bare variable; powers of a nonnegative variable) apply to 48 instances.
- Results are mixed on small instances and large on one family. Gurobi 13
  (60 s, 48 instances) reports 26 solved without and 25 with links; these
  counts include unverified and tolerance-infeasible incumbents. The mean time
  is unchanged. On the open water-network instances `waterno2_06/09/12/18`,
  whose model defines `x^2` and `x^3` of each flow in separate equations, the
  links raise Gurobi's dual bound after 1800 s from 137 to 192, 220 to 285, 379
  to 1160 and 771 to 2168. All four exceed the best dual bounds listed on the
  MINLPLib pages on 2026-09-21 (165.19, 273.90, 479.51, 770.74). These are
  single floating-point solver runs, not certified bounds. BARON (1800 s) gives
  much weaker bounds in both forms and corroborates only the direction: with
  links its bounds rise from 109 to 138, 126 to 250 and 124 to 494 on
  `waterno2_09/12/18` and fall slightly on `waterno2_06`.
- The exact convex hull of `(x, x^2, x^3)` (two rotated cones, classical),
  added in Gurobi for every variable with the `{2, 3}` power pair, dominates the
  relation link: after 1800 s the dual bounds on `waterno2_06/09/12/18` are 231,
  656, 1570 and 3339 (link: 192, 285, 1160, 2168), and on `ghg_2veh` and
  `ex8_4_2` they are 7.58 and 0.483 against listed best dual bounds of 7.43 and
  0.449. Same qualification: single uncertified runs.
- A point for `waterno2_18` with objective 5178.159, below the listed 5269.64,
  was obtained by polishing the linked-model incumbent (binaries fixed, native
  model, Gurobi tolerances `1e-9`); every native constraint, bound and
  integrality condition holds to `5.8e-11`; the residuals were evaluated
  exactly in rational arithmetic (`exact_check_point.py`): the largest
  violation is `32325/2^49` and the objective is `728761127366816713/2^47`
  (`polish_point.py`, point saved in `point_waterno2_18.json`). This certifies
  tolerance feasibility, not exact feasibility.
- SCIP 10 returns a wrong optimum on `waterno2_02` and `waterno2_03` (42.343
  against 39.571; 130.84 against 115.005); its own solution checker accepts the
  better points. SCIP's numbers on this family are therefore not used for any
  claim. Gurobi's "optimal" 28.931 on `ex8_4_7` (MINLPLib: primal 29.047,
  best listed dual bound 29.0437 from LINDO) is not a valid solve: it lies
  below that dual bound. A rerun of the same command on 2026-09-25
  reproduced it (28.931149, same node count) and saved the point
  (`results_gurobi_60_ex8_4_7_rerun.jsonl`, `review/rerun_point_check.py`).
  Under the plain-float evaluator of the original model the point violates
  row 25 by `8.9e-4`; Gurobi's own `MaxVio` reports the same value, far
  above its default feasibility tolerance `1e-6`. The reviewer's separate
  reproduction returned 28.922 with a `8.7e-4` violation
  (`review/note_model_point_check.jsonl`).
  SCIP's "optimal" 1.20585 on `ex7_3_5` (native and linked) is below the
  MINLPLib dual bound 1.206653; not investigated.

## The reformulation

For every variable `x` of the model (`link_detect.py`):

1. *Trigonometric pair.* If both `sin(x)` and `cos(x)` occur (of the bare
   variable), add `s = sin(x)`, `c = cos(x)`, `s^2 + c^2 = 1`.
2. *Powers.* If `x >= 0` has finite bounds and at least two exponents
   `p_1, ..., p_m` different from 0 and 1 occur (`x^p`, squares, square roots,
   reciprocals, repeated products; a negative exponent needs `x > 0`), add
   `t_k = x^(p_k)` and `t_k = t_ref^(p_k / p_ref)`, where `p_ref` has the
   smallest magnitude.

Both are valid equalities on the feasible set, so the feasible set in the
original variables does not change. The solvers identify `t_k = x^(p_k)` with
their own auxiliary variable for that subexpression (SCIP), or carry a second
copy of it (Gurobi); either way the new constraint ties the terms together.
If every shared function is convex and used only through its epigraph, the
joint epigraph is already convex, so separate exact epigraph descriptions
lose nothing. This does not extend to arbitrary functions: simultaneous
convexification can strengthen even one-sided epigraph uses when curvature
is mixed. For example, on `[0,1]`, `(x,t_1,t_2)=(1/2,1/4,1/2)` satisfies the
individual epigraph hulls of `x^2` and `sqrt(x)`, but not their joint hull.
Equality in `E[X^2] >= E[X]^2 = 1/4` forces `X=1/2`, hence the joint hull
requires `t_2 >= sqrt(1/2)` there. Equality-defined terms remain an important
case, as in the instances below; they are not a necessary condition for gain.

Not implemented: exponential and logarithm pairs, inner arguments other than a
bare variable, and the chord of the arc for the trigonometric pair. The full
hull of the space curve is added only for the `{2, 3}` power pair, as two
explicit cone constraints (section on the exact hull below).

## Computational record

Machine and solvers as in the [row-hull experiment record](../notes/row-hull-experiments.md).
Relative gap `1e-4`. `native` is the OSiL model as read; `linked` adds the
constraints above. One run per cell.

### Gurobi 13, 60 s, 4 threads (`results_gurobi_60.jsonl`)

All 48 instances with links (the two containing `abs`, `water` and
`inscribedsquare03`, were added after `abs` support was put into the builder).
Solver-reported solved: 26 native, 25 linked (`ex8_4_7` and `lnts50` only native, `wastepaper4`
only linked); shifted geometric mean time 8.2 s against 8.4 s; of the 24 solved
by both, the linked form is faster on 10. On `water` (14 links) the 60 s dual
bound moves from 255.0 to 267.2. No dual bound of either form is on the wrong
side of the best known primal value for the instance's optimization sense
(for the maximization instance `pricing050` the dual bounds lie above it).
Dual bounds after 60 s on unsolved instances (all minimization
except `pricing050`, a maximization, where the linked bound is the weaker one):

| instance | links | native | linked |
|---|---|---|---|
| `waterno2_06` | 78 | 96.3 | 150.2 |
| `waterno2_09` | 117 | 175.2 | 464.4 |
| `waterno2_12` | 156 | 351.5 | 1110.5 |
| `waterno2_18` | 234 | 605.7 | 2236.3 |
| `pricing050` | 34 | -1331 | -1290 |
| `ghg_3veh` | 9 | 0.0 | 3.63 |
| `ghg_2veh` | 6 | 6.87 | 3.93 |
| `ex8_4_2` | 9 | 0.191 | 0.117 |
| `waterx` | 14 | 708.9 | 666.6 |
| `lnts100` / `200` / `400` | 101 / 201 / 401 | 0.5517 / 0.5518 / 0.5205 | 0.5417 / 0.5492 / 0.4953 |

`waterno2_03` is solved in 3.5 s instead of 12.1 s and `waterno2_04` in 34.6 s
instead of 47.7 s. The links hurt on the particle-steering family `lnts*`
(Gurobi solves `lnts50` natively in 24 s and not within 60 s, or 300 s, with
links), on `ex8_4_7` (compared with a native solve that is itself invalid;
see the Summary), and at 60 s on `ghg_2veh`.

### The exact hull of `(x, x^2, x^3)` in Gurobi (`gurobi_link.py` mode `moment`, `results_gurobi_60_moment.jsonl`, `compare_moment.py`)

The convex hull of the planar relation `t_3 = t_2^1.5` for
`t_2 in [l^2,u^2]`, with `0 <= l <= u`, is the projection of the classical
convex hull of `(x, x^2, x^3)` on `[l,u]`. The planar equality itself is
nonconvex. The full three-dimensional hull is described by
`(x - l)(t_3 - l t_2) >= (t_2 - l x)^2` and
`(u - x)(u t_2 - t_3) >= (u x - t_2)^2`, together with
`x-l >= 0`, `t_3-l t_2 >= 0`, `u-x >= 0`, and `u t_2-t_3 >= 0`.
These are two rotated second-order cones. The nonnegative factors are
required, including at interval endpoints; both implementations impose them.
Added as quadratic constraints for every variable with the `{2, 3}` power pair
(19 of the 48 link instances), Gurobi 13, 60 s, 4 threads:

| instance | native | link | exact hull | hull + link |
|---|---|---|---|---|
| `waterno2_04` (solved) | 47.7 s | 34.6 s | 14.0 s | 13.8 s |
| `waterno2_06` dual | 96.3 | 150.2 | 212.0 | 208.9 |
| `waterno2_09` dual | 175.2 | 464.4 | 642.5 | 653.9 |
| `waterno2_12` dual | 351.5 | 1110.5 | 1541 | 1500 |
| `waterno2_18` dual | 605.7 | 2236 | 3252 | 3354 |
| `ex8_4_2` dual | 0.191 | 0.117 | 0.470 | 0.455 |
| `ghg_2veh` dual | 6.87 | 3.93 | 7.00 | 6.96 |
| `ghg_3veh` dual | 0.00 | 3.63 | 2.68 | 0.00 |

Solved counts are 9 of 19 in every mode and the mean times are within noise
(12.9, 12.1, 11.8, 11.7 s). The exact hull dominates the relation link on every
water instance and on `ex8_4_2`, and removes the harm the link did on
`ghg_2veh`; the link on top of the hull adds nothing consistent. All 60 s
dual bounds are on the valid side of the best known primal values for the
optimization sense (above the primal value for the maximization instance
`pricing050`). In SCIP 10 the same constraints (`moment_pilot.py`, 60 s)
gave only small gains: dual bounds 124.3 against 117.4 (linked) on `waterno2_04`, 139.9 against 140.6 on `waterno2_06`,
0.304 against 0.236 on `ex8_4_2`, and a much weaker bound on the maximization
instance `pricing050` (-145 against -1425; an earlier version of this note
misread this as an invalid bound). The difference is presumably Gurobi's
handling of the convex quadratic constraints. The 1800 s runs of the exact
hull are in the 1800 s table below.

### When do the links help? Evidence and a rule (`compare_rules.py`, `results_gurobi_60_linked2.jsonl`)

The 60 s data separate three cases.

1. *Power links where both powers enter equality rows* (`waterno2*`: `x^2` and
   `x^3` of every flow are defined in separate equations and used elsewhere):
   large reported bound gains for Gurobi and gains on three of the four
   longer BARON runs. SCIP results on this family are excluded because of
   the inconsistency documented below. Here the individual envelopes sharing
   `x` can still be weaker than simultaneous convexification; the extra link
   lets the solver additionally relax the planar curve `(x^2, x^3)`.
2. *Trigonometric links* (`lnts*`, `inscribedsquare*`): help SCIP, hurt Gurobi.
   Gurobi handles `sin` and `cos` by its own piecewise treatment, and the added
   nonconvex quadratic equality `s^2 + c^2 = 1` is one more object to branch on;
   the observed effect is solver specific; these runs do not validate a
   selection rule based on model structure alone.
3. *Badly conditioned links.* `ex8_4_7` has exponents `{-1, 2}` on variables in
   `[660, 680]`; the first rule takes the reference exponent of smallest
   magnitude, `-1`, and writes `t_2 = t_{-1}^{-2}` with `t_{-1}` about `1/670`.
   With that link Gurobi times out. With the reference chosen as the positive
   exponent closest to 1 (`link_detect.reference(..., "positive")`, mode
   `linked2`) Gurobi reports an optimum of 26.994 after 36 s (native: 28.931
   after 7.5 s). This result is inconsistent with the reference bounds: it is
   7.1% below the best dual bound listed on MINLPLib for this minimization
   instance (29.0437, LINDO; primal 29.0473). It is not counted as a valid
   solve; the native 28.931 is also not valid (see the Summary). A rerun of
   the same command on 2026-09-25 (same script and settings, 60 s, 4 threads,
   run alone rather than eight at a time) reproduced the result exactly
   (26.99421396, 123,620 nodes, 36 s) and saved the point
   (`results_gurobi_60_ex8_4_7_rerun.jsonl`, `review/rerun_point_check.py`).
   In the original model that point has the same objective 26.994 and
   satisfies all variable bounds, but it violates row 39,
   `x61 = x50 exp(-x51 (800/x49 - 1))`, by `5.9e-5`. Because `x61` is about
   0.008, this is a relative error of about 0.7%. Five of the nine other rows
   of this form (rows 30–38) are violated by `9e-6` to `3.8e-5`.
   Gurobi's `MaxVio` for the linked model reports the same `5.9e-5`, well above
   its default feasibility tolerance `1e-6`. The violated row is an original
   row, not a link, and the objective of the linked model matches the original
   evaluator. The invalid solve therefore appears to come from Gurobi
   accepting points that are infeasible by a small absolute amount on rows whose
   variables are of order `1e-3`, not from a bug in the reformulation. This
   diagnosis was not confirmed by a solve at tighter tolerances. Over the 46
   instances run with both rules the results are otherwise within noise (24
   solved under each rule as reported by Gurobi, 23 under the second rule
   without `ex8_4_7`; mean time 8.4 s against 8.6 s; `wastepaper4` solves
   under the first rule only). The data therefore show no benefit of either
   reference choice. Whether the reference exponent affects conditioning on
   `ex8_4_7` would need a validated solve against the original model. The
   curve-hull study also excludes `ex8_4_7` as numerically unreliable
   (`research-20260922/curve-hulls/report.md`).

A heuristic suggested by this evidence is to prioritize power links with
powers appearing in equality rows or with both signs; treat trigonometric
links as solver specific. (An earlier version also preferred a positive
reference exponent close to one; its only support was the invalid
`ex8_4_7` result above.) These are priorities, not necessary conditions for
a useful link. In particular, the mixed-curvature epigraph example above
rules out the earlier claim that one-sided epigraph uses can never gain. The heuristic comes from 48 instances
and one run per cell; it is not a validated policy.

### Gurobi 13, 1800 s, 3 threads (`results_gurobi_1800.jsonl`, `results_gurobi_1800_moment.jsonl`)

Native and linked: ten runs at once. Exact hull (`run_moment_1800.sh`): six
runs at once, on the same machine. No run reached optimality.

| instance | native dual | linked dual | exact hull dual | native primal | linked primal | exact hull primal | MINLPLib page 2026-09-21: best dual (solver) / primal |
|---|---|---|---|---|---|---|---|
| `waterno2_06` | 136.79 | 191.53 | 231.38 | 282.917 | 282.917 | 284.366 | 165.19 (SCIP), 162.19 (Gurobi) / 282.888 |
| `waterno2_09` | 220.22 | 285.00 | 656.49 | 943.87 | 936.40 | 904.75 | 273.90 (SCIP), 226.83 (Gurobi) / 922.595 |
| `waterno2_12` | 378.70 | 1159.96 | 1570.28 | 2310.39 | 2291.60 | 2234.78 | 479.51 (Gurobi) / 2263.36 |
| `waterno2_18` | 770.92 | 2168.25 | 3339.19 | 5302.79 | 5138.30 | 5083.08 | 770.74 (SCIP) / 5269.64 |
| `ghg_2veh` | 4.670 | 7.157 | 7.5817 | 7.7816 | 7.7709 | 7.7718 | 7.4335 (SCIP) / 7.7709 |
| `ex8_4_2` | not run | not run | 0.48321 | not run | not run | 0.48516 | 0.44935 (BARON) / 0.48515249 |

On the four water instances the linked dual bound exceeds the listed best dual
bound; on `ghg_2veh` it does not. The exact hull exceeds the linked bound on
all five common instances, by 21% on `waterno2_06` and by 35-130% on the other
three water instances, and its bounds on `ghg_2veh` and `ex8_4_2` exceed the
listed best dual bounds (7.58 against 7.43; 0.483 against 0.449, where the
listed primal is 0.48515). The exact-hull runs also report incumbents below the
listed primal values on `waterno2_09`, `waterno2_12` and `waterno2_18` (904.75,
2234.78 and 5083.08, the last also below the polished point 5178.16 in the next
section); `gurobi_link.py` prints only the summary line, so these points were
not saved and their native-model feasibility was not checked, unlike the
polished `waterno2_18` point. The linked run on `waterno2_18` also returns a
primal value below the listed one; that point was not saved. The reviewer's
own 870 s run of the linked model gives dual 2442.7 and a point with objective
5151.90 whose largest constraint violation in the native model, evaluated in
plain floating point, is `9.9e-7` (bounds `1e-16`, integrality exact); it is
feasible at `1e-6` but not at MINLPLib's `1e-8`.
Qualifications: the MINLPLib pages name only the solver behind a bound, not the
version, options or time, so these are not like-for-like comparisons; Gurobi's
bounds are floating-point results and were not certified; the listed SCIP bounds
for this family are doubtful for the reason in the next section.

### BARON through GAMS 54, 1800 s, 1 thread (`baron_link.py`, `results_baron_1800.jsonl`)

Power links only (BARON has no trigonometric functions). `ghg_2veh` was not
run: the GAMS text produced by `baron_link.py` does not compile for it (error
445 on its power expressions), a limitation of the writer, not a result.

| instance | native dual | linked dual | native primal | linked primal |
|---|---|---|---|---|
| `waterno2_06` | 73.7 | 72.8 | 304.13 | 297.02 |
| `waterno2_09` | 108.7 | 137.8 | 980.02 | 985.65 |
| `waterno2_12` | 125.9 | 250.2 | 2401.53 | 2382.52 |
| `waterno2_18` | 124.0 | 493.9 | 5603.16 | 5617.80 |

BARON's bounds are far below Gurobi's in both forms and below the MINLPLib
values, so they cannot confirm the Gurobi numbers; they show the same direction
on three of the four instances. On `waterno2_02` BARON finds the correct
optimum 39.571 in both forms in about 2 s.

### The improved `waterno2_18` point (`polish_point.py`, `point_waterno2_18.json`)

The linked model (Gurobi, 900 s, 4 threads) gives a point with native-model
objective 5180.37 and largest violation `9.8e-7`. Fixing its binaries and
re-solving the continuous nonconvex native model from that start with
`FeasibilityTol = OptimalityTol = 1e-9` (600 s, not to optimality) gives
objective 5178.159 with largest violation below `5.8e-11` over all constraints,
bounds and integrality conditions. `exact_check_point.py` re-evaluates every
row of the native model at the saved point in exact rational arithmetic (the
model has only products, squares and cubes): the largest violation is exactly
`32325/2^49 = 5.742e-11` (row 309, lower side) and the objective is exactly
`728761127366816713/2^47 = 5178.159251...`. The point therefore meets the stated
`1e-8` feasibility tolerance with an exact residual bound, and its objective
is below the listed primal bound 5269.64. The residual is positive, so this
is not an exact feasible point or a certified upper bound on the exact
problem. Optimality is not certified, and the dual bounds remain solver
output. The checker rationalizes the parsed binary floating-point model
coefficients and saved point. The additional
[`review/exact_scope_audit.py`](../code/shared_variable_terms/review/exact_scope_audit.py)
check uses the OSiL decimal coefficients as exact rationals and obtains the
same objective and maximum residual for this point. It reuses the OSiL
reader, so this independently checks coefficient conversion, not XML parsing.

### SCIP 10 (`results_links.jsonl`, `results_lnts_1800.jsonl`)

In the 60 s pilot (single thread) SCIP reports 24 native and 25 linked of 48 as
solved (gap limit counted; one of the linked solves is the wrong `waterno2_04`
optimum), with unchanged mean time. With links its dual bound on `lnts50` after 1800 s is
0.5543 instead of 0.5117 (optimum 0.55467), and 0.5456 instead of 0.5397 on
`lnts100`; for the trigonometric family the link therefore helps SCIP and hurts
Gurobi. Adding `p = tf cos u`, `q = tf sin u`, `p^2 + q^2 = tf^2` on top
(`lnts_soc.py`) did not help (0.5423 after 300 s against 0.5522).

**Solver error.** On `waterno2_02`, `waterno2_03` and `waterno2_04` SCIP 10
(its own OSiL reader or our builder, default settings) stops with "optimal"
values 42.343 and 130.8 on the first two, native and linked alike, and 161.1 on
the third with links (the native run timed out), while Gurobi and MINLPLib give
39.571, 115.005 and 145.440. `check_scip_waterno2.py` solves `waterno2_02` with Gurobi
at tolerances `1e-9` and passes the point to SCIP's `checkSol` on the original
problem: SCIP accepts it as feasible with objective 39.5714; the reviewer
confirmed this on `waterno2_02` and `waterno2_03` (also with `completely=True`).
The behaviour depends on settings (`numerics/feastol 1e-7` gives 46.149 on
`_02` and the correct 115.0045 on `_03`; presolve off gives 42.3435 and 117.579).
SCIP therefore cuts off the optimum on this family, and its dual bounds there,
including the ones in our pilot, prove nothing.

## Literature

See the [literature note](../notes/shared-variable-terms-literature.md) for
statements and access limits. Closest: Ballerstein (2013, Chapter 5);
Sherali and Tuncbilek (1997), whose convex variable-bounding constraints
`(X_q)^p <= X_pq` are the convex half of the power link for integer exponents;
the trigonometric identity as a modelling device in AC power flow (Jabr's
second-order cone constraint) and kinematics, where the angle is usually
eliminated; redundant relaxation-only constraints supplied by the modeller in
BARON (Sahinidis and Tawarmalani 2005). We found no solver documentation of an
automatic linking step and no library-wide study; an unsuccessful search does
not establish novelty.

## Limitations

- Two detection rules only; 48 of 1,594 instances; the effect is decisive on one
  model family and neutral or negative elsewhere. The proposed selection
  heuristic has not been validated.
- Single runs on a loaded machine. Gurobi and SCIP were run on the full link
  set; BARON was tested only on selected power-link instances and does not
  support the trigonometric models in this pilot.
- The relation link is weaker than the known hull of the space curve. The
  exact hull was added only for the `{2, 3}` power pair, where it has a
  two-cone closed form and dominates the link in Gurobi; hull cuts for the
  other pairs (trigonometric, other exponent sets) were not tested.
- The incumbents reported by the 1800 s exact-hull runs were not saved and
  their feasibility in the native model was not checked.
- The improved dual bounds are uncertified solver output and are not
  reproduced in value by BARON; the improved primal point on `waterno2_18` has
  an exact residual bound and meets the stated tolerance, but is not exactly
  feasible. Solver-reported solved counts are not independently certified.
- The `lnts_soc.py` numbers were read from the terminal and have no raw record.

## Reproduction

```
cd code/shared_variable_terms
RUN="uv run --project ../minlp_solver_lab python"
$RUN scan.py scan.jsonl                        # structural scan
./run_links.sh                                 # SCIP, 60 s, native and linked, on scan_candidates.txt
./run_gurobi_links.sh                          # Gurobi, 60 s on link_instances.txt, then 1800 s on five instances
$RUN check_scip_waterno2.py waterno2_02        # SCIP accepts the point it excludes
./run_baron_links.sh                           # BARON, 1800 s, native and linked
./run_moment.sh && python3 compare_moment.py    # exact moment-curve hull in Gurobi
./run_moment_1800.sh                           # 1800 s runs of the exact hull
$RUN polish_point.py waterno2_18 900 600       # the improved primal point
$RUN exact_check_point.py waterno2_18 point_waterno2_18.json   # exact residuals at that point
./run_linked2.sh && python3 compare_rules.py    # reference-exponent rule comparison
for m in linked2 native; do $RUN review/rerun_point_check.py ex8_4_7 $m 60 4; done > results_gurobi_60_ex8_4_7_rerun.jsonl   # ex8_4_7 points, checked in the original model
$RUN moment_pilot.py waterno2_04 moment 60     # the moment-cone variant
```
