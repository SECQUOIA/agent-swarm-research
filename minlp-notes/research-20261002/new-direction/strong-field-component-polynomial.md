# Exact polynomial mixed-box optimization through strong fields and random components

Date: 2026-10-02. Status: direct theorem with a
[fresh independent composition review](../reviews/strong-field-component-polynomial-review.md),
a separate [arithmetic-budget review](../reviews/strong-field-polynomial-budget-review.md),
and targeted exact nonlinear diagnostics passing. No index or priority claim.

This note extends the [strong-field mixed-QP argument](strong-field-component-qp.md)
using the reviewed [constant-base polynomial component solver](polynomial-component-primitive-limit.md).
The persistence and random-component counting arguments are unchanged.
The new interface is exact algebraic component output for arbitrary
explicit fixed-degree polynomials, including every degenerate noise atom.

## 1. Input, noise, and derivative enclosures

Fix a total degree bound `d`. Let `F_0` be a rational polynomial given by
an explicit list of monomials, or a sum of polynomial factors each given
by such a list, of degree at most `d`. The domain is a nonempty bounded
closed product box. Each coordinate is a continuous rational interval
or a native-integer interval. Round integer bounds inward, reject an
empty domain, and substitute fixed coordinates. Their values are retained
for the output. Write `I` for the base input length, including the original
coordinates, rational noise half-width `sigma>0`, and the polynomial-size
preprocessing data. If no coordinates remain, evaluate the resulting
constant directly.

Let `n` be the remaining dimension and `[ell_i,u_i]` the continuous hull
of its effective coordinate domain. Build a graph on these coordinates
by joining each pair that occurs together in a nonzero displayed
monomial. Thus each monomial support induces a clique. Combining identical
monomials first can remove unnecessary edges, but is not required.
A graph that instead makes every supplied factor scope a clique is also
valid and can be more conservative. The graph is the **primal graph**;
an incidence graph between factors and variables is not used in the
component bound. Let

\[
                  \Delta_+=\max\{1,\max_i\deg(i)\}.
\tag{1}
\]

This convention includes isolated coordinates without a separate case.

For every `i`, compute rational numbers `m_i<=M_i` with

\[
      \partial_i F_0(x)\in[m_i,M_i]
       \quad\hbox{on the entire continuous hull},\qquad R_i=M_i-m_i.
\tag{2}
\]

The following explicit rule supplies these enclosures in polynomial bit
work at fixed degree. Differentiate each monomial. For a univariate power
`x_j^e`, its exact interval range on `[ell_j,u_j]` is obtained from the
endpoints and also zero when `e` is positive even and the interval contains
zero. The zeroth power has range `[1,1]`. Multiply these rational intervals
over the variables of each derivative monomial, scale by its coefficient,
and add the resulting intervals. The sum can overestimate the derivative
range because its monomials are not independent; it remains a valid
enclosure. Fixed degree bounds the number of factors in each monomial,
and all resulting rational bit lengths are polynomial in `I`.

The enclosures and graph are computed before the random draw. No tightness
assumption on (2) is made. A tighter, independently verified enclosure
may replace this rule if its verification cost is included explicitly.
The polynomial-work theorem below uses the displayed rule or another
format with polynomial verification in the counted input.

Choose a power of two `M>=2` and independently sample the original
remaining coordinate coefficients

\[
 \gamma_i\in\{-\sigma+2\sigma j/(M-1):j=0,\ldots,M-1\}.
\tag{3}
\]

The target is `F_gamma(x)=F_0(x)+gamma^T x`. Let `b=log_2 M` be the
sampling bits per coordinate. One can also sample the originally fixed
coordinates; their terms are rational constants and do not affect any
decision or probability bound.

## 2. The theorem and its strong-noise condition

Fix the component implementation and its proved work bound in advance.
For a concrete conservative choice, Section 7 gives
`c_d=2^(10000 D)`, where `D` is the least even integer strictly larger than
`d`. A smaller effective integer base with an independently proved
`c_d^k poly_d(H)` bound may replace it. This is an algorithm constant fixed
before the input and draw, not an unknown existential constant or a value
inferred from observed running times. Set

\[
 a_i=\begin{cases}
 c_d,&i\text{ continuous},\\
 u_i-\ell_i+1,&i\text{ native integer},
 \end{cases}
 \qquad
 q_i=\Pr\{\gamma_i\in[-M_i,-m_i]\},
 \qquad \beta=\max_i a_iq_i.
\tag{4}
\]

