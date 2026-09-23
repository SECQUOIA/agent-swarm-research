# Second independent review of exact recovery from surrogate cells

Date: 2026-09-06. Reviewed file:
[bilevel-reopened-approximate-structure.md](bilevel-reopened-approximate-structure.md).

**Verdict:** the stated mathematical recovery theorem is sound under its
explicit assumptions. This review found no incorrect enclosure, unsafe status
certificate, or gap in the exact recovery argument. Two small improvements to
the statement and certificates are described below. They do not invalidate
the complexity or correctness conclusion.

The reviewer independently derived the bounds and recovery argument, checked
the existing fixed-rank cover construction, and wrote an independent exact
arithmetic checker. This review does not establish publication priority or
practical speed relative to a global solver.

## Mathematical checks

For `e=z-y` and `p=(Q-Qhat)y`, the follower variational inequalities imply
`e^T Q e+p^T e <= 0`. Completing the square gives precisely the asserted
ellipsoid, including its center, radius, and factor `1/2` in support bounds.
For a gradient coordinate the output vector is `Q e_i`, so its squared dual
norm is `Q_ii`, while the center becomes `ghat_i+p_i/2`. The diagonal of
`Q^{-1}` belongs in the coordinate bound, and the diagonal of `Q` belongs in
the gradient bound; the manuscript uses both correctly. No positive
semidefiniteness assumption on `Q-Qhat` is needed.

On a compact rational polytope the convex quadratic `p^T Q^{-1}p` attains a
maximum at a vertex. This remains true for a singleton or a polytope of
smaller affine dimension. Exact vertex enumeration can select full-rank
subsets from all defining equalities and active inequalities in the fixed
ambient dimension. Every vertex has a spanning active-normal system; a
failure of spanning would permit a nontrivial feasible segment through it.
Thus degeneracy does not require a generic-position assumption. Rational
matrix operations and fixed-dimensional enumeration have polynomial bit
complexity in the explicit rational description.

The status tests are sufficient. Strict gradient signs identify the
corresponding bound; a weak coordinate enclosure can identify a bound because
the true response is in the box. Strict interiority identifies zero gradient.
Squaring comparisons only after checking the sign of the rational side avoids
spurious certification. All numbers under square roots are nonnegative.

The fixed-rank surrogate need not have positive semidefinite `H`. Positive
definiteness of `Qhat` is the relevant condition for uniqueness and KKT
sufficiency. Threshold arrangements live in `(x,w)` of dimension `r+k`.
Intersecting closed threshold cells with the affine consistency equations and
compact aggregate bounds produces exactly the type of cover required here.
Taking closures creates harmless duplicate boundary descriptions, since the
clipped affine formulas agree at thresholds.

For each completed true status assignment, `Q_FF` is invertible regardless
of how many free coordinates occur. Its inverse gives rational affine true
responses. Imposing the true bound signs and weak free-coordinate box
constraints is necessary and sufficient for the true follower KKT system.
Certified free coordinates have zero gradient; they need not be treated as
bounded variables in a reduced nonlinear problem. This is why dense
interactions among arbitrarily many certified free coordinates cause only
polynomial linear algebra, with the exponential count restricted to the
ambiguous statuses.

At a degenerate coordinate on a bound with zero gradient, either its bound
status or free status is compatible with KKT. Enumerating three statuses and
allowing weak inequalities therefore loses no feasible point. Each recovery
LP is compact because its variables remain in the supplied compact cell.
The finite union is closed, so exact response-dependent upper equalities and
inequalities introduce neither a limiting-point issue nor irrational output
requirements in this quadratic model. An attained rational optimum follows.

## Two improvements

1. The phrase "at most `M 3^t` rational linear programs" should explicitly
   count **recovery** LPs if screening extrema are also computed using LPs.
   Alternatively, calculate every affine screening extremum over the vertex
   set already enumerated for the quadratic bound. That avoids extra
   screening LP calls and makes the literal count correct. Either choice
   preserves the stated polynomial preprocessing and bit complexity.

