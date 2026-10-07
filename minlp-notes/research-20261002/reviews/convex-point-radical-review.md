# Independent review of the convex point-output reduction

Date: 2026-10-02. Verdict: **pass**. This review read the complete
[quartic point-output construction](../new-direction/convex-point-radical-comparison.md)
and its [strongly convex cubic predecessor](../new-direction/convex-active-set-radical-comparison.md).
The reduction applies to distance from an optimizer, including an
arbitrary optimizer returned by an algorithm. It does not establish
NP-hardness, an objective-gap obstruction, or a uniform-growth
obstruction. A separate agent independently checked the amplifier and
then the actual completed text. No mathematical blocker remains.

## 1. Both comparison copies have the required signs

Changing the sign of the root-to-`t` bilinear term changes neither its
Hessian norm nor the source lower bound. Each copy has Hessian at least
`I/16` and therefore a unique optimizer on its box. At `t=0`, that
optimizer can only be the unique unperturbed tree optimizer. The two
one-sided `t` derivatives there are opposite, namely
`epsilon*(b-s^0)` and `epsilon*(s^0-b)`.

The box KKT conditions therefore give the two equivalences in (4).
A negative derivative excludes every optimum on the zero face; a
nonnegative derivative at the unperturbed face optimizer certifies the
global minimum there by convexity. At `t=1` both derivative formulas
are at least `2-2epsilon>0`, since both the root and target lie in
`[0,2]`. Thus the reversed copy has no hidden upper-bound exception.
For a strict radical comparison exactly one copy has positive optimal
`t`, and the other has optimal `t=0`.

## 2. Convexity holds jointly, including at zero amplitudes

For either amplifier term the exact directional identity is

```
D²[t²(y-c)²][p,q]² = 2(tq+2(y-c)p)² - 6(y-c)²p².
```

It contains no division by `t`. On `y in [0,1]`, the losses in the two
terms are bounded by `6eta*p_+²` and `6eta*p_-²`. These affect different
base coordinates. The base lower bound `I/16` and `eta=1/192` leave
at least `||p_base||²/32`, with the two remaining squares nonnegative.
This proves joint convexity on the full box, not just along separate
coordinates or near the optimum. It also covers `t_+=t_-=0`, where
the pure `y` direction has zero curvature.

The additional terms are nonnegative. At the independent base
optimizers they both vanish for `y=1` in the positive-comparison case
and for `y=0` in the negative-comparison case. Hence the global optimal
value is exactly the sum of the two base optimal values. Any optimizer
must attain each base minimum and must make both added terms zero.
Strong convexity fixes all base coordinates, and the nonzero amplitude
then fixes `y`. This establishes the claimed unique optimizer and the
endpoint for every optimizer without solving the perturbed stationarity
equations.

## 3. Equality and point accuracy are handled exactly

The trace proof works even when the nonsquare radicals are algebraically
dependent. Each nonsquare `sqrt(a_i)` has zero trace to `Q` by trace
transitivity through its quadratic subfield. The integer terms have
trace equal to the field degree times their value. An integer sum of
positive radicals would therefore leave a zero sum of positive
nonsquare terms after removing the square terms. This is impossible.

Only integer square-root tests and addition are needed for preprocessing;
the exponentially large field is used for proof, not constructed by the
reduction. Positivity of the radicands and the integer target are
essential to this argument. The statement does not concern arbitrary
signed radical sums.

Absolute Euclidean or maximum-norm error at most `1/4` controls the `y`
coordinate by `1/4`. Thresholding the returned coordinate at `1/2`
therefore decides the strict source comparison. This uses unnormalized
coordinate distance. Neither feasibility of the reported point nor a
canonical optimizer selection is needed. The all-square and other
trivial source cases are decided before the optimization query.

## 4. Encoding, width, and the conditioning limitation

The two averaging trees have linear size. Their normalizations and the
target coefficient have polynomial binary length. All factors have
bounded scope and degree at most four. The two new pair bags
`{t_+,y}` and `{t_-,y}` can join the two source decompositions while
preserving connected occurrences of each variable. Maximum bag size
remains three, so treewidth is at most two.

The displayed coordinate-curvature upper bound `L=5` is valid: a real
leaf contributes at most four from its cubic and at most one half from
its parent residual; internal tree variables contribute at most two
plus one half; the new `t` diagonal is at most `2+2eta`; and the `y`
diagonal is at most `4eta`. The bilinear source terms add no diagonal
curvature. Scaling intervals of width at most two to the unit box
multiplies each coordinate diagonal by at most four, giving `L=20`.

The completed draft correctly removes the aggregate constant after
unit-box substitution. Without that step, bounded individual factor
constants could sum to an unbounded global constant coefficient.
Every nonconstant monomial has bounded factor incidence here, so its
expanded coefficient remains bounded by an absolute constant.

The source's uniform growth bound does not survive the amplifier.
Holding the base optimizers fixed and moving only `y` inward gives

```
F-F* = eta*t_active²*|y-y*|².
```

Consequently any full point-growth modulus is at most
`eta*t_active²`. The note makes no input-polynomial bound on its inverse.
The conditional complexity implication is therefore consistent with
algorithms parameterized by growth and with polynomial objective-value
approximation for convex functions.

The independent one-dimensional noisy core in section 5 changes none
of these facts. It has projected growth one and retains the same
residual problem on every draw. Expected running time of an
always-correct point evaluator would give a Las Vegas Square Root Sum
algorithm; it does not imply deterministic polynomial running time.
The original convex program remains a compact exact description, so
the stated limitation concerns an efficient coordinate evaluator.

## 5. Targeted verification

The separate reviewer checker
[check_convex_point_radical_review.py](check_convex_point_radical_review.py)
uses exact `Fraction` arithmetic. Its
[saved results](convex-point-radical-review-results.json) report:

- 80 amplifier Hessians with the proved `1/16` base lower bound;
- all 560 principal minors nonnegative and 2,160 directional identity
  and lower-bound checks;
- five singular zero-amplitude cases, including the null `y` direction;
- an indefinite raw quartic Hessian showing why the base bound matters;
- endpoint/value-scale fixtures at amplitudes `2^-1`, `2^-20`, and
  `2^-200`, and the constant coordinate-threshold test.

These are arithmetic diagnostics for the amplifier. The tiny amplitudes
are test inputs to its formula, not numerically computed minimizers of
particular Square Root Sum instances. The symbolic proofs above cover
all parameters. This checker does not implement a radical solver,
global optimization, or a complexity experiment.

Commands actually run:

```
python research-20261002/reviews/check_convex_point_radical_review.py
```

The review, checker, and result file also passed targeted local-link,
fence, trailing-whitespace, Python-syntax and JSON checks, and scoped
`git diff --check`. No project-wide tests or CI checks were run. The
author's distinct tree/endpoint diagnostic was inspected by report;
it is not claimed as independently rerun here.