Each `q_i` is an exactly computable rational probability: count the integer
indices `j` for which the atom in (3) lies in the closed interval in (4),
using rational floor and ceiling operations and clipping to `[0,M-1]`.
This takes polynomial work in `I+b` without listing the noise grid.

**Theorem.** There is a deterministic algorithm after the draw that returns
an exact global optimizer and an exact structured value expression for
`F_gamma` on every atom of (3). If `4 Delta_+ beta<1`, its expected bit
work is at most

\[
 \operatorname{poly}_d(I+b)
 \left[1+\frac{\sum_i a_iq_i}{1-4\Delta_+\beta}\right].
\tag{5}
\]

Given an integer `q>=0`, the same output can be refined to a feasible
rational point with certified objective gap at most `2^(-q)`, and to a
rational enclosure of the optimal value of width at most `2^(-q)`, within
the bound (5) with `poly_d(I+b+q)` in place of `poly_d(I+b)`. The polynomial
exponents do not depend on the dimension or component sizes.

The exact output consists of one common univariate real-root representation
per remaining component, its coordinate polynomials and integer labels,
and the rational pinned coordinates. The global value is a rational constant
plus the sum of the component value expressions. No expansion of that sum
into one global minimal polynomial, and no efficient exact sign or equality
test for arbitrary sums of unrelated algebraic values, is claimed.

A sufficient regime giving a uniformly bounded denominator in (5) is

\[
 \sigma\ge8\Delta_+\max_i(a_iR_i),\qquad
 M\ge16\Delta_+\max_i a_i.
\tag{6}
\]

Indeed the number of equally spaced atoms in a closed interval gives

\[
 q_i\le\frac{R_i}{2\sigma}+\frac1M,
 \qquad a_iq_i\le\frac1{8\Delta_+},
 \qquad 4\Delta_+\beta\le\frac12.
\tag{7}
\]

Choosing the least power of two satisfying (6) uses polynomially many
sampling bits even when integer ranges are encoded in binary. The expected
work is then polynomial in `I+q` at fixed degree. The numerical noise
half-width can be large; (6) includes its genuine dependence on derivative
variation, graph degree, and integer label counts. Conservative derivative
enclosures can make this sufficient condition stricter.

## 3. Original-coordinate independence and exact persistence

Call coordinate `i` bad when the event in (4) occurs. If it is not bad,
one of two strict inequalities holds:

- If `gamma_i>-m_i`, the sampled objective is strictly increasing in that
  coordinate for every choice of the others. Fix it to `ell_i`.
- If `gamma_i<-M_i`, the sampled objective is strictly decreasing in that
  coordinate for every choice of the others. Fix it to `u_i`.

These conclusions follow from (2) on every real coordinate interval.
They therefore also hold between integer labels. Product feasibility
allows each such coordinate change independently, so **every** original
global optimizer has the pinned values. All the substitutions may be made
simultaneously. Threshold equalities remain bad; no finite atom is ignored.

Every bad event depends only on its own original coefficient `gamma_i`
and the fixed pre-draw data. These events are independent Bernoulli events
with probabilities `q_i`. The algorithm does not recompute random derivative
intervals after pinning to justify this claim. Optional further simplifications
are unnecessary for the theorem.

After substitution, split the objective over the connected components of
the original graph induced by bad coordinates. Each surviving monomial
lies within one component: two of its remaining variables would be adjacent
in the original primal graph. Terms with no remaining variables form a
rational constant. Unary sampled-noise terms cause no new edges. Thus

\[
                 F_\gamma= c_\gamma+
                         \sum_{C\text{ bad component}}f_{C,\gamma}
\tag{8}
\]

on the pinned product domain. Each component has its original product
domain, and these domains are independent. The fixed-degree explicit
polynomial data after substitution have encoding length polynomial in
`I+b`. This proves exact separation, even for higher-order monomials or
supplied factors whose scopes contain more than two variables.

## 4. Component work, algebraic output, and refinement

For a component `C`, enumerate its native-integer labels and invoke the
reviewed continuous polynomial solver for each label assignment. Its
deterministic all-input guarantee gives work

\[
 A(C)\operatorname{poly}_d(I+b),\qquad
 A(C)=c_d^{|C\cap\mathcal C|}\prod_{i\in C\cap\mathcal Z}(u_i-\ell_i+1)
     =\prod_{i\in C}a_i.
\tag{9}
\]

