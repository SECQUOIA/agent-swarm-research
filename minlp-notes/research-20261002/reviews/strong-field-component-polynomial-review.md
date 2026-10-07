# Independent review of the strong-field polynomial composition

Date: 2026-10-02. Result: passed the mathematical theorem and stated bit
and output bounds. Read the complete actual
[composition](../new-direction/strong-field-component-polynomial.md)
afresh. This is a separate review from the
[component-solver review](polynomial-component-primitive-limit-review.md)
and the earlier genericity audit. No substantive correction was needed.

The result applies to explicit rational polynomials of fixed degree on
bounded closed mixed product boxes. Its expected polynomial guarantee
requires the stated noise condition; its optimization answer is exact
for the sampled objective on every draw.

## 1. Derivative enclosures and persistence

The proposed interval calculation is valid on the full continuous hull,
including hulls with negative endpoints. For a positive odd power the
endpoints give the range. For a positive even power, an interval
containing zero also requires the zero minimum, which the rule includes.
The zeroth power is handled separately. Products and signed coefficient
scaling enclose each derivative monomial; adding intervals encloses the
derivative even though different monomials share variables.

At fixed degree, each derivative monomial has only a bounded number of
factors. Its rational endpoints have polynomial bit length. Summing the
explicit input terms, including terms listed in separate supplied
factors, preserves polynomial bit work and length. The theorem uses an
enclosure, so dependencies and cancellation can weaken the noise
condition without invalidating the proof. Verification of any alternative
enclosure is explicitly included in the input and cost model.

Outside the closed bad interval, the sampled derivative is strictly
positive or strictly negative on the entire coordinate interval for
every choice of the other coordinates. Each such coordinate is therefore
at the stated original bound in every sampled-objective optimizer. The
same conclusion holds for native integer coordinates because their
successive labels lie on that real interval. Product feasibility permits
all these pins simultaneously. Equalities at a threshold remain bad and
are not discarded as measure-zero cases.

The intervals and graph are fixed before sampling. Each bad event depends
only on its own original noise coordinate; substitution does not change
the event used by the probability calculation. Thus the Bernoulli
independence in the proof is valid. There is no conditioning on a selected
component or reuse of a random post-pinning interval.

## 2. Higher-order monomials separate over the stated graph

The required graph is the primal graph of monomial supports, or an
overgraph made from factor-scope cliques. Pinning only removes variables
from a monomial support. If a surviving monomial contained variables in
two different bad components, the original support clique would supply
an edge joining those components, a contradiction. Terms with no
surviving variables become rational constants; sampled unary terms add
no edges.

This proves additive separation on the pinned product domain, including
monomials involving three or more variables. An incidence graph would
not justify the connected-set bound used here, and the statement
explicitly excludes that interpretation. Input cancellation may leave
unnecessary graph edges but cannot create a false separation.

Substitution of fixed rational bounds and enumerated native integer
labels preserves fixed degree. Each substituted polynomial has encoding
length polynomial in the original input and noise bits, uniformly over
the realized pinning choices. Thus dependence of the component
coefficients on those choices causes no additional probabilistic
requirement.

## 3. Component weights and expected work

For one component, enumerate its integer labels and keep a running best
candidate using the continuous solver's exact univariate value
comparisons. One comparison per new label suffices; the number of labels
is not squared. This gives the displayed weight

\[
 A(C)=c_d^{|C\cap\mathcal C|}
            \prod_{i\in C\cap\mathcal Z}(u_i-\ell_i+1).
\]

The fixed constant `c_d` can be chosen to cover the full component
construction and comparisons. The remaining bit factor is a fixed
polynomial in `I+b`, with an exponent independent of component size.
The solver is deterministic on every rational input, so exceptional or
degenerate finite-noise atoms need no separate fallback budget.

An interval of length `R_i` contains at most
`(M-1)R_i/(2 sigma)+1` atoms. Therefore the stated
`q_i <= R_i/(2 sigma)+1/M` bound is valid, including a singleton bad
interval. Under the sufficient regime, the two weighted contributions
are each at most `1/(16 Delta_+)`; hence
`a_i q_i <= 1/(8 Delta_+)` and `4 Delta_+ beta <= 1/2`.

