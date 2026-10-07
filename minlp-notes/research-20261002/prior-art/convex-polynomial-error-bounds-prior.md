# Prior-art check: convex-polynomial growth on compact polytopes

Date: 2026-10-02. Scope: the exponent in the compact-polytope growth lemma
in [`canonical-convex-fiber-regularization.md`](../new-direction/canonical-convex-fiber-regularization.md), its relationship to classical error bounds, and what those bounds do and do not imply for point recovery. This is a focused comparison, not a novelty finding.

## The exponent in Li's results

I checked the author-hosted primary PDFs, including rendered page images. Li's
2010 paper defines

\[
\kappa(m,d)=(d-1)^m+1,
\]

with the dimension as a superscript. This is easy to misread in extracted text,
which flattens it to `(d−1)m+1`. The PDF itself is unambiguous: Definition 4.2,
printed and physical p.13, and its later example at p.16 display the power.
The paper also states explicitly that when `d=2`, `κ=2` for every dimension
(Theorem 4.2, printed p.15; Corollary 4.1, printed/physical p.16).

Li proves a global Hölder error bound for one convex polynomial on all of
`R^m`. In the notation above, the near-minimum distance exponent is
`1/κ(m,d)`: there is an existential constant `τ>0` for which
`dist(x,argmin f) ≤ τ (gap + gap^(1/κ))`. Thus on a bounded near-optimal
sublevel, this gives `gap ≥ c dist(x,argmin f)^κ`. The source is Guoyin Li,
[“On the Asymptotically Well Behaved Functions and Global Error Bound for
Convex Polynomials”](https://doi.org/10.1137/080733668), SIAM Journal on
Optimization 20(4) (2010), 1923–1943; author-hosted PDF:
[UNSW manuscript](https://web.maths.unsw.edu.au/~gyli/papers/AWB_convex_polynomial_11-12-09.pdf).
The relevant result is Theorem 4.2 and Corollary 4.1, with Lemmas 4.3–4.6
and Definition 4.2 (printed pp.13–16; physical PDF pp.13–16).

Li's 2013 paper treats a convex polynomial over a polyhedron directly by
writing `f=g+δ_P`, where `g` is convex on all of `R^n` and `P` is polyhedral.
Theorem 1 in §3.1 gives a global Hölder error bound with the same
`κ(n,d)=(d−1)^n+1`; Corollary 1 gives a compact-set version. These results
cover a compact-polytope restriction of a globally convex polynomial and its
full minimizer set, including nonunique minima. For degree two they give
`κ=2`, hence quadratic growth; for degree `d≥3`, their displayed exponent
depends on dimension and can be much weaker than `1/d`. Source: Guoyin Li,
[“Global Error Bounds for Piecewise Convex Polynomials”](https://doi.org/10.1007/s10107-011-0481-z),
Mathematical Programming 137 (2013), 37–64; the author-hosted manuscript is
[here](https://web.maths.unsw.edu.au/~gyli/papers/Li_MP_July_20_Final.pdf).
Theorem 1 is in §3.1, printed/physical pp.12–14; Corollary 1 is printed/physical
pp.14–15. Definition 3, printed/physical p.5, visibly confirms the power
formula. This comparison is based on the full author manuscript, not its
abstract.

Luo and Sturm provide a stronger quadratic special case: for any quadratic
`q` and bounded polyhedron `P`, their Theorem 3.3 gives
`dist(x,{y∈P:q(y)=0}) ≤ c |q(x)|^(1/2)` on `P` whenever that zero set is
nonempty. Applying it to `q=f−min_P f` gives global quadratic growth toward
the entire optimizer set, with no convexity assumption. This is an
existential-constant result. See [“Error Bounds for Quadratic Systems”](https://doi.org/10.1007/978-1-4757-3216-0_16),
Theorem 3.3, printed pp.11–12.

## Comparison with the compact degree-only lemma

The current lemma in [`canonical-convex-fiber-regularization.md`](../new-direction/canonical-convex-fiber-regularization.md)
assumes one polynomial `f` is convex on a compact polytope `Y`, and proves an
existential `c>0` such that

\[
f(y)-f^*\ge c\,\operatorname{dist}(y,S)^d,
\qquad S=\operatorname*{argmin}_{Y}f.
\]

This is a degree-only exponent, independent of ambient dimension. For `d=2`
it agrees with the classical quadratic-growth exponent. For `d≥3` and
`n≥2` it is stronger than the exponent `κ(n,d)` in Li's global polynomial
bounds; in one dimension, Li's exponent is also `1/d`. The lemma also
requires only convexity on `Y`, while Li's constrained theorem assumes the
polynomial is globally convex on `R^n`.

The lemma's coefficient `c` is not bounded in terms of input bit length, and
the proof uses nonquantified polyhedral and transverse-growth constants.
Therefore the stronger exponent alone does not give polynomial-precision
point recovery. It should be presented as a qualitative growth fact, with no
claim that its algorithmic constant is known or efficiently certifiable.

## What this says about regularized point selection

For a fixed compact convex fiber, adding `λ||y||²` selects the minimum-norm
point of the minimizing face as `λ↓0`; compactness gives qualitative
convergence. An error bound can turn this into a conditional rate. The rate
in the draft follows by comparing the regularized minimizer with that
minimum-norm point and substituting the growth inequality; it depends on `c`
and the fiber diameter. The cited global error-bound theorems also give only
existential constants, not a polynomial-bit parameter schedule.

The moving-core discontinuity in §3 of the same draft and the fixed-degree
precision example in
[`regularization-point-precision-obstruction.md`](../new-direction/regularization-point-precision-obstruction.md)
show limitations of independent regularization and core-accuracy schedules.
They are not lower bounds against all methods for approximating a minimizer.
For exact minimization, Jiang's [“Minimizing Convex Functions with Rational
Minimizers”](https://arxiv.org/abs/2007.01445), Theorem 1.2, covers an
integral/rational-minimizer promise. That promise does not cover a general
irrational minimum-norm point of a polynomial fiber.

## Source limits

Yang's “Error Bounds for Convex Polynomials,” SIAM Journal on Optimization
19(4) (2009), [DOI 10.1137/070689838](https://doi.org/10.1137/070689838), is
directly relevant, but only its abstract is currently available in the local
record; no exponent, hypotheses, or effectivity statement is attributed to
it here. The abstract says it applies to unconstrained and polyhedral
constrained convex-polynomial error bounds.

Ngai's 2015 paper is about systems of convex polynomial inequalities, not
just one objective. Its full author manuscript has now been retrieved and
read into the local package
[`ngai2015-global-error-bounds-for-systems`](../../literature/papers/ngai2015-global-error-bounds-for-systems/).
This note does not use its system-level theorem to claim an exponent for a
single-objective optimizer. Neither source access nor this focused search
establishes novelty.
