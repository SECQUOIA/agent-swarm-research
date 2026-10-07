# Independent review of native-integer recourse

Date: 2026-10-02. Verdict: **pass** after the recorded interface
clarifications. This review read the actual
[native-integer theorem](../new-direction/smoothed-native-integer-recourse.md),
its [optional implicit variant](../new-direction/native-integer-recourse-implicit-closure.md),
the exact and approximate continuous-recourse predecessors, the linked
finite-law interfaces, and the applicable primary-source passage for
the TU oracle. It found no remaining mathematical blocker under the
stated exact-oracle and curvature premises. This is an internal proof
review, not an assessment of publication priority.

## 1. Fixed residual feasibility is essential

The domain is a product of the continuous core box and one fixed finite
integer feasible set. The core changes objective coefficients only.
Consequently each fixed-label objective has the supplied core-coordinate
upper curvature, and its lower envelope has the same upper curvature
after the independent linear core noise is removed. Conditional
optimization and coordinate-restricted conditional optimization use the
same feasible label sets at every core point.

Neither the hull certificate nor the near-optimal core count would follow
from an oracle whose feasible set changed with the core. The statement
correctly excludes core-dependent supplies, balances and right-hand sides.
The oracle must solve every tightened integer coordinate box exactly,
including infeasibility, with a polynomial exponent independent of the
core dimension. Unrestricted recourse alone would not suffice.

At rational core points the original polynomial and integer labels give
rational exact values with polynomial bit length. Fixed-degree evaluation
does not depend polynomially on the numerical size of a label. It depends
polynomially on its binary length. Feasibility of an original label is
also exactly checkable using the original rational residual inequalities.

## 2. Uniform exclusion of every competing label

For any integer point `z`, the union of the at most `2r` restrictions

```
z'_i<=z_i-1 or z'_i>=z_i+1
```

is exactly the feasible residual set minus `z`. Coupling between residual
coordinates does not change this identity. Infeasible restrictions are
omitted by assigning value infinity. This covers the singleton residual
case as well, including an empty residual coordinate set.

The bound `G` is uniform for all feasible labels, and also bounds the
value of the chosen label as the core moves. Every fixed-subset value
function is `G`-Lipschitz in core infinity distance. If the reference
corner `c` is in the retained hull `D`, every `v` in that hull is at
distance at most its maximum coordinate width `w`. Hence

```
V_other(v)-F_gamma(v,z)
  >= V_other(c)-V(c)-2G w.
```

Strict positivity proves that the same integer label is the unique
conditional winner throughout the entire hull. The incumbent reference
corner belongs to the hull: a cell containing that queried corner cannot
be discarded while it realizes the incumbent minimum. Nested dyadic
refinement preserves such a cell if the incumbent was queried earlier.

Both the strict inequality and the exact excluded value matter. A gap
equal to `2Gw` can leave a tie at the far endpoint. An arbitrary feasible
excluded upper value can conceal a better competing label and give a
false certificate. The note states both restrictions correctly; the
reviewer diagnostic below includes explicit examples.

## 3. Cutoff and exact whole-core completion

On the good growth event, the incumbent completion satisfies
`||w_j-a||²<=e_j/g_0`. Distinct native integer labels are at least one
unit apart, regardless of the number of labels or the constraints on
them. The cutoff `h<=1/(4A_0)`, with `A_0=2+kL/g_0`, therefore identifies
the optimal residual label and gives the stated `e_j<=g_0/8` bound.

Every point with a different label has objective at least `f*+g_0`,
even at the same core corner. Thus the excluded value gap is at least
`g_0-e_j>=7g_0/8`. The second cutoff inequality gives
`2G width(D)<=4GA_0 h<=g_0/4`, leaving strict slack in the uniform
label certificate. No supplied discrete separation premise is hidden
in this argument.

After this certificate, the feasible slice `[0,1]^k times {z}` contains
an original global optimizer and is a subset of the original domain.
Its exact minimum is therefore the original global minimum. Solving
the entire slice is valid without convexity, uniqueness, a positive
Hessian, or strict core-bound gradients. It remains valid when the
slice has a continuum of optimizers; canonical lexicographic selection
chooses one of them. This is the simpler primary proof in the final
saved main note. Its cutoff and exceptional probability use only the
growth event.

