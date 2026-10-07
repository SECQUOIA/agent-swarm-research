# Prior-art audit: point approximation for globally convex polynomials

Date: 2026-10-02. This focused comparison covers the candidate
[effective global-convex polynomial point theorem](../new-direction/globally-convex-polynomial-point-oracle.md).
The candidate has passed two independent actual-file proof reviews, linked
from its theorem file. This is a literature comparison, not a proof review
or publication-priority claim.

## Candidate contract

For a fixed degree bound `D`, the input is an explicit rational polynomial
`f` of degree at most `D`, promised convex on all of `R^n`, and a nonempty
bounded rational polytope `P`. The candidate computes a rational constant
`Gamma` with `log Gamma=poly_D(I)` and proves, for feasible points of gap at
most one,

```text
dist(x,argmin_P f) <= Gamma (f(x)-min_P f)^(1/D).
```

Together with ordinary convex value optimization, this yields deterministic
bit-polynomial approximation in `I+q` to the optimizer set, and to the
minimum-original-Euclidean-norm optimizer, at distance `2^-q`. The effective
constant is the main algorithmic feature: it converts a requested point
accuracy into a value tolerance whose binary length is polynomial in the
input and `q`. The theorem does not return exact active labels or a short
expanded algebraic optimizer.

The ambient global-convexity premise matters. The argument evaluates `f`
outside `P`, and the source-level claims below concern globally convex
polynomials or polynomials convex on all of Euclidean space. The candidate
does not cover every polynomial that happens to be convex only on the
bounded feasible polytope.

## Direct error-bound prior: Li

Li's 2010 result is for the unconstrained minimizer set of one polynomial
convex on all of `R^n`. It is a qualitative global-convexity baseline, but
the candidate's constrained optimum over `P` is matched more directly by
Li's 2013 theorem below. Definition 4.2 sets
`kappa(n,D)=(D-1)^n+1`; Theorem 4.2 and Corollary 4.1 give a global
Hölder error bound to the full minimizer set with distance exponent
`1/kappa(n,D)` and an existential function-dependent constant. It is a
qualitative prior for unconstrained global-convex polynomial error bounds. The
constant is not presented as a polynomial-time-computable rational with a
bit bound. For `D=2` the exponent is `1/2`; for degree three it grows
exponentially with dimension in this formula. The source was checked in the
author manuscript, including the superscript in the exponent: Definition
4.2 is p.13, Theorem 4.2 p.15, and Corollary 4.1 p.16.
([Li 2010](https://doi.org/10.1137/080733668); [read local primary
package](../../literature/papers/li2010-on-the-asymptotically-well-behaved/paper.md).)

Li's 2013 theorem is an even closer domain match. It considers
`g+delta_P`, where `g` is convex on all of `R^n` and `P` is a polyhedron.
Theorem 1 gives the same exponent `1/((D-1)^n+1)` with an existential
constant; Corollary 1 gives the constrained residual form and a compact-set
specialization. It does not give an input-computable bit bound for the
constant. Thus the candidate should not claim the qualitative error-bound
principle or the use of a Hölder bound as new. Its comparison is the
degree-only exponent `1/D` together with an explicit polynomial-bit
constant and a resulting dimension-independent polynomial-time point
approximation under fixed `D`. For an objective of actual degree `D>=4` in
dimension greater than one, `1/D` is stronger than Li's displayed
dimension-dependent exponent; if the input degree bound exceeds the actual
degree, or in low degree, that exponent comparison need not hold. For
degree at most three, global convexity forces the cubic part to vanish, so
exact convex-QP algorithms already settle the point-output task. The
candidate is algorithmically distinct from Li primarily through effective
constant construction.
([Li 2013](https://doi.org/10.1007/s10107-011-0481-z); [read local
primary package](../../literature/papers/li2013-global-error-bounds-for-piecewise/paper.md),
Definition 3 p.5, Theorem 1 p.12, Corollary 1 p.14.)

