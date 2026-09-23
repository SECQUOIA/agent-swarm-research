# Separable vector graphs with oracle error bodies: source addendum

Date: 2026-09-05. Bounded assessment by `joint_flow_novelty`. The full
[extension draft](convex-separable-vector-oracle-curvature-rank-precision.md)
and its promoted shared-basis separable dependency were read. The author
reports two independent proof audits passing; this note assesses sources.

No matching combined theorem was found in the checked primary literature.
The candidate transfers the existing curvature-rank construction and
shared-basis product comparison to separable multivariate vector outputs
with an arbitrary unconditional strong-oracle error body. Its bounds are

```
p_bin <= p_conv + 8n + 2n ceil(log2 r)    (finite real coefficients),
p_out <= p_conv + 21n + 2n ceil(log2 r)   (compact rational construction).
```

Here `n` counts nonaffine input coordinates, and `r` is the dimension of the
single shared nonlinear output image across all coordinate summands. The
benchmark remains the minimum integer dimension of a lift for the original
whole vector graph, with unrestricted continuous size and general integers.

## What the extension inherits

The [one-input oracle-body assessment](convex-vector-oracle-curvature-rank-novelty.md)
records direct primary precedents for maximum-volume and approximate
barycentric spanners, approximate-oracle spanner construction, polar and
anti-blocker access through GLS, parity-based MICP rank bounds, and shared
vector interpolation. Those source readings are reused here. Neither the
spanner construction nor positive-polar access becomes new when the input
has several coordinates.

The [earlier separable source assessment](convex-separable-vector-curvature-rank-novelty.md)
already treats one shared output basis and a product packing against the
original vector lift. The present extension preserves that mechanism.
Selecting one basis across all coordinate blocks is necessary for the stated
comparison; independently selecting different bases would not supply the
same conclusion. The lattice-ball estimate and greedy separated subset
remain elementary supporting arguments, not a new coding theorem.

## A direct separable approximation comparison

Bärmann, Burlacu, Hager and Kleinert,
*On piecewise linear approximations of bilinear terms: structural comparison
of univariate and bivariate mixed-integer programming formulations*,
[open primary article](https://link.springer.com/article/10.1007/s10898-022-01243-y),
Section 2.1, Definition 5 and Lemma 1, explicitly defines the combined error
of sums of univariate interpolants and bounds that error using the individual
summand errors. The introduction and Section 3 compare numbers of simplices
needed for accuracy with the strength of the resulting continuous
relaxations. Sections 1–2 and the setup of Section 3 were read directly;
the remaining bilinear comparison proofs were not audited here.

Comparison: adding coordinatewise interpolation errors and using separable
PWL graph formulations are established. That source compares prescribed
approximation families for a scalar bilinear expression, including
univariate reformulations. It does not supply the candidate's comparison
with all convex integer lifts for the original vector tube, its oracle-body
assumptions, or its shared nonlinear-rank guarantee. Its distinction between
approximation size and relaxation strength also applies here: the current
integer-count theorem does not imply an ideal or computationally strong MILP.

A search also returned the publisher's indexed introduction to *Polyhedral
methods for piecewise-linear functions I: the lambda method*, which calls
separable lambda interpolation established. Direct retrieval returned 403;
the full paper was not read or used for a more specific theorem claim.

## Qualified contribution and limits

The additional conclusion is a coupled-body transfer: the same two body
bases work across all separable coordinates, while an explicit rational
parallelotope absorbs the summed chord and rounding errors. This produces
a complete MILP without retaining oracle constraints or enumerating facets
of the original error body. The resulting overhead depends on `n` and `r`,
and the total rational encoding remains polynomial in the supplied dense
separable representation and oracle data.

This is a useful extension of the two existing local theorems, rather than
a separate broad approximation or oracle principle. Compared with the
explicit-facet companion, it trades a larger rank-dependent overhead for
access to nonpolyhedral or implicitly described unconditional bodies. It
should not be described as uniformly improving the explicit-facet count.

The result excludes mixed-coordinate nonlinear terms. Output count, dense
degree, coefficients, and radius encodings still affect time and formulation
size; their absence concerns the additive integer-count bound only. The
theorem does not compute `p_conv`, prove necessity of its overhead, or give
a polynomial algorithm for solving the output MILP. Finite continuous
summands support the real-coefficient existence result, whereas the compact
rational construction retains the dense polynomial and oracle promises.

Fresh targeted searches for separable vector approximation, shared
barycentric bases, and minimum integer dimension found no closer combined
result. This is a bounded source finding, not an exhaustive priority claim.
The existing attribution to the oracle, compiler, interpolation, and product
packing dependencies should remain explicit when presenting the extension.