The label enumeration includes ties. The continuous solver includes
singular and positive-dimensional stationary sets through finite
deformation limits; it does not assume genericity of the finite noise.
Candidates from different labels are compared within this component using
univariate value polynomials. This operation is already included in (9).
There is no cross-component value comparison: choosing a minimizer of each
summand in (8) minimizes their sum.

Each component's output keeps all its algebraic coordinates in one common
real-root representation. In particular, evaluating a component does not
form a Cartesian product of unrelated coordinate algebraic fields. Keeping
one such representation per component also avoids multiplying their degrees
across the whole graph. Large components can have large exact output on an
individual draw; their output and construction cost obey (9). The theorem
claims an expected bound, not a polynomial output-size bound on every draw.

To enclose the total optimal value within `2^(-q)`, refine each of at most
`n` component values to width `2^(-q)/n` and add the rational enclosures
and exact constant. This adds only `ceil(log_2(max(1,n)))` accuracy bits.
For a feasible rational point, ask each component for a feasible rational
point with gap at most `2^(-q)/n`, retain its integer labels exactly, and
combine the points with the pinned coordinates. Its total gap is at most
`2^(-q)` by (8). The component solver's bound is polynomial in the additional
accuracy bits; hence the realized refinement work is bounded by

\[
 \operatorname{poly}_d(I+b+q)
                 \left[1+\sum_C A(C)\right].
\tag{10}
\]

The case with no bad coordinates uses only rational arithmetic. This is
an exact implicit algebraic answer with certified numerical evaluation,
not a claimed polynomial algorithm for arbitrary algebraic-sum comparison.

## 5. Expected work and an exact proof record

For any vertex `v`, the number of connected sets of size `t` containing
`v` is at most `(4 Delta_+)^(t-1)`. One direct encoding chooses a canonical
rooted ordered spanning tree. There are at most `4^(t-1)` tree shapes and
at most `Delta_+^(t-1)` choices of neighbor labels along its edges. Allowing
repeated labels only enlarges the count.

The probability that a connected set `S` is an entire bad component is at
most `prod_(i in S)q_i`: omit its exterior conditions and use independence.
Therefore

\[
 \begin{aligned}
 \mathbb E\sum_{C\text{ bad component}} A(C)
 &\le\sum_{S\text{ nonempty connected}}\prod_{i\in S}a_iq_i\\
 &\le\sum_v a_vq_v\sum_{t\ge1}(4\Delta_+\beta)^{t-1}\\
 &=\frac{\sum_v a_vq_v}{1-4\Delta_+\beta}.
 \end{aligned}
\tag{11}
\]

The second line intentionally overcounts each set through its possible
roots. Combining (10) with (11) proves the theorem. The algorithm remains
exact when `4 Delta_+ beta>=1`; this argument then supplies no useful
expected-work bound. The exact probabilities can certify (5) when the
simpler sufficient condition (6) fails.

A replayable global proof record contains the monomial derivative enclosures,
the strict pinning comparisons, the component partition and separated
polynomials, and each component solver's exact face/label calculation.
A verifier can recompute these operations within the same realized-work
bound. Component optimality suffices to certify global optimality without
comparing a sum of algebraic values with an unrelated number. Independence,
the random law, and the noise condition are needed only for the expectation,
not for soundness of any returned answer.

## 6. Scope and verification status

The target is the one sampled objective. For an optimizer `x_gamma` and an
unperturbed optimizer `x_0`, its original-objective loss is at most
`sigma sum_i(u_i-ell_i)`, by optimality for `F_gamma` and coordinate bounds.
The strong-noise condition can make that guarantee weak. This result does
not solve the original objective exactly, cover general nonlinear coupling
constraints, or remove the integer-label dependence of the sufficient
noise regime. Product feasibility and explicit fixed degree are essential
to the stated proof and bit bound.

The component solver supplies the structural improvement over the QP-only
antecedent. Monotonicity, primal-component separation, and subcritical
connected-set counting are standard. The component construction itself
uses classical elimination and rational-univariate ideas; its source
comparison is being handled separately through the literature workflow.
No claim of novelty or practical solver performance is made here.

The QP antecedent has not been changed.

## 7. An effective component-budget constant

