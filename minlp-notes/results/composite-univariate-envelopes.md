# Envelopes of composite univariate subexpressions with certified curvature

Date: 2026-09-21. Status: method, implementation and experiments by the root
agent; literature check by a separate research agent completed. The
[independent review](../notes/review-composite-univariate-envelopes.md) found
no error in the propositions and no soundness violation in 5,760 randomized
cut checks or in the recorded runs; it found one latent cut-flag bug, missing
domain checks and overclaiming words, all addressed as listed in the
experiment record.
Experimental details and all negative results are in
[the experiment record](../notes/composite-univariate-envelopes-experiments.md).

## Summary

LP-based global solvers relax a nonlinear expression operator by operator.
When a subexpression depends on one variable but contains several nonlinear
operators or several terms in that variable — a univariate polynomial,
`x exp(-x)`, a logistic function written with `exp`, an Antoine or
heat-capacity correlation — the separate relaxations ignore that all parts
move together. This is the dependency problem of interval arithmetic in
relaxation form.

- **Observation.** On `min sum_i p_i(x_i)` with one or three linear rows and
  random quartics `p_i` in 10 to 80 variables, native SCIP 10 solves 2 of 24
  instances in 120 s, Gurobi 13 solves 3 and BARON 6. Of 1,632 MINLPLib
  files, 1,594 were parsed (38 use operators the reader does not support or
  are too large); 744 of them have general nonlinear rows, 140 of those
  contain composite univariate subexpressions, and for 115 at least one has a
  finite, certifiable domain.
- **Method.** Detect maximal univariate subexpressions `g(x)`; certify the
  convex and concave pieces of `g` by ball arithmetic on `g''`; separate the
  convex and concave envelopes of `g` on the node interval by a
  conjugate-slope search whose cuts are valid for every slope; propagate with
  the range of `g`. "Certified" refers to the curvature labels. Function
  values are floating point with a fixed safety shift, and the envelope is
  exact up to the width of the undecided slivers and the search tolerance.
  The implementation is a SCIP constraint handler that works alongside
  SCIP's own treatment of the same constraint.
- **Guarantee.** With exact envelopes the root gap of a separable program
  with `m` linking rows is at most the sum of the `m` largest envelope
  defects (Aubin–Ekeland; Udell–Boyd), independent of `n`. Term-wise
  relaxation can lose `Theta(n)`.
