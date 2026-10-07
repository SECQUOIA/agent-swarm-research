# Independent audit of the two constant-accuracy point reductions

Date: 2026-10-03. Verdict: **pass, with the scope qualifications below**.
This audit reconstructs both reductions from the actual source notes.
It finds no blocking mathematical, encoding, or precision error. It does
not establish publication priority or an unconditional complexity-class
separation.

The audited claims are:

- [Square Root Sum point reduction](../../../research-20261002/new-direction/convex-point-radical-comparison.md),
  especially lines 29–213.
- [PosSLP point reduction](../../../research-20261002/new-direction/posslp-convex-point-extraction.md),
  especially lines 35–295.

## 1. Exact problem and output contract

Both reductions construct an explicitly listed rational polynomial of
degree at most four and an explicitly given rational box. The polynomial
is jointly convex **on that box**. Neither argument establishes global
convexity on the ambient Euclidean space.

The requested output is an explicitly readable point within absolute
Euclidean or maximum-norm distance `1/4` of a genuine optimizer. In both
constructions the optimizer is unique and a designated coordinate is
exactly zero or one. Thresholding that coordinate at `1/2` decides the
source predicate. The approximation need not be feasible for this
implication. No canonical selection, exact coordinate equality test,
algebraic-number comparison, or precision depending on the source
instance is hidden in the final query.

A compact unevaluated optimizer descriptor is a different output. The
input program already provides one. The reduction applies to such a
descriptor only when its promised evaluator supplies the point
approximation in polynomial work. Likewise, objective-gap approximation
does not satisfy the stated output contract.

The deterministic consequence is conditional: a polynomial-time routine
for the target task would put the respective source decision problem in
polynomial time. An always-correct routine with expected polynomial
work gives the corresponding Las Vegas consequence. Neither result is
an NP-hardness theorem.

## 2. Square Root Sum reduction

### Normalization, equality, and bit size

The normalization in lines 43–62 of the radical note is sound. Each
power of two `R_i` and each rational `c_i=a_i/R_i^2`, `w_i=R_i/M`, and
`b=B/(KM)` has polynomial binary length. The complete averaging tree has
`O(n)` nodes, with at most a factor-two padding overhead. Its zero
residual assignment has root `sum_i sqrt(a_i)/(KM)`.

The equality preprocessing in lines 153–172 is valid for the stated
positive-radical source problem. In the common multiquadratic extension,
every nonsquare radical has trace zero by transitivity through its
quadratic subfield. If their positive sum plus the integer radicals were
an integer, taking the trace would remove every nonsquare term. The
remaining equality would require the sum of strictly positive nonsquare
terms to be zero. The reduction therefore needs only integer square-root
tests; it does not factor the radicands or construct the extension.

This proof depends on positivity of the radical summands. It should not
be restated as an equality algorithm for arbitrary signed radical sums.

### Base curvature and the comparison amplitudes

The predecessor's
[averaging-tree estimate](../../../research-20261002/new-direction/convex-active-set-radical-comparison.md)
(lines 123–148) is valid: distinct rows of its child matrix `P` have
disjoint supports, giving `||P||_2 <= 1/sqrt(2) < 3/4`.
Leaf second derivatives are at least two, so
`H_F0 >= 2(I-P)^T(I-P) >= I/8`.

Appending each `t^2` and the signed root coupling of norm `1/32` leaves
the claimed conservative `I/16` lower bound. At `t=0`, the remaining
coordinates have their unique unperturbed optimum. The sign of the
one-sided `t` derivative therefore decides whether that face contains
the optimizer. The upper-face derivative is strictly positive. After
the equality preprocessing, exactly one base optimum has a positive
amplitude. These arguments cover padding nodes and leaf optima on a
box boundary.

### Amplification, uniqueness, and sparsity

The division-free identity in lines 109–130,

```
D²[t²(y-c)²][p,q]² = 2(tq+2(y-c)p)² - 6(y-c)²p²,
```

is exact. With `eta=1/192`, the losses for the two amplitude coordinates
consume at most `1/32` of their base curvature. The resulting quartic
is jointly convex, including at zero amplitudes.

Each base objective is at least its own minimum and the added squares
are nonnegative. The suitable endpoint of `y` makes both squares zero
at the independent base minima. Consequently every full optimizer must
attain both unique base minima and that same endpoint. This proves
uniqueness without estimating the possibly tiny positive amplitude.

The bags described in lines 190–196 give a valid decomposition of width
two: two independent averaging-tree decompositions are connected through
the path containing the root, amplitude, and endpoint bags. Every
variable's bag occurrences are connected, and every factor is covered.

The coefficient statement in lines 176–188 correctly removes the
aggregate constant after mapping the box to the unit box. Every
nonconstant monomial has bounded factor incidence. The claimed
coordinate curvature bounds `5` before and `20` after that change are
also valid. These are coordinate second-derivative bounds, not a claim
of an input-independent full point-growth modulus.

## 3. PosSLP reduction

### Bounded arithmetic gates

The rational-pair arithmetic in lines 37–93 preserves `u/v=a` with
positive exact `v`. Addition, subtraction, repeated inputs, and
multiplication are all covered. The optimization variables themselves
need not have positive denominators away from the exact circuit
assignment: the objective uses polynomial residuals and performs no
division by variables.