Here is one deliberately loose way to make the sampler's constant fully
effective. Use schoolbook integer arithmetic, fraction-free Bareiss
determinants, tensor interpolation on consecutive integer nodes,
subresultant polynomial gcd and Bezout computations, and squarefree Sturm
root isolation and refinement. Exact signs and root matching use these
same routines. These elementary fixed implementations have a per-query
bit bound `A(L+2)^100`, where `L` counts the input encoding length and
requested precision. Matrix and fixed-three-variable interpolation inputs
are included. The exponent is a loose common upper bound: the relevant
degree, subresultant height, root separation precision, rational arithmetic,
and number of bisection nodes each have polynomial bounds well below it.
No probabilistic system-solving subroutine is used.

For the continuous component solver with dimension `k`, data length `H`,
and requested additional accuracy `q`, put

\[
 D=\min\{2j:2j>d\},\qquad B=2^{Dk},\qquad
 U=B(H+q+d+2).
\tag{12}
\]

All fixed-degree prefactors below depend only on `d`. On a face of free
dimension `r<=k`, the number of memoized monomials is at most
`binom((D-1)r+1,r)<=2^(Dr)<=B`, and the quotient dimension is
`N=(D-1)^r<=B`. Normal-form degrees in the deformation variable are
`O_d(k)`, and coefficient heights are polynomial of degree at most two
in `H+k+1`. The `O(rN^2)` linear forms have coefficients with
`O_d(k^2)` bits. Determinants have matrix order `N`, degree at most `N`
in each of two variables and at most `O_d(kN)` in the third. Their tensor
interpolation grids have at most `O_d(U^4)` nodes; sampled entries and
determinant values have polynomial height bounded conservatively by
`O_d(U^5)`. Including interpolation gives coefficient height at most
`O_d(U^8)`.

Subresultant and Sylvester determinant bounds then put gcds, modular
inverses and coordinate polynomials within degree and height
`O_d(U^12)`. Fixed-degree objective composition and its value resultant
fit within `O_d(U^18)`. Cauchy bounds, squarefree separation bounds,
derivative bounds for evaluation, and the additional `q` bits require
at most `O_d(U^25)` precision. This allows a generous common bound
`C_d U^50` for the full encoding length of every primitive query,
including isolating endpoints and dense arrays. The at most `3^k<=B`
faces, `O(rN^2)` forms per face, coordinate directions, interpolation
nodes, roots and comparisons require at most `C_d U^10` such queries;
the elementary table-building loops fit the same budget.

Consequently this fixed implementation has bit work at most
`C'_d U^5010`. In particular a valid explicit bound is

\[
 T(k,H,q)\le C''_d\,2^{10000Dk}(H+q+1)^{10000},
 \qquad c_d=2^{10000D}.
\tag{13}
\]

The factor depending only on `d` stays in the polynomial prefactor. It
does not need to be multiplied into the weight at every vertex. This
budget is conservative; its purpose is to specify a computable noise law,
not to recommend a practical implementation or noise magnitude.

## 8. Targeted nonlinear diagnostic

The [exact checker](check_strong_field_polynomial.py) uses rational
arithmetic and canonical square-root expressions. Its fixtures become
separable convex cubics after fixing integer labels, so integer enumeration
and their explicit scalar minimizers give an independent whole-instance
oracle for this restricted class. The component and whole-instance paths
share that scalar oracle. They test persistence and separation, not the
general algebraic component construction, whose distinct diagnostic is
linked in its own note.

The fixtures include fourth-degree integer terms, a three-variable monomial
hyperedge, a connected hyperedge-plus-tail graph, negative integer bounds,
two continuous algebraic components after pinning, and finite-grid derivative
threshold equalities. The checker compares original whole-instance answers
with component answers, probes derivative enclosures on the real hull,
and checks feasible rational point gaps and optimal-value enclosures.
It separately sums the weighted component cost over every bad-site pattern
on the four fixture graphs. Those counting checks use illustrative positive
weights, not the large conservative implementation constant in (13).

Command actually run:

```sh
python3 -B research-20261002/new-direction/check_strong_field_polynomial.py
```

Result: 388 exact same-draw comparisons, 864 coordinate pins, 81 retained
threshold-equality incidences, 18 draws with multiple remaining components,
489 full-hull derivative probes, 29 certified rational refinements, and 34
weighted bad-site patterns across four expectation bounds passed. These
finite checks supplement the proof. No project-wide verification or CI
inspection was run.
