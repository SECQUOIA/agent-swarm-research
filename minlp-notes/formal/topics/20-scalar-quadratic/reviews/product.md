# Independent product review

Reviewed `Product.lean`, `ProductLower.lean`, and `ProductExact.lean` against
P1–P2 and the exact convex-minimum part of P3. Also inspected the relevant
`Model`, `LowerPullback`, `IntervalLower`, `BinaryModel`, and `SquareLift`
interfaces and the product section of
`results/quadratic-inertia-one-sided-integer-complexity.md`.

Result: the reviewed claims pass. No proof changes were needed.

## Domain and lower bounds

`productDomain` is the original two-dimensional unit square and
`productFunction x = x 0 * x 1`. The epigraph lower theorem pulls an actual
lift back along `t ↦ (t,1-t)` on the entire unit interval. The hypograph
lower theorem uses `t ↦ (t,t)`, giving the square directly; this is the
reflected version of the epigraph slice. The pullback preserves the exact
integer dimension `p` and allows every finite number of continuous
coordinates. It imposes no boundedness or closedness requirement on the
original carrier or integer witnesses. The finite parity-grid argument in
`IntervalLower` proves the bound even at equality, without a diameter
attainment assumption.

## Construction and accuracy

`productUpperCarrier` is an affine preimage of the square lift intersected
with the original input domain and one convex quadratic inequality. Its
output constraint is the elimination of the exact positive-square
epigraph variable in the source construction. It implements
`xy = ((x+y)/2)^2 - ((x-y+1)/2)^2 + (x-y+1)/2 - 1/4`.

Containment quantifies over every `w ≥ xy`, not just graph points. The
hypograph transformation similarly contains every `w ≤ xy`; neither
construction caps the unbounded output direction. The square auxiliary
output and witnesses are continuous coordinates. The integer code is
copied unchanged. The square binary-to-integer bridge proves equality of
the projected relaxations, using the actual binary bounds.

`productExactEpigraphLift_attains` supplies a feasible original point
`(squareWidth p/2, 1-squareWidth p/2)` and output exactly the product minus
`squareWidth p^2/4`. Both coordinates lie in the unit square. The reflection
used for the hypograph is an affine involution that preserves accuracy and
integer dimension.

## Thresholds and minima

The two `product_*_lift_iff` theorems hold for every real error parameter:
feasibility with exactly `p` unrestricted integers is equivalent to
`(1/4)^p/4 ≤ ε`. Thus the positive threshold is attained, zero or negative
errors are impossible with finite `p`, and `p=0` is feasible precisely when
`ε ≥ 1/4`. For positive `ε`, `squarePrecisionCount` uses the natural
ceiling, so it implements the maximum with zero for coarse tolerances.
`product_one_sided_minimum` proves feasibility at that count and the lower
bound for every competing count.

This review does not verify P3's separate finite-linear-lift construction
with arbitrarily small positive extra slack. In particular, the exact
product convex construction must not be labeled a finite LP.

## Targeted checks

From `formal`:

- `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake build --wfail Formal.QuadraticPrecision.ProductExact` — passed.
- `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake env lean /tmp/topic20-product-review.lean` — passed. The temporary review examples instantiated both `p=0` threshold equivalences, finite-`p` impossibility at zero error, and the attained point `(1/2,1/2,0)` for the zero-integer epigraph construction.

The same temporary check printed the axioms of both lift equivalences,
`product_one_sided_minimum`, and `productExactEpigraphLift_attains`. Each
used only `propext`, `Classical.choice`, and `Quot.sound`. These targeted
checks are not a project-wide build or a CI result.

## Follow-up: finite linear lifts with positive slack (P3)

Independently reviewed `ProductLinear.lean`, including its uses of
`UpperAssembly`, `FoldingLift`, and `LinearSystem`. This closes the P3
linear-construction limitation of the initial review above.

`product_epigraph_binary_two_depths p L` combines the positive square's
zero-binary folding LP at depth `L` with the negative square's `p`-binary
hypograph LP. `UpperAssembly` constructs an actual finite family of affine
rows, rather than assuming that a convex set has a linear description.
The code index has cardinality `0+p=p`; component outputs and folding
variables are continuous. Original unit-square constraints are present.
Both transformed inputs are proved to lie in `[0,1]`.

The combined error is `squareWidth p^2/4 + foldError L` with the correct
signs. Containment again quantifies over the full epigraph. For every
`δ>0`, `product_epigraph_binary_slack` explicitly takes
`L=squarePrecisionCount δ`, whose folding error is at most `δ`. The
resulting finite LP has exactly the same `p` binaries and error at most
`(1/4)^p/4+δ`. Its affine reflected finite row system proves the matching
hypograph statement, preserving both binary dimension and full downward
output rays. No zero-slack or exact finite-LP threshold assertion is made.

Targeted checks from `formal` passed:

- `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake build --wfail Formal.QuadraticPrecision.ProductLinear`.
- `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake env lean /tmp/topic20-product-linear-review.lean`. This instantiated both zero-binary constructions at error `1/4+1/100` and printed axioms for the two-depth epigraph theorem and both positive-slack theorems. All three use only `propext`, `Classical.choice`, and `Quot.sound`.

No proof changes were needed. P1–P3 now pass this product review in full.
