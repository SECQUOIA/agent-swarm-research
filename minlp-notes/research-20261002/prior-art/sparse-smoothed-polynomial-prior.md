# Prior-art audit: sparse smoothed polynomial optimization

Date: 2026-10-02. This focused comparison covers the proposed extension of
the sparse bag-cell method from quadratic to fixed-degree polynomial factors,
with a finite rational law of independent ambient linear perturbations and
exact output on every draw. The polynomial theorem is still under
development; this note audits its proposed components and does not validate
the proof or claim priority.

## Candidate scope and proof obligations

The working model is a bounded rational mixed product box and an explicit
rational polynomial objective of fixed degree, with every factor scope in a
supplied tree decomposition of maximum bag size `p`. Each coordinate gets an
independent linear perturbation from a finite rational grid selected from the
base input before sampling. The intended result is an expected fixed-width
polynomial bit bound and an exact optimizer/value representation for every
draw. A same-draw exact algebraic fallback covers exceptional draws; the
good-draw route uses sparse bag-cell pruning, active-bound and integer-label
recovery, and a verified strongly convex patch. No claim is made here that
this construction has passed its pending mathematical reviews.

Three distinct questions must remain separate:

1. Does linear perturbation produce a useful global growth constant and
   active-gradient margins with high probability under the selected finite
   law?
2. Does sparsity make the expected retained-cell work polynomial for fixed
   `p`?
3. Can the exceptional draws be solved exactly with a cost whose dependence
   on the perturbation's bit length has an absolute polynomial exponent?

The existing [sparse quadratic audit](sparse-bag-cell-smoothed-qp-prior.md)
already covers the expected semiconcave bag-row count, tree-decomposition
DP, discrete smoothed isolation, and quadratic exact closure. The polynomial
extension should be presented as a higher-degree extension of that core
method, not as a new semiconcavity or tree-DP principle.

## Genericity and conditioning under linear tilts

Lee and Phạm's 2017 Theorem A is the closest qualitative result for linear
objective perturbations. On a fixed regular closed semialgebraic feasible
set, for an open dense set of tilt vectors, nearby objectives of the form
`f(x)-u'x` have unique minimizers, uniform *local* quadratic growth, and a
global sharp-minimum inequality. On a compact feasible set, the last
inequality implies a qualitative *global* quadratic-growth bound: if
`Delta=f_u(x)-f_u(x(u))` is bounded above by `M`, then
`Delta+sqrt(Delta) <= (1+sqrt(M))sqrt(Delta)`, so Theorem A's
`Delta+sqrt(Delta) >= c_3 ||x-x(u)||` yields
`Delta >= [c_3/(1+sqrt(M))]^2 ||x-x(u)||^2`. Compactness bounds `M`, but
the theorem gives no effective lower bound on this derived constant in terms
of input data. In this paper, “regular” means the equality gradients and
active inequality gradients in a chosen basic semialgebraic description are
linearly independent (LICQ; Definition 3.1, citing the authors' constraint
qualification reference). It does not mean variational normal regularity.
A bounded mixed box meets this hypothesis: encode each integer coordinate
`z_j` by the polynomial equality
`prod_{k=l_j}^{u_j}(z_j-k)=0`, whose derivative is nonzero at each allowed
label, and encode positive-width continuous intervals by their two linear
inequalities. The active gradients then occupy distinct coordinate
directions. Substitute fixed continuous coordinates first. This is a
qualitative semialgebraic encoding; its expanded degree can grow with the
integer-domain size, and Lee–Phạm give no complexity bound for constructing
or using it. Since the exceptional tilt set is lower-dimensional, any
absolutely continuous linear-tilt law has the theorem's uniqueness and
qualitative global growth almost surely on this fixed compact mixed box.
That does not transfer to a finite grid with atoms on the exceptional set or
give a quantitative growth margin.
[[lee2017-generic-properties-for-semialgebraic-programs]] Definition 3.1
p.9; Theorem A p.3-4

For compact feasible sets, Lee and Phạm's 2016 Theorem 6.1 gives an open
dense semialgebraic set of coefficients of the *whole bounded-degree
polynomial objective* for which the global minimizer is unique and satisfies
global quadratic growth and strong second-order sufficiency. This is a
strong qualitative genericity precedent, but it perturbs in the full
polynomial-coefficient space. It does not imply the same result for a
perturbation restricted to the linear-coefficient subspace, and it gives no
effective growth modulus or smoothed algorithm. [[lee2016-stability-and-genericity-for-semi]]
p.20-21