The small-core algebraic format has two blocks of at most `k` variables,
one free scalar, `O(k^2)` atoms, and fixed degree. All original residual
constraints disappear from this core formula after a feasible label
is fixed. Combining like terms leaves at most `binom(k+d,d)` monomials
with coefficient height polynomial in `I+log M`. This format control,
rather than a generic `I^{O(k)}` fixed-dimensional algorithm, is what
justifies the FPT conclusion.

The reviewed Renegar bit bound gives a structural factor
`(k+1)^{O_d(k^2)}` and a coefficient-height exponent independent of `k`.
Univariate products, squarefree extraction, root isolation and refinement
have absolute polynomial degree/height exponents. They can all be
absorbed into the same parameter-only factor. The scalar formulas
describe coordinates and value of the same canonical optimizer; their
selected roots are consequently consistent. A separate focused bit
review independently confirmed this argument, including tied and
positive-dimensional optimizer sets.

Construction is invoked once after a successful label certificate.
Its parameter-only cost is therefore additive to the expected sparse
core-search work, as in the final bound. During exceptional label
enumeration, pairwise comparisons need not rewrite the winning
coordinate representations in a compositum. The fallback returns the
winning label's small-core representations. Re-isolation with respect
to each coordinate's own polynomial establishes the stated output
length and refinement bound on every draw, independently of the number
of tested labels. Raw full-domain elimination polynomials would not
justify this last bound; the actual fallback uses label enumeration.

Expanded output here means integer univariate polynomials with rational
isolating intervals. It does not mean minimal polynomials or one common
primitive element. A degree-three optimizer and its exact value are
included in the finite diagnostic below.

## 4. Optional sharper implicit closure

In the separate implicit variant, original core-bound gradient signs are
tested on a box containing every original optimizer's core. Their
uniform error bounds justify each fixing. The gradient cutoff has
ample slack, and a coordinate free at an optimum cannot pass a strict
whole-box sign test because its derivative vanishes there. The remaining
free-face Hessian at the optimizer is at least `2g_0 I`. Its variation
to and over the tested box is at most `2T A_0 h<=g_0/2`, so the rational
positive-definite test succeeds. Conversely, any accepted sign and
Hessian certificates are sound without assuming the good event occurred.

With zero core dimension the exact integer oracle already solves the
whole problem, including ties. If the supplied upper core-coordinate
curvature is nonpositive, endpoint interpolation provides an exact
`2^k`-query alternative. No small-curvature division is needed in that
branch. The optional variant returns a compact exact implicit continuous
patch with polynomial evaluation work. Its exact convex-QP branch and
the primary theorem's rational core-face enumeration justify exact
rational outputs for quadratic objectives.

## 5. Large native widths and one finite noise law

The integer disjunction for a coordinate has one atom per native label,
but its count has only polynomial logarithmic length. Adding the
residual inequalities keeps the formula at two quantified point blocks,
one free noise scalar, and fixed degree. The reviewed fixed-block
elimination bound therefore gives scalar-section complexity
`2^{poly_d(I)}`, not a double exponential in the binary interval length.
The main algorithm computes the bound in binary and does not construct
this expanded formula during ordinary core search.

For the optional variant's active core gradients, the proof must fix candidate labels and faces
for a union bound. It must not condition on the random winning label.
The revised note makes this distinction explicit. After fixing a
candidate label and face, conditioning on every coefficient except one
active core coefficient leaves its uniform scalar law unchanged.
Positive full point growth makes the relevant free stationary system
nonsingular. Isolated-root counting remains valid even if other roots
or components are singular or positive dimensional. The stated `R_Z`
and `3^k` factors safely cover all candidates, including infeasible
labels counted unnecessarily.

The exceptional algorithm may enumerate all native labels and solve
the remaining polynomial core problems. Label substitution creates
only polynomial-length coefficients. Algebraic degrees, candidate
counts and comparisons have a base-only singly exponential bound;
sampled coefficient bits and requested accuracy enter a polynomial
factor with fixed exponent. The alternative canonical two-block
fallback gives the same interface. The quadratic face-enumeration
route is an explicit rational special case.

`G`, `M_1`, `T`, `S`, `K`, `B` and the section bound are all chosen
from base data whenever used. Their magnitudes can be large, but their logarithms
are polynomial in the original input. This makes `J` polynomial before
`M` is chosen. The primary theorem has only the growth failure event,
of probability at most `rho`; its same-draw fallback costs `rho B` in
expectation apart from polynomial factors. The optional variant adds
the active-gradient event and uses the valid larger allowance `2rho B`.
No resampling or sampled-height
precision circle occurs. A separate focused bit review and its
independent cross-check reached the same conclusion.

