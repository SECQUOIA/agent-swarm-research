# Source audit: positive separable precision with unconditional error bodies

Date: 2026-09-05. Independent source audit of
[the candidate theorem](positive-separable-unconditional-error-precision.md)
and its [rational allocation lemma](rational-log-product-convex-body-oracle.md).
This is a bounded literature audit, not proof of priority or a substitute for
the independent mathematical reviews.

## Assessment

No matching theorem was found that bounds the minimum integer dimension of
every convex lifted graph approximation by this log-product allocation under
an arbitrary unconditional output-error body. The defensible contribution is
the whole-error-body Jensen comparison and its combination with a compact
rational MILP construction. Convex log-utility allocation over general
downward-closed sets is already established. Unconditional norm monotonicity,
separation-based convex optimization, and polynomial interpolation are also
established ingredients.

Relative to the repository's componentwise positive-polynomial result, this
is a useful extension of its allocation principle. It preserves the finite
integer overhead `O(r+sum_i log D_i)` without an output-dimension ellipsoid
rounding loss. It is best presented together with that theorem rather than as
a new general convex-optimization method. For fixed degree, the overhead is
`O(r)`; the sharper diagonal-quadratic construction retains `5r+1`.

## Closest allocation precedent

Laurent Massoulie's primary report,
[Structural properties of proportional fairness: stability and insensitivity](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2005-102.pdf),
explicitly permits a convex, non-increasing capacity region in the positive
orthant. Section 1, equations (1)--(2), includes weighted logarithmic utility.
Section 2, printed page 5, changes to logarithmic allocation coordinates and
proves the transformed feasible set convex using convexity and downward
closure. Thus log-product optimization over general monotone capacity sets,
including its logarithmic-coordinate interpretation, is prior work. Its
application is bandwidth allocation and stability, not graph approximation
or integer dimension.

In the candidate, `P={p in [0,1]^r:Cp in K}` is downward closed because
`C>=0` and `K` is unconditional. Taking unit utility weights makes its
allocation objective a direct instance of this familiar framework. The
new interpretation concerns what the allocation certifies about formulations.

The earlier linear-capacity version is explicit in Kelly, Maulloo and Tan,
[Rate control for communication networks: shadow prices, proportional fairness and stability](https://web.stanford.edu/class/cs244/papers/ShadowPricesFairnessStability.pdf),
Section 2: maximize weighted log rates subject to linear resource capacities.
The general-body extension should cite Massoulie as well as this source;
citing only linear resource allocation would understate the antecedent.

## GLS oracle assumptions checked against the original source

The primary source is Groetschel, Lovasz and Schrijver,
[The ellipsoid method and its consequences in combinatorial optimization](https://ir.cwi.nl/pub/10046/10046D.pdf)
(1981). Printed page 172, Definition (5), returns a rational point within
the requested distance of the body and with the requested objective accuracy.
Definition (6) uses a separator normal with norm **at least one**, matching
the candidate's normalization. Equation (7) assumes known inner and outer
balls about a common center; the input model includes the binary accuracy
and radius encodings. Theorem (3.1), printed page 177, gives polynomial
separation--optimization equivalence. Printed page 178 already discusses
downward-closed positive-orthant bodies and antiblockers. These source
conditions were checked in the primary text, including the page-172 scan.

The candidate supplies its own rational log-product hypograph, known balls,
and rational weak separator, so the stated import has the needed input.
GLS weak optimization alone does **not** promise exact feasibility. The
candidate's explicit central-ball convex-combination repair addresses that
gap. Its polynomial-bit log evaluation and rational arithmetic still need
the mathematical and implementation checks stated in the supporting lemma.

The supporting oracle lemma allows signed `C` and a nonsymmetric closed
convex `K` containing a known ball: its own hypograph is bounded by the
coordinate and objective restrictions. The graph theorem uses the stronger
nonnegativity and unconditionality assumptions at different steps. These
two scopes should remain distinct.

## Approximation and formulation antecedents

The [positive-polynomial source audit](positive-separable-polynomial-precision-novelty.md)
records the closest polynomial MILP constructions: Teles, Castro and Matos's
2013 univariate and multiparametric disaggregation work already uses radix
expansions and residual variables for polynomial approximation. Shared
binary encodings for several outputs and exact binary--continuous product
linearization are also established. The extension does not establish
independent priority for its prefix-power recurrence or Taylor enclosure.

Anisotropic interpolation already allocates resolution through local error
metrics. Cao's
[An interpolation error estimate on anisotropic meshes and optimal metrics for mesh refinement](https://epubs.siam.org/doi/10.1137/060667992)
optimizes interpolation metrics; Frey and Alauzet's
[Anisotropic mesh adaptation for CFD computations](https://www.ljll.fr/~frey/publications/cmame05-3.pdf)
combines metrics for several solution fields. The checked comparisons in
[the weighted-quadratic audit](quadratic-weighted-precision-algorithm-novelty.md)
explain why mesh design and multiple error targets are prior mechanisms.
These sources do not provide the candidate's uniform minimum-integer
comparison against arbitrary convex lifts and unrestricted integer variables.

## What distinguishes the proposed theorem

The relevant chain is specific. Parity-compatible exact graph points force
their nonnegative Jensen vector into the same error body `K`. Coordinatewise
domination and convex expectation then place the transformed-support
covariance allocation `Cp` in **that body itself**. This gives a volume lower
bound for every convex lift. Conversely, the polynomial Taylor construction
uses a rational rectangle dominated by a feasible `Cp`, so every admitted
error lies in `K`. The upper formulation does not need a finite exact linear
description of a curved `K`.

This yields a comparison to the best possible formulation, not merely a
good grid within a prescribed class. It is the strongest novelty claim
supported by this search. The construction's running time and continuous
size can depend on the number of outputs and the oracle encoding even
though the additive integer overhead does not.

## Limits and search record

Unconditionality means invariance under **independent** coordinate sign
changes. Central symmetry alone does not justify coordinatewise domination;
arbitrarily correlated ellipsoids therefore remain outside this theorem.
Nor does the result assert efficient optimization of the constructed MILP.
Polynomial dependence on degree uses the stated dense or equivalent
degree-explicit polynomial input, not binary-encoded huge sparse exponents.

The focused searches combined unconditional/monotone error norms with
anisotropic interpolation, separable polynomial graph approximation,
minimum integer variables, and proportional-fairness formulations. Most
unconditional-interpolation hits concerned function spaces or numerical
stability, not the stated output-error geometry. No exact match was found
in the checked primary sources. This supports a qualified novelty statement,
not an assertion that no matching result exists anywhere in the literature.