Nie's genericity result for KKT regularity and finite Lasserre convergence
provides another established route to nondegenerate local optimality
conditions. It uses coefficient-polynomial exceptional sets and, for finite
SOS convergence, also requires archimedeanness plus constraint
qualification, strict complementarity, and second-order sufficiency at all
global minimizers. It gives neither a numerical lower bound on a growth or
active-gradient margin nor a uniform relaxation-order or expected-runtime
bound. Generic regularity of stationary points should not be conflated with
the candidate's quantitative global event bounds. [[nie2013-optimality-conditions-and-finite-convergence]]
p.2-3, p.10-16

Thus qualitative global growth after continuous linear tilting is already a
classical consequence on compact regular semialgebraic domains. The project's
reviewed [linear-tilt growth tail](../new-direction/proximal-growth-tail.md)
is quantitatively sharper: it bounds the probability of small *global point*
growth for arbitrary compact feasible sets under independent continuous
coefficient tilts, then transfers the bound to a single finite rational grid
through a coefficient-height-free component bound. The proposed polynomial note
[`polynomial-finite-noise-tails.md`](../new-direction/polynomial-finite-noise-tails.md)
states that transfer for mixed boxes. Its primary elimination ingredient is
Renegar's fixed-block quantifier-elimination theorem, not a generic Morse
argument. That note's proof review is separate from this prior-art audit.

## Fixed-block elimination and exact fallback

Renegar's Part III Theorem 1.1 is the strongest directly checked source for
the finite-noise component bound. For a first-order formula with `omega`
alternating quantified blocks, `ell` free variables, block sizes `n_b`,
`m` polynomial atoms, and maximum degree `d`, it outputs a disjunction of
conjunctions with the number of output terms, atoms per term, and polynomial
degrees bounded by `(m d)^(2^{O(omega)} ell product_b n_b)`. In the integer
bit model, output coefficient lengths have the same algebraic growth factor
times the input coefficient bit length. Theorem 1.1 is on printed p.330
(journal page 330; the stored PDF is the primary source).
[[renegar1992-on-the-computational-complexity-and]] p.1-2

For the proposed bad-growth scalar section, the formula has two blocks of
`n` variables, one free noise coordinate, fixed degree, and a quantifier-free
description of the mixed box. Listing each native-integer label contributes
at most the sum of the domain cardinalities to the formula length/atom count;
for binary-encoded interval bounds this is `2^poly(I)`, so its logarithm is
polynomial in the base input length `I`. Renegar's bound is therefore
`2^poly(I)` in size and degree, uniformly in the other fixed noise values,
the growth threshold, and their coefficient heights. In one free variable,
the output polynomials have at most that many roots in total. Their signs,
and hence the good-growth event and its complement, have at most
`2^poly(I)` interval or point components. This is the needed finite-grid
discrepancy input; it does not require all stationary points to be isolated.
The derivation and exact atom count are recorded in the separate
[finite-noise tail note](../new-direction/polynomial-finite-noise-tails.md).

For the exact fallback, the argmin set on a compact mixed box is itself
defined by a one-block formula with `x` free:

```text
D(x) and for all y: (not D(y)) or F_gamma(y) - F_gamma(x) >= 0.
```

Finite integer domains can be encoded by finite disjunctions, so this remains
a semialgebraic formula even when the optimizer is tied or its set has
positive dimension. Renegar/Basu-Pollack-Roy quantifier elimination followed
by a real-algebraic sample-point routine can return a compact univariate
representation of one optimizer; it need not enumerate nonsingular KKT
points or assume uniqueness. Basu, Pollack, and Roy's Theorem 1.3.1 states a
one-block elimination bound and explicitly separates formula length from
degree-dependent coefficient growth. Their sampling results provide
univariate representations of sample points. [[basu1996-on-the-combinatorial-and-algebraic]]
p.3-5, p.7-8; [[basu2006-algorithms-in-real-algebraic-geometry]] p.524-527

Basu, Pollack, and Roy's Algorithm 14.9 is a direct global-optimization
precedent: it introduces the objective value, eliminates the decision
variables, samples critical values, and returns a minimizer when one exists.
Its stated arithmetic complexity is `s^(2k+1) d^(O(k))` for `s` constraints
in `k` variables; it has no sparsity or smoothed-runtime guarantee.
[[basu2006-algorithms-in-real-algebraic-geometry]] p.567-568

The precise fallback target `B_base poly(I+J)`, with `J` the perturbation
coefficient bit length and `B_base=2^poly(I)` chosen before sampling, is an
inference from the fixed-degree elimination and algebraic-sampling bounds,
not a bound stated verbatim by Algorithm 14.9. Renegar's bit-size result is
important here: the algebraic height factor depends on dimensions and degree,
not on the number of atoms, while the input coefficient height enters
multiplicatively. For fixed degree and `n<=I`, all dimension/atom factors can
be absorbed into `B_base`; the remaining dependence on `J` is polynomial
with an absolute exponent. The implementation still needs to state the
chosen algebraic-number representation and account for its root isolation
and exact sign tests. A generic CAD bound with a doubly-exponential
dimension exponent would not establish this precision separation.