The connected-set encoding is also valid: a canonical rooted ordered
spanning tree and its neighbor indices determine its vertex set.
Counting extra encodings and repeated labels only enlarges the bound
`(4 Delta_+)^(t-1)`. The event that a connected set is an entire bad
component is contained in the event that all its vertices are bad.
Independence bounds its probability by the product of the `q_i`.
Rooting and overcounting then give exactly the geometric series in the
composition. The convention `Delta_+>=1` covers isolated coordinates.

The general expectation formula retains its explicit denominator and
does not assert a uniform polynomial bound as that denominator tends to
zero. The sufficient regime supplies a uniform margin. Its least allowed
power-of-two grid has polynomial bit length: logarithms of the native
integer label counts are bounded by their binary endpoint encodings.
The potentially large numerical noise width and its dependence on those
counts remain explicit assumptions.

## 4. Exact output, refinement and replay verification

Each component keeps its optimizer coordinates in one common univariate
real-root representation, with exact integer labels. Values are compared
within that component. Independent minimizers then minimize the separated
sum without any comparison between unrelated algebraic sums.

The global output is consequently a collection of component
representations and a rational constant plus a symbolic sum of their
values. The note correctly declines to promise an expanded global
minimal polynomial or an efficient arbitrary sign test on such sums.
Output on a large realized component may be large; its size is covered
by that component's weight and the expected-work bound.

Refining each of at most `n` component values to width at most
`2^(-q)/n` yields the requested total enclosure. Combining component
points with individual gaps at most that quantity gives a feasible
rational global point with total gap at most `2^(-q)`. This adds only
`O(log n)` accuracy bits. The all-pinned case is rational and requires
no division by a zero component count.

The stated proof record is replayable within the same realized-work
bound: recompute the rational derivative bounds, pins, component
partition and separated polynomials, then replay each exact face and
label calculation. Within-component comparisons verify its selected
optimizer; additive separation verifies the global result. No comparison
with an unrelated algebraic sum is necessary. This is an exponential
record or replay on some draws, with the claimed expectation, rather
than a uniformly small optimality certificate. The random law and
independence are needed for expected work only.

Finally, sampled optimality gives
`F_0(x_gamma)-F_0(x_0) <= gamma^T(x_0-x_gamma)`.
The stated original-objective loss bound `sigma sum_i(u_i-ell_i)` follows
directly. The note correctly separates that guarantee from exact
optimization of the unperturbed objective.

## 5. Scoped additions and nonlinear diagnostic

Read the later effective-weight appendix and checked its interface with
the theorem: a fixed degree-dependent prefactor can remain outside the
component weight, while the exponential base determines the sampler's
continuous-coordinate weight. The appendix gives one fixed implementation
convention rather than an oracle for choosing an unspecified solver
constant. Its detailed arithmetic ledger has a separate review.

Read the complete
[nonlinear diagnostic](../new-direction/check_strong_field_polynomial.py)
and ran it once. Its exact whole-instance oracle enumerates all integer
labels and minimizes the resulting separable convex cubics explicitly.
The scalar minimization is correct on its required interval `[0,1]`,
including zero cubic coefficient and endpoint cases. The component path
uses that same scalar oracle, so the comparison tests pinning and
separation, not the general algebraic component solver.

The square-root expressions and their rational enclosures give exact
fixture comparisons. The code also checks inclusive threshold handling,
that no surviving monomial crosses components, feasible rational point
gaps, value enclosures, and the weighted expectation by exhaustively
summing the independent bad-site patterns. Its finite derivative probes
supplement the interval proof; they are not a substitute for full-hull
derivative certification. The illustrative weights in that counting
test are explicitly distinguished from the conservative implementation
constant.

Command actually run:

```sh
python3 -B research-20261002/new-direction/check_strong_field_polynomial.py
```

Result: passed 388 exact same-draw comparisons, 864 pins, 81
threshold-equality incidences, 18 split draws, 489 derivative probes,
29 certified rational refinements and 34 weighted patterns on four
fixture graphs. The run completed in under one second. No fixture or
implementation change was needed.

## Verification scope

Performed a complete independent mathematical and bit-complexity review,
with no further delegation for this composition. Read the final scoped
additions and executed the nonlinear checker as recorded above. A
targeted inline Python check of the composition and this review passed
local link resolution, balanced display delimiters, trailing whitespace
and sequential equation tags; the checker also passed an AST parse.
No external search, project-wide verification or CI inspection was
performed.
