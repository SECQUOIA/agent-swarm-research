# Adversarial review of core-only smoothing on arbitrary flow-core faces

Date: 2026-10-02. Result: passed. The complete actual
[boundary-flow theorem](../new-direction/smoothed-boundary-core-flow.md)
was read independently. Its geometric, probabilistic and algorithmic
composition passes after the original-arc chart clarification. A separate
fresh [quantitative margin and arithmetic review](boundary-core-flow-bit-adversary.md)
also passed. This is not a priority assessment.

The [deterministic certificate review](flow-optimal-face-adversary.md)
checks optimal-flow intervals, convex inward-derivative flow minimization,
conformal proximity, and the Taylor fixing inequality. It includes a
distinct exact rational diagnostic. The present review concerns why the
certificate terminates under one finite core-noise law, without residual
noise or core-interiority assumptions.

## 1. The chart universe covers the actual tests

The final family contains every structurally valid augmented residual
arborescence for every feasible native flow, whether or not the tree is
ever shortest. A tree selected at a query point is therefore included.
Its symbolic potential is a sum of at most `s` marginal polynomials.
Native labels have base-bounded binary length. Thus chart degree and
coefficient height are bounded before the draw, despite adaptive selection
of the particular flow, tree and query point.

For every original arc the family includes every native adjacent-label
marginal. It consequently contains all within-interval unit differences
and first outside differences tested by the certificate, with a possible
sign reversal for the lower outside difference. The counts in (4) are
valid overcounts; their logarithms are polynomial in the base input.

The corrected no-normal case tests interval identities and original-arc
outside marginals at threshold zero. It does not inherit sign tests for
the artificial source arcs. Such tests are unnecessary for flow optimality
and were not included in the stated zero-set family. This correction is
substantive for the termination interface: all remaining tested polynomials
are now covered by the chart universe. The source arcs still legitimately
construct potentials at the center.

On each original face, nonidentity chart zeros form a compact set of
relative dimension at most `q-1`. The cross-label gradient image must range
over every feasible flow, rather than only the flow defining that chart;
the theorem does so. Polynomial maps preserve the dimension bound. The
fixed-block elimination enclosure and union count therefore give the stated
base-only degree bound, without constructing the image polynomials online.

## 2. Tube and normal-margin events do not select a random label

At a global core optimum in the relative interior of its true face,
every attaining flow makes its own smooth fixed-flow slice globally minimal
there. Each free gradient is consequently `-gamma_A`, regardless of
nonsmoothness or ties in the lower envelope. The uniform Hessian bound
implies (7) by moving that same flow's gradient to the nearest chart-zero
point. The finite-grid tube bound may be applied separately to every
fixed face's free-noise marginal, then union-bounded over faces. Conditioning
on the optimizer-selected face is neither necessary nor used.

For normal derivatives, the analysis-only lexicographically least restricted
core minimizer is a measurable semialgebraic choice depending only on the
free noises. All normal noise terms are constants on that face. Its entire
attaining flow set is therefore also independent of each normal coefficient.
Conditional on the other coefficients, the minimum inward derivative has
the form `b+s_i gamma_i`. The finite-grid interval bound in (9) applies
directly; no union over native labels is hidden in it.

Positive projected point growth makes the global core unique. On its true
face, any other restricted core minimizer would be another global core
minimizer, so the selected restricted point is exactly the true optimum.
Each attaining flow has nonnegative inward derivative by first-order
optimality. Outside the closed interval event `[0,tau]`, their minimum is
strictly larger than `tau`. This covers vertex faces as well as faces of
positive dimension and includes finite atoms with zero derivatives.

## 3. Distance is converted into a positive marginal value

The proof correctly distinguishes distance from a polynomial zero set
from a numerical lower bound on its value. For nonzero `p`, the set
`K_delta` is compact and excludes all zeros when nonempty, so its minimum
absolute value `m` is positive. Formula (10) has truth set precisely
`(m^2,infinity)`: an attaining point witnesses every larger scalar, and
no point witnesses a scalar at or below the minimum. An empty zero set
makes the distance constraint vacuous; an empty `K_delta` makes the claim
irrelevant. Constant polynomials and zero-dimensional faces are handled
directly.

