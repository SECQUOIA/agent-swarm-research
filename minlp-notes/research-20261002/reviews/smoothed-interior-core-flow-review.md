# Independent review: core-only smoothing with interior core and integer-flow recourse

Date: 2026-10-02. Verdict: **passed** for the complete actual
[flow theorem](../new-direction/smoothed-interior-core-flow.md).
No substantive mathematical correction was requested. This is a fresh
composition review, not a publication-priority assessment.

I read the entire theorem, the relevant exact-oracle, algebraic-output,
and finite-growth sections of the
[native-integer predecessor](../new-direction/smoothed-native-integer-recourse.md),
the [tube interface](../new-direction/core-noise-active-stratum-tube.md),
and the [boundary obstruction](../new-direction/core-only-flow-boundary-obstruction.md).
The theorem uses ordinary algebraic completion in the small core, rather
than a local positive-Hessian closure. Persistent integer-flow ties are
therefore compatible with its output and stopping argument.

## 1. Exact residual certificates and their polynomial charts

For a fixed feasible integer flow, the available residual arcs depend
only on that label and the fixed native bounds. They do not change with
the core. Every forward or backward unit marginal is a polynomial in
the core of degree at most `d`. Convexity of the arc costs implies the
usual residual-circulation lower bound on any other feasible integer
flow's objective difference. Nonnegative reduced marginal costs are
therefore sufficient for global conditional optimality.

At an optimal queried flow there is no negative residual cycle. Adding
a zero-cost source makes every node reachable and yields finite rational
shortest-path distances. The draft correctly chooses an arborescence
by searching the tight-edge graph. Arbitrarily retaining predecessor
edges could create a zero-cost predecessor cycle; the stated procedure
does not. Every source-to-node tree path has at most `s` edges. Its
polynomial path sum equals the shortest-path distance at the query.

The resulting reduced-cost polynomials are nonnegative at the query.
Testing them nonnegative on the entire retained box is an exact uniform
flow certificate. Identically zero polynomials must pass, and the draft
does not impose an artificial strictness requirement. Including the
added source arcs causes no difficulty; it can make a chart more
restrictive, but remains a sound sufficient certificate.

Each whole-box sign decision has only `k` quantified core variables,
fixed polynomial degree, and polynomial coefficient height. Thus the
small-core algebraic factor is parameter-only; coefficient length has
a fixed polynomial exponent. There are at most `2r+s` decisions per
level, rather than one algebraic solve for every generated corner.

## 2. The finite chart universe is used only for analysis

The native label bound `R_Z=product_a(u_a-l_a+1)` has polynomial binary
length even when the number of labels is exponential. For one label,
there are at most `(2r+s)^s` possible augmented arborescences and at most
`2r+s` reduced-cost polynomials per tree. The stated finite family count
is consequently valid. Polynomial path lengths and fixed polynomial
degree also give base-only coefficient heights.

Discarding an identically zero polynomial from the exceptional set is
correct: its certificate inequality is true everywhere. Every retained
nonconstant nonzero polynomial has a zero set of dimension at most
`k-1`; a nonzero constant contributes no zero. The finite union `S`,
restricted to the closed core box, is compact and lower-dimensional.

If a connected retained box avoids `S`, every nonzero reduced-cost
polynomial of its selected chart has constant sign there. At the selected
corner its value is nonnegative and cannot be zero, hence the sign is
positive throughout the box. The identity polynomials remain zero.
Thus avoiding `S` really is sufficient for the computed chart to pass,
including charts chosen adaptively after sampling.

The ordinary algorithm neither constructs the full chart family nor
enumerates its labels. It computes a single flow, one tight tree, and
its polynomial inequalities. The large family only determines logarithmic
precision bounds. Charging its enumeration to ordinary work would break
the theorem; the actual algorithm does not do so.

## 3. Interiority and the cross-label exceptional image

At a global core optimum `a`, any attaining flow `w` has
`F_w(v)+gamma'v>=V_gamma(v)>=V_gamma(a)=F_w(a)+gamma'a`.
Hence `a` minimizes every attaining smooth slice globally. The supplied
interiority hypothesis gives `gamma=-grad F_w(a)` without requiring
differentiability of the lower envelope or uniqueness of `w`.

The draft's exceptional image takes the gradient image of the entire
chart-boundary set for **every separate flow label**. This cross-label
construction is essential: the label attaining the original optimum
need not define the chart boundary nearest that optimum. Polynomial
maps preserve the upper semialgebraic dimension bound, and the union
is finite and compact. Therefore the image is lower-dimensional.

The one-block image formula has `k` quantified and `k` free variables,
`O(k)` atoms, and fixed degree. Fixed-block elimination yields a
parameter-only output-format bound. For an image piece with empty
interior, every point must annul a nonconstant polynomial atom in its
quantifier-free formula; otherwise all atom truth values would persist
on an open neighborhood. Removing zero and constant atoms before taking
the product is correct. The product is nonzero. Empty pieces contribute
the constant one.

