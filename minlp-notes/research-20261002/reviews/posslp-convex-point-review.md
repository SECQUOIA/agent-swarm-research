# Independent review of the PosSLP convex point reduction

Date: 2026-10-02. Verdict: **pass**. This review read the actual
[quartic reduction](../new-direction/posslp-convex-point-extraction.md),
including the bounded circuit encoding and the weighted gate objective.
It also checked the new composition with the already
[reviewed paired amplifier](convex-point-radical-review.md).
A separate mathematical agent independently checked the gate,
Hessian, and encoding arguments. No substantive gap was found.

The conclusion is a conditional complexity implication for constant
distance to an optimizer. It is not an NP-hardness claim, a complexity
class separation, or an obstruction to objective-value approximation.
The construction makes no bounded-treewidth claim.

## 1. Bounded gate encoding and the zero source output

For addition and subtraction, the ratio of the new numerator to the new
denominator is exactly `u_1/v_1 +/- u_2/v_2`. For multiplication it is
their product. The constant pairs encode zero and one exactly, and each
new exact denominator is the product of two positive earlier
denominators divided by four. Positivity therefore propagates without
an algorithm testing a large circuit value.

The numerator bounds hold on the entire optimization box: at most
`1/32` for a sum or difference of two normalized products and at most
`1/64` for a single product. The constant gates and the final affine
gate also remain in `[-1/4,1/4]`. Thus the unique triangular gate
assignment is feasible.

Denominator variables are allowed to be negative away from this exact
assignment. This causes no problem. The reduction contains polynomial
gate residuals, not division by denominator variables. Positivity is
used only to interpret the unique zero-residual assignment. All
derivative and Hessian estimates are uniform on the full box.

The final gate is

```
t = (2u-v)/4 = v(2A-1)/4.
```

Since `A` is an integer and `v>0`, this output is never zero. It is
positive exactly when `A>0`, including the correct negative sign when
`A=0`. No equality preprocessing or source sign query is hidden in
the reduction.

Both coordinates of a new source gate depend only on earlier source
pairs. Either order within the new pair is therefore topological.
The argument allows mixed parent order, repeated inputs, and arbitrary
fanout. Repeated inputs merely collect at most two quadratic monomials;
the value and derivative bounds still hold by the triangle inequality.
For example, repeating a parent in addition gives `uv/2`, and repeating
it in multiplication gives `u²/4`. Their derivative and Hessian bounds
are well inside the stated bounds of one. Constants and the final
affine gate satisfy the same uniform bounds.

## 2. The weighted convexity proof covers arbitrary fanout

Use `a_i=64^(N-i)` and `D_ii=sqrt(a_i)`. The normalized Jacobian has

```
E_ij = 8^(j-i) * partial_j p_i,  j<i.
```

Every row has absolute sum at most `1/8`, because its derivative row
sum is at most one. For a fixed column, each later topological index
occurs only once, even if the source variable has large fanout. The
absolute column sum is consequently bounded by
`sum_(k>=1) 8^-k=1/7`. Thus
`||E||_2<=sqrt(||E||_1 ||E||_infinity)<=1/sqrt(56)<1/4`.
The positive Jacobian contribution satisfies

```
2 ||D(I-L)h||² = 2 ||(I-E)Dh||² >= (9/8)||Dh||².
```

For the nonlinear residual contribution, `|r_i|<=1/2`, the gate
Hessian norm is at most one, and the gate depends only on earlier
coordinates. Therefore its total lower bound is

```
-sum_i a_i ||h_<i||²
  = -sum_j h_j² sum_(i>j) a_i
  >= -(1/63) sum_j a_j h_j².
```

This is a bound on the full quadratic form, including mixed directions;
it is not a diagonal-only Hessian test. Combining the two terms gives

```
H_G >= (559/504)D² >= I.
```

Triangularity gives exactly one zero-residual assignment. At that point
the ambient gradient of the sum of squared residuals vanishes, even
when a constant gate attains a box endpoint. The lower bound on the
Hessian therefore gives the claimed point-growth bound for `G` without
an interiority assumption.

## 3. Polynomial encoding does not expand gate values