- **Results.** With the handler SCIP solves all 48 separable test instances
  in seconds. On 107 MINLPLib instances the root relaxation improves on 35
  and worsens on 4, but the Python prototype solves 51 within 120 s against
  54 for native SCIP. See [Computational evidence](#computational-evidence).

The envelope construction and the weakness of term-wise relaxation are
known. What appears to be new is the automatic, certified, general-function
treatment inside an LP-based branch-and-bound solver. See
[Literature](#literature).

## Certified curvature pieces

Let `g` be an elementary expression on `[L, U]`. Bisect `[L, U]`; on each
interval `I` evaluate `g` and `g''` in ball arithmetic (python-flint `arb`).
A finite enclosure of `g` shows that `g` is defined on `I`; poles and
arguments outside the domain of `log` or a fractional power give no finite
enclosure. If the enclosure of `g''` is nonnegative, `I` is *convex*; if
nonpositive, *concave*. When the natural enclosure is undecided, the
mean-value form `g''(m) + g^(3)(I)(I - m)` is tried, which is much sharper on
small intervals. In an unarchived development test on a MINLPLib kriging
function (the expression, domain and output are not recorded in the
repository), it reduced the number of undecided slivers from 1,973 to 231
and the model build from 46 s to 1 s.
Otherwise `I` is split. Intervals of width below
`1e-7 max(1, U-L)` that remain undecided are *unknown* and carry a rigorous
enclosure `[glo, ghi]` of `g` on `I`. Adjacent intervals with the same label
are merged. An interval is unknown whenever neither enclosure decides the
sign of `g''` before the width threshold. This happens around inflection
points and at singular endpoints such as `x^0.6` at `0`, but also wherever
the ball enclosure of `g''` is too wide, for example for an expanded shifted
quartic in the [independent review](../notes/review-composite-univariate-envelopes.md).

At a singular endpoint the ball evaluation of `g` fails. The enclosure is
then the union of enclosures on dyadic subintervals approaching the endpoint
and of the exact endpoint value. The uncovered sliver has relative length
`2^-60`, or up to `2^-20` of an undecided sliver when rounding of a ball
touches a singular endpoint other than `0`; continuity of `g` there is
assumed, not verified. Certification
gives up, and the subexpression stays native, for unsupported functions,
expressions with more than 400 operations, or more than 20,000 intervals.
Sympy may simplify an expression before certification (`sqrt(x)^2` becomes
`x`), which can enlarge its domain; the native constraint still enforces the
original one.

## Cuts that are valid for every slope

Fix a node interval `[l, u]` and a slope `s`. Put
`phi_s(x) = g(x) - s x` and compute a lower bound `h(s)` on
`min_{[l,u]} phi_s` piece by piece:

- concave piece: the smaller endpoint value, which is exact;
- convex piece `[a, b]`: if `phi_s'` changes sign, find `x0` with
  `phi_s'(x0) ~ 0` by Brent's method and use
  `phi_s(x0) - |phi_s'(x0)| (b - a)`, which is valid by convexity for any
  `x0` in the piece; otherwise the smaller endpoint value;
- unknown piece `[a, b]`: `glo - max(s a, s b)`.

**Proposition 1.** For every `s`, `g(x) >= s x + h(s)` on `[l, u]`.

Validity therefore does not depend on how `s` is chosen. A relative safety
shift of `1e-11` guards the floating-point evaluation of `g`; the
implementation is not a verified numerical code.

**Proposition 2.** If the inner minima are exact, `sup_s (s x* + h(s))` is
the convex envelope of `g` on `[l, u]` at `x*`, and the supremum is attained
at any `s` for which `x*` lies in the convex hull of `argmin phi_s`.

This is the biconjugate formula. The minimizer of `phi_s` moves right as `s`
grows, so bisection on `s` finds the supporting slope; unknown pieces are
ignored while steering the search and included in the final `h(s)`. The
concave envelope is the same construction for `-g`. The range of `g` is
enclosed by `[h(0), -h_{-g}(0)]`.

The cost is a few dozen piece scans per cut, about 1–2 ms in Python. No
closed forms, tie-point equations or bounds on the number of inflection
points are needed.

## Why it matters: a gap that does not grow with `n`

Consider `min sum_i g_i(x_i)` subject to `A x (<=,=) b`, `l <= x <= u`, with
`m` rows, and let `rho_i = max (g_i - env g_i)`.

**Proposition 3 (Udell–Boyd 2016, Theorem 1, in the form reported by the
literature check; it refines Aubin–Ekeland 1976).** For lower semicontinuous
`g_i` on compact intervals and a feasible problem, the relaxation that
replaces each `g_i` by its convex envelope has gap at most the sum of the
`min(m, n)` largest `rho_i`. The source was not re-read for this note.

**Example 4.** Let `g(x) = x^4 - x^2` on `[-1, 1]` for every `i` and let the
single row be `sum x_i = 0`. Term-wise relaxation keeps `x^4` and replaces
`-x^2` by its secant `-1`. Its optimal value is `-n`, attained at `x = 0`.
The true optimal value is `-n/4` for even `n`, attained at
`x_i = +-1/sqrt(2)` in balanced pairs. The term-wise gap is `3n/4`. The
envelope of `g` is `-1/4` between the two minimizers, so the envelope
relaxation is exact here, and Proposition 3 bounds its gap by `1/4` for every
right-hand side.

This explains the experiment: spatial branching must repair a term-wise gap
in every coordinate, while with exact envelopes at most `m` coordinates have
any gap at the relaxation's vertex solutions.

## Detection

In the expression tree of each constraint, a maximal subtree that depends on
exactly one variable and contains at least two nonlinear operators is a
candidate. Inside a sum, all univariate summands in the same variable are
grouped into one candidate, so a polynomial written as separate monomials is
recovered. Products with a constant, sums and negation are not counted as
nonlinear operators. Subtrees containing `abs` are left to the solver.

A candidate is used only if its variable has finite bounds after a SCIP
presolve pass with dual reductions disabled, and if curvature certification
succeeds on that interval. Those implied bounds are then imposed on the
variable. Otherwise the subexpression stays native. Quadratic terms that
OSiL stores outside the expression tree are not merged into a candidate.

## Integration with SCIP

For each accepted candidate the model gets an auxiliary variable `w`, the
native constraint `w == g(x)`, and one constraint of the handler on
`(w, x, g)`. SCIP remains responsible for feasibility, branching and its NLP
heuristics. The handler adds:

- initial envelope cuts at both ends and the middle of the global interval;
- envelope cuts at LP solutions, at most 12 per constraint and node, marked
  local whenever the node interval differs from the global one at all;
- forward propagation of the range of `g` to `w`, and, when the interval of
  `w` is smaller than that range, backward trimming of `x` by bisection on
  the test "the range of `g` on `[l, t]` misses the interval of `w`";
- a completion heuristic that keeps the LP values and sets every `w` to
  `g(x)`.

A standalone mode, where the handler alone enforces `w == g(x)` by cuts and
branching on `x`, is kept for the separable test families. On purely concave
single-operator terms it is worse than SCIP, because SCIP's NLP heuristics
cannot see the constraint. When an interval of `x` is below `1e-9` relative
width and the constraint is still violated, which happens at non-Lipschitz
points such as `x^0.6` at `0`, this mode fixes `x` at its LP value and gives
up the rest of that interval.

## Computational evidence

Details, tables and the review resolutions are in
[the experiment record](../notes/composite-univariate-envelopes-experiments.md).
Code: [`code/univariate_envelopes`](../code/univariate_envelopes/README.md).
SCIP 10.0, one thread, 120 s, gap `1e-4`; times include certification and
the Python handler.

**Separable families (the mechanism in isolation).** 48 instances: random
quartics or logistic utilities in 10 to 80 variables with 1 or 3 dense
linear rows, three seeds. SCIP with the handler solves all 48 in at most
15.3 s and 91 nodes. Native SCIP solves 8, Gurobi 13 solves 27 (all the
logistic ones, 3 quartic ones), BARON 12. These runs shared the machine with
other jobs; the contrast between seconds and time limits is robust, the
individual times are not.

**MINLPLib (end to end).** 107 instances where the handler applies:

- *Consistency:* none of the 317 runs with a reference comparison
  contradicts the MINLPLib reference bounds (the `t1000` `split` error and
  the six runs of `ex8_6_1` and `uselinear`, which lack parseable reference
  bounds, are not compared). This is a check against reference data, not a
  proof of soundness.
- *Root relaxation:* on the 81 instances with a root LP bound in both modes,
  the handler reduces the root gap to the reference optimum by more than 10%
  on 35, often by orders of magnitude (`cesam2log` 861 to 0.51,
  `procurement1large` 3.95 to 0.011, `kriging_peaks-full500` 334 to 6.4,
  relative to the optimum), and increases it on 4, slightly.
- *Solved within 120 s:* native 54, reformulation without the handler 53,
  with the handler 51. The handler solves 2 instances that native SCIP does
  not (`pricing050` at the root; `arki0003`, which `split` mode, the
  reformulation plus precomputed implied bounds, also solves) and loses 5.
  Where both solve, the handler is more than twice as slow on 16 instances
  and more than twice as fast on 2. Where neither solves, the final bound is
  better on 11 and worse on 10.

**Conclusion.** Proved: cut validity for every slope (Proposition 1) and the
`n`-independent gap for separable programs (Proposition 3, cited).
Empirical: the envelope handler removes the failure of all three solvers on
separable programs with composite univariate terms, and it strengthens the
root relaxation on 35 of 81 comparable MINLPLib instances. Also
empirical: as a Python plugin the method is a net loss on MINLPLib within
120 s, because nodes become 5 to 20 times slower and instances that SCIP
solves in seconds gain nothing. Anticipated, not shown: that a native
implementation with a selection rule turns the root gains into end-to-end
gains.

## Literature

Checked by a separate agent on 2026-09-21. Several full texts were not
accessible; an unsuccessful search does not establish novelty.

- The weakness of term-wise relaxation of univariate composites and the
  benefit of treating them as a unit: Sundar–Sanjeevi–Nagarajan (2020,
  MINLPLib `ex4_1_1`: 52% against 99.99% gap), Wilhelm–Wang–Stuber (2023,
  activation functions), Najman–Bongartz–Mitsos (2019, thermodynamic and
  cost models), Li et al. (arXiv:2604.03871, 2026, polynomials).
- Exact envelopes from a convex/concave decomposition: McCormick (1976),
  Tawarmalani–Sahinidis (concavoconvex functions), per-operator Newton tie
  points in SCIP, Couenne and BARON. Li et al. give a complete bitangent
  algorithm for univariate polynomials, evaluate root-node bounds only, and
  name branch-and-bound integration as future work.
- Envelope as biconjugate: Lucet (1997), Gardiner–Lucet (2010).
- Hand-written unit treatments in solvers: SCIP's univariate quotient
  handler (Bestuzheva et al. 2023) and the Lennard-Jones example handler
  (SCIP 10.1), MAiNGO and EAGO intrinsic functions. SCIP's convexity
  detection is rule based and requires every summand to have the right
  curvature. Gurobi 13 documents a decomposition into single-operator
  univariate functions; its polynomial function constraint, which treats a
  polynomial as one function, is deprecated.
- Piecewise αBB underestimators for univariate functions:
  Gounaris–Floudas (2008). Composite relaxations with a multivariate outer
  function: He–Tawarmalani (2021, 2022), complementary to this note.

Claim: to our knowledge this is the first general-purpose and automatic
treatment of composite univariate subexpressions, with certified curvature,
in an LP-based spatial branch-and-bound solver. The envelope construction and the
term-splitting weakness are not claimed.

## Limitations

- The handler is a Python plugin, and its overhead decides the MINLPLib
  outcome. No native implementation exists, so end-to-end benefit on general
  instances is not established.
- There is no rule that predicts on which instances the handler pays off.
  On `ex6_2_*` and `ghg_*` it makes the final bound worse.
- Only univariate subexpressions are treated. A variable that also occurs
  elsewhere in the constraint keeps its other occurrences native.
- Curvature certification needs a finite interval on which `g` is `C^2`.
  Unbounded variables and `abs` are skipped.
- Floating-point evaluation of `g` is guarded by a fixed relative shift, not
  by directed rounding.