For integer source output `A`, the final gate
`t=(2u-v)/4=v(2A-1)/4` is never zero and has the sign of the PosSLP
predicate `A>0`. This handles the zero source output without an extra
oracle. Every exact gate value lies in `[-1/4,1/4]`. The stated bounds
on gate value, gradient one-norm, and Hessian operator norm are valid,
including when two source inputs coincide.

### Weighted convexity

The proof in lines 95–163 handles arbitrary circuit fanout. In
zero-based or one-based indexing, the normalized Jacobian entry is

```
E_ij = 8^(j-i) * partial_j p_i,  j<i.
```

Its absolute row sums are at most `1/8`, and its absolute column sums
are at most `sum_(k>=1) 8^-k=1/7`. Hence `||E||_2 < 1/4`, and the
positive Jacobian contribution is at least `(9/8)||Dh||²`.

For the nonlinear residual terms, `|r_i|<=1/2` and `||H_p_i||_2<=1`
give a loss at most `sum_i a_i ||h_<i||²`. The geometric weights bound
this sum by `(1/63)||Dh||²`. Thus

```
H_G >= (9/8 - 1/63)D² = (559/504)D² >= I.
```

The estimate controls mixed directions, not only coordinate curvatures.
The triangular residual equations have exactly one zero. At that point
the ambient gradient vanishes even when a constant gate lies on a box
boundary, so the stated quadratic growth of `G` follows.

### Size and bounded coefficients

The reduction never expands the exact rational circuit values. Each
gate residual has at most three monomials and its square at most six
monomial occurrences after local collection. There are `O(N)` gates,
and each weight `64^(N-i)` has `O(N)` bits. Collection across gates
preserves polynomial encoding length.

Scaling the **entire** final objective by `64^-N`, as specified in
lines 289–295, preserves its optimizers. Its gate weights become
`64^-i`, whose sum is bounded by an absolute constant. This geometric
sum bounds collected coefficients even with arbitrary fanout and
monomial collisions. The finitely many auxiliary terms also remain
bounded. The fixed affine map to the unit box preserves this property:
every factor has bounded degree and a bounded number of variables, so
each coefficient expands into a bounded number of bounded contributions
per factor. Unlike the unscaled radical construction, even the
aggregate constant is bounded here by the geometric weight sum.

This scaling also scales every curvature modulus. Bounded coefficient
magnitudes are not bounded denominator bit lengths, bounded height, or
a uniform conditioning guarantee. The actual coefficient encodings
remain polynomial in the circuit size.

### Endpoint forcing

The two sign-test bases in lines 165–204 have Hessians at least
`31I/32`. The same amplifier identity used above leaves at least
`15||p_base||²/32`, establishing convexity of the full objective. The
nonnegative-sum argument then fixes both base minimizers and the
endpoint coordinate. The complete optimizer is unique. Its Hessian is
positive definite at that point, as asserted in lines 257–262.

That last statement must not be enlarged to uniform strong convexity
on the whole box: when both auxiliary amplitudes are zero, the pure
`y` direction has zero Hessian curvature. The note makes no such
enlargement. Treewidth is unrestricted in this construction.

## 4. Consequences for the topic's result map

Both hardness results can be retained without mathematical repair.
Their complementary strengths should remain visible:

- Square Root Sum: width two, bounded coefficient magnitudes, bounded
  coordinate curvature, unit-box form, and a unique optimizer.
- PosSLP: a broader arithmetic source problem, unique optimizer,
  degree four, and bounded coefficient magnitudes after full scaling;
  no bounded-width or uniform conditioning promise.

Both concern convexity on the feasible box. They are compatible with a
polynomial point algorithm under **global** convexity or a supplied
effective point-growth bound. Appending the independent noisy scalar
core does not change the difficult endpoint on any draw, so both
core-only-noise consequences also pass. Nothing here rules out compact
exact descriptions without an efficient point evaluator.

## 5. Targeted checks actually run

An independent inline `python3 -B - <<'PY'` exact-arithmetic diagnostic
implemented sparse gate polynomials, derivatives, expansions, and LDL
tests without importing the earlier checker. It passed:

- Five circuit fixtures, covering positive, zero, and negative outputs,
  repeated operands, cancellation, and high fanout.
- Twenty-six exact rational-pair invariants and 271 local gate-vertex
  value, gradient, and Hessian bounds.
- Twenty exact positive-definiteness checks of the normalized full gate
  Hessian after subtracting `(559/504)I`.
- Five scaled coefficient and unit-box polynomial-expansion checks.
- A 12-gate repeated-squaring circuit with 25 coordinates, a 1,025-bit
  source output, and maximum unscaled weight length 145 bits.
- Both amplifier Hessian identities as exact polynomial identities.

The existing, non-writing source diagnostic was also run:

```sh
python3 -B research-20261002/new-direction/check_convex_point_radicals.py
```

It passed 11 exact source comparisons, seven decompositions with 190
bags, and 35 endpoint/tie checks including 1,000-bit amplitude scales.

The inline diagnostic was run from a heredoc and is recorded here by
its command form and results; it is not a persisted additional checker.
Finite arithmetic checks support the symbolic argument and do not
prove its general complexity claims. A scoped
`git diff --check -- research-20261003-arithmetic/reviews/point-core/hardness-audit.md`
and a separate inline Python check of this audit's three local links,
whitespace, and code fences passed. No project-wide verification or CI
status/log inspection was performed.