Each residual contains at most three monomials, so its square contains
at most six after like terms within the square are collected. The
expanded objective has `O(N)` monomial occurrences before collection
across gates. Each weight has `O(N)` bits, and collecting coefficients
preserves polynomial bit length. The topological order, local gate
formulas, and geometric weight identities form a polynomial-size,
directly checkable convexity proof.

The exact rational gate assignment can require extremely many bits.
It is never expanded as part of the reduction. Only fixed small gate
coefficients and geometric weights of polynomial bit length are
written. This distinction is essential to the transformation's running
time.

Multiplication of the complete objective by `64^-N` is also sound.
The normalized gate weights sum to less than `1/63` in each copy.
Every squared gate has bounded coefficients, so even arbitrarily many
collisions of an expanded monomial have bounded total coefficient
magnitude after scaling. The finitely many extra amplifier coefficients
are bounded as well. Mapping the fixed box to a unit box preserves
degree and polynomial encoding length. The scaling changes curvature
moduli, as the main note explicitly states.

## 4. The quartic suffix preserves the sign and fixes every optimizer

The two functions `G+a² +/- epsilon*a*t` have Hessian at least
`(1-epsilon)I`, since the added bilinear term has operator norm
`epsilon=1/32`. On the face `a=0`, each has the unique minimizer `x*`.
Its new one-sided derivative is `-epsilon*t*` or `+epsilon*t*`.
Convex KKT conditions therefore activate exactly one auxiliary
coordinate. At `a=1` either derivative is at least
`2-epsilon/4>0`, excluding a hidden upper-bound case.

The paired amplifier is nonnegative. Its division-free Hessian identity
subtracts at most `6eta` from each distinct auxiliary direction, leaving
`1/2-6eta=15/32` from the conservative base lower bound. Thus the full
quartic is jointly convex, including points where both amplitudes
vanish.

At the independent base minima exactly one amplitude is positive.
Choosing the corresponding endpoint of `y` makes both added squares
zero. Every global optimizer must attain both unique base minima and
make those squares zero, forcing `y=1` when `A>0` and `y=0` otherwise.
The complete optimizer is therefore unique. Its Hessian is positive
definite: a nonzero base direction has the strict lower bound above,
and a pure `y` direction has positive curvature from the nonzero
amplitude. No uniform quantitative bound on this final curvature is
implied.

Maximum-norm or Euclidean point error at most `1/4` determines which
side of `1/2` contains `y`. The reduction needs no canonical selection,
algebraic value output, or feasible reported point for this implication.
It also needs no tiny-parameter estimate to construct the instance.
The output coordinate itself is exactly zero or one; its correct
selection is the issue.

The final saved sections 5–6 also pass. The independent scalar noisy
core has optimizer `1/2-gamma/2`, curvature two, and projected growth
one for every allowed draw. Its separable addition leaves the residual
optimizer and its endpoint unchanged. Thus the stated implication for
an efficiently sampled finite rational core-noise law is valid. An
always-correct expected polynomial-time point routine gives a Las Vegas
PosSLP algorithm, not a deterministic running-time conclusion. A compact
descriptor with a polynomial-time full-point Cauchy evaluator has the
same implication at the fixed requested precision.

## 5. Targeted diagnostics

The exact checker
[check_posslp_gate_review.py](check_posslp_gate_review.py)
targets the new gate convexification, not the previously tested
amplifier. Its [saved results](posslp-gate-review-results.json) record:

- four source circuits with outputs `-3`, `0`, `1`, and `-1`;
- 41 exact normalized pairs with positive denominators and correct
  ratios, including repeated-input and mixed-parent operations;
- 447 local gate-box vertex checks for values, derivative row sums,
  and Hessian norm bounds;
- 688 gate jets in full weighted Hessian calculations;
- 32 exact rational positive-definiteness checks of
  `D^-1 H_G D^-1-(559/504)I`, using an exact LDL factorization.

The global fixtures include box endpoints, a zero point, alternating
signs, exact gate assignments, rational interior points, and repeated
fanout from old source coordinates. The checks provide arithmetic
confidence in the formulas. They do not replace the uniform estimates
above and do not run a convex optimizer or a PosSLP algorithm.

Command actually run:

```
python research-20261002/reviews/check_posslp_gate_review.py
```

The three new review files also passed scoped local-link, fence,
whitespace, Python-syntax and JSON checks, and `git diff --check`.
No index, project-wide test, or CI check was used.