Neither Li source establishes that its constant is impossible to compute;
the precise statement is that the cited theorems provide an existential
constant and do not give the candidate's polynomial-bit computation
guarantee. The distinct Yang 2009 record is metadata/abstract-only, so this
audit does not infer theorem details or effectivity from it. Ngai 2015
concerns systems of convex polynomial inequalities, not just the minimizer
set of one convex polynomial, and is not used to support a single-objective
claim.

## Qualitative compact growth is broader, but not effective

The project has a reviewed lemma for one polynomial convex only on a compact
polytope: some `c>0` satisfies

```text
f(x)-f* >= c dist(x,argmin_P f)^D.
```

That lemma has the same degree-only exponent as the candidate and applies
under the weaker domain-restricted convexity assumption. Its proof leaves
the transverse growth, interior-ray, and polyhedral constants existential;
it does not bound their encoding length. The candidate's global convexity
assumption buys a computable rational constant with polynomial bit length.
This is the relevant boundary: the exponent alone is not enough for
polynomial-precision point output. The separate
[regularization precision example](../new-direction/regularization-point-precision-obstruction.md)
also cautions against turning an existential growth constant into a
polynomial-bit regularization schedule. That example is a compact-box
limitation and is not claimed to satisfy the candidate's stronger
all-space convexity premise.

## Value optimization and degree-two cases

The GLS ellipsoid-oracle framework gives weak convex optimization from weak
separation; for a rational fixed-degree polynomial on a rational polytope,
rational gradients and the constraint rows provide the required
separation interface. This supplies objective-gap approximation, not
distance to a chosen optimizer. A growth/error bound is what converts the
former to the latter. The candidate's contribution over this baseline is
the effective bound, not a new convex value-optimization method. The source
locators and the rational bit-model inference are recorded in the local
[GLS package](../../literature/papers/grotschel1988-geometric-algorithms-and-combinatorial-optimization/paper.md),
Corollary 4.2.7 and §4.1.

For degree two, Kozlov, Tarasov, and Khachiyan give deterministic exact
rational convex-QP output, including an attaining point for singular PSD
Hessians and nonunique minima; clearing denominators extends their integer
input statement to rational data. Degree-three global convex polynomials
are also quadratic: their affine Hessian must be positive semidefinite at
every point of `R^n`, forcing its linear part to vanish. Thus the
all-space theorem's new algorithmic range begins at fixed degree at least
four. The exact QP baseline is stronger in output at degrees two and three.
([KTK 1980](https://doi.org/10.1016/0041-5553(80)90098-1); [read local
primary package](../../literature/papers/kozlov1980-the-polynomial-solvability-of-convex/paper.md),
pp.1–5.)

Kannan–Rademacher's low-dimensional polynomial-perturbation algorithm is
the central comparison for the separate coupled-core theorem, documented
in the [coupled-polytope audit](coupled-polytope-core-value-oracle-prior.md).
It returns range-normalized objective accuracy after a grid in the
polynomial's selected coordinates. It does not itself give point distance
or an effective global error bound. Taking the whole polynomial as its
perturbation also makes the grid dimension `n`; its stated accuracy cost
does not yield this candidate's dimension-independent polynomial bit-time
point guarantee.

## Comparison boundary

The examined sources establish global convex-polynomial error bounds,
convex value optimization, and exact rational output for convex QPs. The
project's compact-polytope lemma already establishes the degree-only growth
exponent qualitatively. The specific candidate claim is narrower and
quantitative: under global convexity and fixed degree, compute a rational
error-bound constant with polynomial encoding length, then use it for
deterministic point-distance and fixed minimum-norm-selector approximation
in polynomial bit time. This note records no result showing that the
effective constant is new or that no equivalent theorem exists.

## Source status

Li 2010 and Li 2013 full author manuscripts, GLS 1988, and Kozlov–Tarasov–
Khachiyan 1980 are read in the local primary-text packages linked above.
The compact-polytope growth lemma is an internal reviewed result. Yang 2009
is metadata/abstract-only and is not used for theorem-level claims. No new
literature package or index entry was created for this audit.
