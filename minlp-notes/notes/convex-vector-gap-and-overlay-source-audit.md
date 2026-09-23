# Source assessment: convex vector error geometry and implicit overlays

Date: 2026-09-05. Bounded comparison of two independently reviewed supporting
notes, [the tilted-error gap](convex-vector-tilted-error-integer-gap.md) and
[the implicit knot overlay](compiled-convex-vector-knot-overlay.md).

The tilted-error result should remain a supporting consequence of the
scalar polynomial gap. Adding a common sufficiently large quadratic makes
both outputs convex; subtracting the outputs recovers the original scalar
function. [Hartman (1959)](https://msp.org/pjm/1959/9-3/pjm-v9-n3-p09-p.pdf)
is an appropriate primary source for the established difference-of-convex
framework. For this compact polynomial domain the particular quadratic
construction is also immediate from the displayed second-derivative bound.
Neither convexification nor transferring a lift through a linear output map
should be presented as a new formulation principle.

What is worth preserving is the explicit limitation: coordinatewise
convexity of two outputs alone does not give a dimension-only binary versus
general-integer comparison when arbitrary symmetric error bodies are
allowed. The construction's error body changes with the instance and becomes
ill-conditioned. It does not settle a fixed-body or uniformly conditioned
variant, and it does not refute the fixed-number-of-outputs box-error bound.
No direct predecessor for this precise convex-polynomial/error-body gap was
located in the bounded search. The broader binary/general-integer distinction
is already established; see the [scalar source audit](nonconvex-polynomial-binary-integer-gap-novelty.md).

For the overlay, there is an exact close primary predecessor:
Lyu, Hicks, and Huchette,
[Building Formulations for Piecewise Linear Relaxations of Nonlinear Functions](https://arxiv.org/html/2304.14542),
Section 3, Proposition 3.1. It merges the union of the breakpoint sets of
several functions with the same scalar input, evaluates all outputs at the
merged knots, and shares one SOS2 formulation. The following paragraph
explicitly contrasts a logarithm of the total merged count with the sum
of the separate logarithmic counts. Thus breakpoint overlay, shared
selection, and the resulting elementary logarithmic count saving are
already known.

The present added scope is algorithmic compression: the knot arrays may be
exponentially long but have polynomial-time indexed evaluators. Exact rank
queries over a polynomial-bit common denominator recover merged endpoints
without listing them. The established circuit compiler then yields a
polynomial rational MILP, and the repository's scalar theorem supplies
the comparison with all convex lifts using unrestricted integer variables.
Binary search, order statistics, continuous Boolean gate encodings, and
the explicit overlay are not new. This is appropriately positioned as a
combined supporting construction with overhead `11+ceil(log2 m)` for
densely encoded convex polynomial outputs, rather than a new general
multiple-function formulation technique. It supplies no lower bound
showing that logarithmic dependence on the number of outputs is necessary.

The existing notes make these distinctions accurately. This audit supports
their qualified positioning, not an unqualified publication-priority claim.

## Unconditional-body extension

The subsequent [unconditional-body candidate](convex-vector-unconditional-log-product-precision.md)
uses a maximum-product positive point `b` in the error body. Its coordinate
box is feasible by unconditionality, and the first-order log-utility
inequality bounds the positive supporting functional `sum v_i/b_i` by `m`.
This is the classical proportional-fair allocation argument; Kelly, Maulloo,
and Tan (1998), Section 2, equation (1), is the correct close attribution
([author PDF](https://www.statslab.cam.ac.uk/~frank/rate.pdf),
[Stanford-hosted copy](https://web.stanford.edu/class/cs244/papers/ShadowPricesFairnessStability.pdf)).
The author URL timed out, but the Stanford copy was opened and PDF page 3
directly confirms equation (1) and its equivalence to unit-weight log-utility
maximization. The general convex-body form follows from the same
elementary first-order inequality, independently of the network setting.

The candidate combines that supporting functional with nonnegative Jensen
vectors and the existing scalar compiler. Its proposed finite overhead is
`ceil(log2(4m-1))`; its rational compact overhead is `14+ceil(log2 m)` under
a polynomial strong separation oracle and known rational radii. The body
need not be polyhedral, since the final formulation uses the inscribed box.
These are meaningful additions to the formulation comparison, not a new
maximum-product or oracle-optimization algorithm. Source assessment remains
qualified: no matching whole-convex-lift count theorem was located, and the
candidate does not establish necessity of the logarithmic output dependence.
It also retains unconditionality, so the tilted-body gap above is compatible
with it. This audit records the claimed constants without independently
rechecking their full analytical dependencies.