The primary evaluator fixes the stored integer vector exactly, refines
the algebraic core coordinates, and clips them to the core box. A
polynomial-bit gradient bound and the separate exact-value enclosure
give feasible rational approximations with certified objective gaps.
The optional variant instead uses the already reviewed convex-patch
evaluator. Both preserve residual feasibility because it is independent
of the core. Output bounds and the expected proof-record bound are
correctly distinguished.

## 6. Concrete TU and network-flow oracle

I read the local primary extraction around Hochbaum--Shanthikumar
Algorithm 4.2 and Theorem 4.3, printed page 858, and the
[focused source audit](../prior-art/integer-convex-flow-recourse-prior.md).
The source requires an optimal extreme-point LP solution, not an
arbitrary point on the LP's optimal face. The note records that
requirement. The scaling construction has logarithmic dependence on
the right-hand-side magnitude and polynomially many prescribed-grid
function evaluations for totally unimodular systems.

For the fixed-degree rational query costs, those grid evaluations and
the resulting LP coefficients have polynomial bit length. A rational
polynomial-time LP algorithm can select an optimal extreme point.
Integral right-hand sides and TU constraints then give the needed
integer point. Tightened coordinate bounds preserve this structure.
Feasibility can be checked by the corresponding rational LP.

The source may evaluate outside an original native interval. The final
note supplies the needed bridge: extend each cost by its tangent line
at either endpoint. This produces a globally convex function agreeing
with the original cost at every feasible label, with polynomial-bit
rational evaluations after core fixing. Uniform conditional convexity
remains a valid supplied premise or requires its own checkable
certificate. The extension changes neither outer core curvature nor
original feasible objective values.

The network marginal-potential certificate also checks independently.
For any alternative integer flow, its signed difference from the
candidate is a nonnegative integral residual circulation, using one
direction for each changed original arc. Discrete convexity bounds the
actual cost increase below by the sum of the current unit marginals
on that circulation. Nonnegative reduced arc costs sum to a
nonnegative number because potentials cancel. Conversely, a negative
simple residual cycle permits an improving feasible unit augmentation.
An optimal flow therefore has no negative cycle, and shortest-path
potentials from a zero-cost source certify this fact. Their rational
length is polynomial in the marginal-cost encoding. This is a compact
optimality certificate, not a polynomial-time claim for repeated unit
augmentation.

## 7. Distinct targeted checks

The command actually run was

```text
python research-20261002/reviews/check_native_integer_recourse_review.py
```

The [checker](check_native_integer_recourse_review.py) and
[saved report](native-integer-recourse-review-results.json) use a small
coupled three-coordinate integer feasible set and a nonlinear core.
They passed 1,215 gap tests, 2,430 coordinate-restricted exact
enumerations, and 5,040 endpoint comparisons for 420 accepted uniform
labels. Here label cost differences are affine in the core, so these
endpoint checks certify every point of each tested interval, not only
a finite sample. The checker verifies the exact union of the excluded
coordinate restrictions, a strict-threshold tie guard, and a false
certificate obtained by substituting an excluded feasible upper value.

Three separate symbolic budget fixtures use native widths with 1, 23
and 200 bits. The primary growth-only cutoff and sampling depths are
52, 293 and 2,240. The optional implicit cutoffs are 55, 293 and 2,240.
They verify the respective gap and probability allocations, together
with the implicit variant's derivative and Hessian bounds.
No large label range is enumerated in those fixtures. These tests do
not implement the Hochbaum--Shanthikumar algorithm or verify an
asymptotic bound experimentally. The author's full core-refinement and
large-capacity flow diagnostic was not rerun here.

The updated checker also verifies expanded algebraic point/value
enclosures at 8, 32 and 96 bits for
`F(v,z)=v^4-v+(z-1)^2`. Label `z=1` has a certified unit gap;
the exact core optimizer is the unique positive root of `4v^3-1`,
and its value is the unique real root of `256f^3+27`.
Rational approximants satisfy the corresponding feasible objective-gap
bounds. This is a finite exact algebraic fixture, not a general
quantifier-elimination implementation.

Targeted document checks cover local links, whitespace, paired fences,
Python syntax and the saved JSON. No index edit, project-wide test, CI
inspection or new external literature search was performed.