2. A valid additional free-status certificate is
   `min_P t_i >= S_i` and `max_P t_i <= -S_i`. It proves both gradient
   bounds are zero. With the current constant-width enclosure it is useful
   when `eta_P=0`. In particular, it certifies a surrogate free coordinate
   throughout its closed cell even when that coordinate touches a bound on a
   cell face. The strict-interiority certificate alone can leave such
   coordinates ambiguous even for `Q=Qhat`. This is avoidable conservatism,
   not an incorrect claim that the parameter is always small. With the extra
   certificate an exact surrogate recovers its supplied statuses throughout
   every closed clipping cell.

The second addition can overlap a lower or upper status at a coordinate
identically on its bound with zero gradient. Those statuses are compatible;
an implementation should use a deterministic choice, not assume all sound
certificate conditions are mutually exclusive once this extra test is added.

## Independent executable checks

Run

```bash
python code/bilevel_reopened/screening_second_review.py
```

The checker imports no implementation from the theorem author. It uses SymPy
rationals, enumerates all `3^4` true active assignments, and solves the
one-leader LPs by exact interval intersection. All 20 seeded cases passed.
The saved [output](../code/bilevel_reopened/screening_second_review_results.json)
records each exact optimum or infeasibility result, cell count, and ambiguity
count.

Cases cover diagonal surrogates with dense positive semidefinite or indefinite
residuals, zero residuals, closed surrogate switching boundaries, singleton
leader domains, signed objective rows, response-dependent inequalities, and
feasible exact response-dependent equalities. On every true active piece
intersecting each surrogate cell the checker verifies every certified status
at both endpoints. Since the coordinate and gradient formulas are affine on
that piece, this checks the status implication over the full piece. It also
checks the ellipsoid inequality at those endpoints and the midpoint, then
compares the exact screened global optimum with unrestricted enumeration.

The script deliberately implements the manuscript's original strict-interior
free-status test, so its success does not rely on the suggested strengthening.
These checks exercise one-dimensional cover geometry; the general fixed
dimension conclusion rests on the proof reviewed above.

## Literature boundary

The review independently opened these primary sources:

- [Liu, Zhao, Wang and Ye, 2014](https://proceedings.mlr.press/v32/liuc14.html):
  variational-inequality enclosures and safe feature elimination are explicit
  prior work.
- [Ndiaye, Fercoq and Salmon, arXiv:2009.02709](https://arxiv.org/abs/2009.02709):
  screening from optimality conditions and active-structure identification
  have an established general framework. The arXiv record is dated 2020;
  a 2021 citation should refer to the publication version if used.
- [Yang et al., 2024](https://arxiv.org/html/2403.01769v1): a close precedent
  combines KKT conditions, variational inequalities, bound-status screening,
  and an auxiliary bilevel screening construction for nu-SVM.

These sources make a broad novelty claim about screening, VI enclosures, or
combining screening with bilevel terminology untenable. They do not supply the
specific exact global recovery theorem from a polynomial-size surrogate
response cover with a verified per-cell ambiguity parameter. The manuscript's
narrow candidate-contribution language is appropriate. A publishable paper
should emphasize that global recovery theorem and report the exact assumptions
and certificate-computation cost, while treating the underlying safe-screening
tools and active-set affine recovery as established ingredients.

## Addendum: final neighborhood corollary

The final Section 3a was independently checked on 2026-09-06: **PASS**.
Unique surrogate responses make leader projection injective on each cell;
relative-interior perturbations extend this injectivity to its affine hull,
so its dimension is at most `r`. Existing-vertex triangulation therefore
uses at most `r+1` vertices per simplex. Outside the union of their
transition coordinates, each nominal status has the stated positive affine
vertex margin, which extends throughout that simplex.

For symmetric residual `E`, the induced infinity norm bounds its spectral
norm. Thus the stated `eps_0` ensures positive definiteness with eigenvalue
at least `m/2`, response perturbation at most `2 eps R/m`, and gradient
perturbation at most `2 eps R(1+L/m)`. Both are at most `sigma/2` under the
closed radius condition. Every coordinate outside that union is therefore
soundly certified and ambiguity is at most `(r+1)q`. The polynomial
triangulation cost, bit-size bound, geometry-dependent radius, and caveat
that its exponent can exceed the initial arrangement exponent are correct.