This exact fallback is a standard but expensive global method. Its role is
only to solve rare exceptional draws; it does not replace the candidate's
expected sparse-DP work and does not make arbitrary-dimensional polynomial
optimization polynomial-time.

The exact representation also needs an evaluation contract. Dadush's
Theorem 2.5.9 is a related ellipsoid weak-optimization result for a centered
convex body with weak membership and rational value oracles (printed
dissertation p.48), but it states an oracle arithmetic-operation bound and
does not alone prove a Turing bit bound. For that claim, use the direct
Turing-model result in Grötschel, Lovász, and Schrijver's
*Geometric Algorithms and Combinatorial Optimization*. Section 1.2 defines
the oracle Turing-machine model and polynomial
answer-length convention, §1.3 specifies binary rational arithmetic, and
§4.1 explains that an oracle-polynomial reduction becomes ordinary Turing
polynomial time when its oracle runs in polynomial time. Theorem 4.2.2,
Remark 4.2.5, and Corollary 4.2.7 (printed pp.105–106) give the
weak-separation-to-weak-optimization reduction for circumscribed bodies.
The project's [capped-epigraph reduction](../new-direction/convex-patch-evaluation.md)
turns minimization on the box into linear optimization over a compact convex
epigraph. Its rational value and gradient evaluations give exact rational
weak separation at rational queries. Applying GLS directly establishes
polynomial query and intermediate bit complexity in the encoding lengths of
the body bounds, oracle inputs/outputs, and rational tolerance.

GLS weak optimization returns an almost-feasible rational point, not
necessarily a point in the epigraph (WOPT, Problem 2.1.10, printed p.50 /
physical p.62). A rational cleanup gives the needed feasible enclosure. Let
the WOPT output be `(x,t)` at tolerance `eta`, let
`bar_x` be the coordinatewise projection of `x` onto `B`, and let `G` be a
rational upper bound on `||grad f||` on `B`. Since `(x,t)` is within `eta`
of the epigraph, `b=f(bar_x)` is feasible and satisfies
`b <= t+(G+1)eta`. Let `(c,W+1)` be the center of the known radius-`r`
inner ball in the capped epigraph, and let `(x*,f*)` be a minimizer. The
homothetic point `(1-eta/r)(x*,f*)+(eta/r)(c,W+1)` lies in the eta-deep
epigraph. Because `|f*|<=W`, its objective is at most
`f*+eta(2W+1)/r`; WOPT therefore gives
`t < f*+eta[1+(2W+1)/r]`. Thus the rational lower endpoint
`a=t-eta[1+(2W+1)/r]` satisfies `a<=f*<=b`, and
`b-a <= eta[G+2+(2W+1)/r]`. Choosing `eta` as the desired value tolerance
divided by this rational factor, and small enough that `eta<=r`, has bit
length polynomial in the accuracy and input lengths. Strong convexity then
turns value tolerance of order `tau_H 2^(-2q)` into `q`-bit optimizer
accuracy, including at boundary minimizers. This is a source-backed
evaluation bridge, not a sparse expected-time result or an exact-global-search method. Dadush's local
source is [the dissertation text](../../research-20260927/common-range-prior-sources/dadush-thesis-2012.txt)
and [PDF](../../research-20260927/common-range-prior-sources/dadush-thesis-2012.pdf);
the GLS primary text is in the local
[source package](../../literature/papers/grotschel1988-geometric-algorithms-and-combinatorial-optimization/).

## Polynomial and sparse optimization precedents

The sparse-QP audit already records the closest random-objective comparisons.
Beier–Vöcking and Röglin–Vöcking bound discrete winner gaps or pseudopolynomial
smoothed complexity for finite integer optimization. The readable
Beier–Vöcking source is their 2004 STOC proceedings paper; the local package
slug starts with `beier2006` because a separate 2006 journal record was
initially catalogued, and that journal version remains unread. Röglin–Vöcking
define polynomial smoothed complexity with a high-probability tail/moment
condition; this is not itself an ordinary expected Turing bit-time bound.
Kelner–Nikolova bound
expected projected-shadow enumeration for low-rank quasi-concave optimization
under random rotation. None gives the candidate's expected count of
near-optimal continuous polynomial bag cells under independent additive
linear coefficient noise, or exact cell closure on each finite-noise draw.
These differences are model differences, not evidence that every possible
smoothed polynomial formulation is new. [[beier2006-typical-properties-of-winners-and]]
p.3-4, p.9-10; [[roglin2007-smoothed-analysis-of-integer-programming]]
p.3-8, p.21-28; [[kelner2007-on-the-hardness-and-smoothed]] p.2-4