Consequently an eliminated nonconstant scalar atom must vanish at `m^2`.
Clearing denominators and removing powers of the scalar before applying
the reciprocal Cauchy bound is valid. The fixed-dimensional coefficient
height factor belongs in the precision bound. The theorem explicitly
retains it as `f_d(k) poly_d(I)` and does not claim polynomial sampling
length with a dimension-independent constant.

The bound is uniform over every face chart because their degrees and
coefficient heights have one base-only bound. No selected tree, root height
or sampled core coordinate enters the definition of `mu_0`.

## 4. Every certificate test passes by the stated cutoff

On the complementary event, the true core `a` is unique and its projected
growth is at least `g_0`. The retained hull bound with
`A_0=2+kL/g_0` is conservative: the retained-corner gap is at most
`kLh^2/4`, and adding a cell width gives a smaller bound than `A_0 h`.
Projecting to the true face preserves the coordinatewise bound. The
midpoint and every projected point are within `k A_0 h` of `a`.

At the cutoff, the projected hull stays at distance at least `delta/2`
from every nonidentity chart zero. Every within-interval marginal that
vanishes at its center must therefore be a polynomial identity on the
original face. Every first outside marginal is strictly positive at the
center by the definition of the maximal minimizing interval. It stays
positive on the connected projected hull, and its absolute-value bound
is at least `mu_0`. Thus the optimal interval-flow set is identical at
the center, at `a`, and throughout the hull.

Taking minima over this common flow set preserves the uniform gradient
Lipschitz bound, so `beta_i(c)>tau-H k A_0 h`. The certificate's geometric
bounds `R<=2k A_0 h`, `T_infty<=A_0 h`, and `T_1<=k A_0 h` then imply

```
beta-HR-(H/2)T_infty
  > tau-H A_0 h(3k+1/2) > tau/2,
r K T_1 <= mu_0/4.
```

The three cutoffs in (14) therefore suffice. Interior faces need no
normal test. Vertex faces use constant chart values and direct rational
margins. This proves termination without a quantitative distance of the
optimizer from the original core boundary.

## 5. One-law and total parameter accounting

The displayed choices give growth failure at most `rho`, tube failure at
most `rho/2`, and normal-margin failure at most `rho/2`. Their union is
at most `2rho=1/(4B)`. The fallback's exponential base factor is selected
before sampling and cancels in the expected cost. Its remaining polynomial
dependence on `I+log M` is material and is absorbed into `f_d(k) poly_d(I)`,
not incorrectly discarded as polynomial in `I` alone.

The expected corner count applies through every searched level because
`M>=2^J`. The number of levels, sampling bits, query heights, `3^k` face
attempts, and constant-base sign-test costs all enter the same parameter
function. Every polynomial arithmetic exponent is independent of `k`.
One selected native flow and one common-root core representation are
returned; the output does not retain a field containing all labels tested
by the fallback. Its refinement bound follows from that representation
and the enlarged input-height budget.

The result is confined to the stated fixed feasible network-flow set,
separable convex arc costs, and core-only cost dependence. The proof does
not extend these conclusions to arbitrary integer recourse or changing
flow balances.

## Verification scope

The deterministic subargument has the independently executed rational
diagnostic linked above. No probability simulation or duplicate full-core
search test was used for this composition review. The final theorem was
reread after the original-arc/tree-family and measurable-selection
clarifications. The separate arithmetic reviewer independently checked the
actual completed theorem and its margin lemma, including the larger sampling
precision and output costs. The author's later two-arc end-to-end diagnostic
was not rerun by this reviewer. Topic-scoped link, syntax, whitespace and
delimiter checks passed. No external search, project-wide verification or
CI inspection was performed.