The separate gradient-label factor gives the square `R_Z^2` in the
degree bound. The claimed
`R_Z^2(2r+s)^(s+1) A_d(k)^3` is safe, and its logarithm is polynomial
in the base input. Neither the chosen sample nor its precision enters
this algebraic degree bound. The solver computes this bound, not the
eliminated polynomials.

## 4. Finite-law probability and the stopping budget

The cited singular-algebraic-set tube estimate applies to the nonzero
polynomial enclosure. Its dimension, degree, and coefficient-independent
constant have the required quantitative bounds. The grid-jitter reduction
includes atoms on the exceptional image through its `sqrt(k)/M` term;
an almost-sure continuous-noise argument alone would not suffice.

The projected-growth predicate uses only the core distance. Residual ties
therefore do not force its margin to zero. Native integrality introduces
exponentially many atoms, but only polynomial logarithmic format length
and two quantifier blocks. The reviewed fixed-block bound consequently
still gives `C_growth=2^{poly_d(I)}`. This bound is not obtained by running
the large elimination as part of each optimization call.

With `rho=1/(4B)`, the chosen `g_0` and finite-grid correction make growth
failure at most `rho`. The tube radius `H_2 delta` contributes `rho/4`,
and its mesh term contributes at most `rho/4`. Their combined failure
probability is at most `3rho/2<1/(2B)`.

On the good event, (9) indeed implies `dist(a,S)>delta`; its inequality
direction is correct. The retained-hull bound is in infinity norm, so
using `k A_0 h` as a Euclidean upper bound is safe. The cutoff leaves
every point of the hull within `delta/2` of `a`, hence disjoint from `S`.
The computed chart then passes by Section 2 of this review. If `S` is
empty, all relevant signs are already constant and the argument needs
no proximity event or special recognition procedure.

All cutoff constants precede the choice of `M`. Their logarithms and
the resulting `J,log M` are polynomial in the base input. The same-draw
fallback has a base-only exponential factor and fixed polynomial sample-
height dependence, so its expected contribution is polynomial. There is
no noise-height/reconstruction circularity and no resampling of exceptional
atoms.

## 5. Whole-core closure, total cost, and output meaning

Once a flow is uniformly optimal on the retained hull, at least one
original global optimizer uses that flow. Minimizing the same flow on
the entire original core box is therefore exactly equivalent in optimal
value. Its optimizer need not remain in the retained hull; it is still
feasible in the original problem and cannot improve below the original
global minimum. This permits tied and positive-dimensional core optima
without imposing local curvature or uniqueness on the closure step.

At every level, the chart tests contribute `A_d(k) poly_d(I)` work.
There are only polynomially many levels, so this remains an additive
parameter factor in the final bound. The expected corner count pays for
ordinary exact recourse calls. One small-core completion and the expected
fallback complete the stated work bound.

The returned coordinate formulas select one canonical optimizer of a
single winning flow slice. Even a fallback that examined exponentially
many labels returns only that slice's small-core algebraic descriptions.
Their own polynomial degrees and heights do not depend on how many
other labels were compared. The all-draw output-size and refinement
claims therefore remain valid, distinct from the expected-size global
proof trace. Integer feasibility persists under core approximation
because balances and capacities do not depend on the core. The rational
quadratic-output specialization also follows from the predecessor's
stationary-face argument.

The all-noise interiority hypothesis is substantive. At a boundary optimum,
ambient stationarity can fail and a positive-probability noise set can
retain a box with no uniformly optimal flow. The linked two-arc example
correctly identifies this limit. No general boundary theorem, integer
label uniqueness, or efficient discovery of the premises is implicit in
this review.

## Verification record

I ran

```sh
python research-20261002/reviews/check_interior_core_flow_charts.py
```

The [independent exact-fraction diagnostic](check_interior_core_flow_charts.py)
uses a small three-node cyclic network with forward and reverse residual
arcs. It passed 205 computed charts, 104 whole-interval certificates,
1,768 exact competing-label interval checks, 683 identically zero reduced
costs, and 33 tied query optima. The all-zero fixture tests tight zero-cost
cycles and the arborescence choice directly. There are 17 feasible fixture
labels; enumerating them is only an independent diagnostic oracle, not
the proposed algorithm. The costs include genuinely core-dependent
quadratic arc coefficients and degree-four joint terms.

This diagnostic is separate from the author's large tied-flow fixture;
I did not rerun that fixture. A scoped inline Python check passed for the
review's five local links, code fences, whitespace, control characters, and
the diagnostic's syntax. No new external literature search, index
edit, project-wide verification, or CI inspection was performed.