For sparse polynomial optimization, Faenza, Muñoz, and Pokutta give
treewidth-based LP approximations for polynomial objectives, including
QCQPs, with inverse-accuracy-dependent formulation size. Sparse moment/SOS
hierarchies give convergent relaxations under running-intersection and
positivity assumptions; finite extraction requires additional flatness or
regularity conditions. These are important width-based and exactness
precedents, but they do not give an expected exact algorithm under random
linear objective coefficients. The already-reviewed comparisons and
assumption details are in the [sparse-QP audit](sparse-bag-cell-smoothed-qp-prior.md)
and [shell-certificate audit](nonlinear-shell-certificate-prior.md).
[[faenza2022-new-limits-of-treewidth-based]] p.6-15;
[[lasserre2006-convergent-sdprelaxations-in-polynomial-optimization]] p.6-16;
[[nie2013-optimality-conditions-and-finite-convergence]] p.2-3, p.10-16

De Loera et al. give an FPTAS for nonnegative polynomial objectives on
bounded mixed-integer polytopes in fixed *total dimension*. For arbitrary-sign
polynomials they prove only a weaker range-relative approximation (and rule
out the usual PTAS unless `P=NP` under their model). This is a strong
polynomial-optimization baseline, but its dimension is fixed rather than
its interaction width, its main result is approximate, and it does not use
random objective perturbations. [[loera2008-fptas-for-optimizing-polynomials-over]]
p.1-3, p.11-15

The literature also contains generic Morse/KKT claims and finite stationary
root counts. Those can justify a finite active-face argument for appropriate
regular perturbations, but they are not substitutes for global optimizer
selection: stationary points can be nonoptimal, flat components can occur
for exceptional finite-grid atoms, and local second-order sufficiency does
not imply a global growth modulus. The exact fallback above should therefore
be described as quantifier-based global optimization; a proof based only on
enumerating generic stationary roots would not cover every draw.

## Assessment and boundary

The standard ingredients are well established: generic uniqueness and
regularity under suitable coefficient perturbations; exact real
quantifier elimination and algebraic sampling; global optimization by
critical values; semiconcave grid counting; sparse tree-decomposition DP;
and SOS or fixed-dimension polynomial approximation. The candidate's
potential contribution is the combination that turns a *finite* independent
linear-noise law into a height-uniform expected count of retained polynomial
bag cells, uses sparse DP and a curvature/growth-based exact closure on good
draws, and retains an every-draw exact algebraic fallback whose base-case
exponential work is independent of sampling precision except for a polynomial
bit factor.

That is a scoped comparison, not a novelty conclusion. The completed
candidate theorem has since passed independent reviews of the sparse
polynomial closure, finite-law tail transfer, exact fallback, and rational
GLS evaluation interface. Targeted exact checks recorded in the review
cover the expected-work budget and finite-grid endpoint atoms. This does not
establish publication priority or practical performance. The focused search
did not identify a primary source matching the full expected exact
sparse-width claim; this limited search result is not evidence of absence.

## Sources examined

- Renegar (1992), Part III, Theorem 1.1, primary full text and PDF checked;
  fixed-block output counts and integer coefficient-height dependence.
- Basu, Pollack, and Roy (1996), Theorem 1.3.1 and sampling discussion,
  primary full text checked; one-block quantifier elimination and algebraic
  sample-point representation.
- Basu, Pollack, and Roy (2006), second-edition book, Algorithms 13.2 and
  14.9 as located in the local source notes; global symbolic optimization and
  real-algebraic sample points.
- Dadush (2012), Theorem 2.5.9, primary dissertation PDF p.48; ellipsoid
  weak optimization from membership and rational value oracles in the
  theorem's oracle arithmetic-operation model.
- Grötschel, Lovász, and Schrijver (1988), §§1.2–1.3, §4.1, Theorem 4.2.2,
  Remark 4.2.5, and Corollary 4.2.7, primary full text checked; Turing
  encoding conventions and polynomial-time WSEP-to-WOPT reduction. WOPT
  allows an almost-feasible output, so the project's rational projection
  cleanup is a separate application argument.
- Lee and Phạm (2016, 2017), Theorem 6.1 and Theorem A, primary local full
  texts checked; polynomial-coefficient genericity versus generic linear
  tilts and local/global growth distinction.
- Nie (2013), Theorems 1.1–1.2 and generic KKT section, local primary full
  text checked.
- The local prior-art notes for sparse smoothed QP, shell certificates, and
  polynomial finite-noise tails, used for the already-audited comparisons.

No literature knowledge-base files were changed. No project-wide checks or
CI inspection were run.
