# Independent review: original quadratic precision headlines

Reviewed `PrecisionUpper.lean` and `ScalarHeadline.lean` on 2026-09-20.
The reviewer did not implement either file. The reusable arithmetic interfaces
were reviewed separately in [precision-arithmetic.md](precision-arithmetic.md).
No mathematical defect was found in the headline assembly.

The three accuracy wrappers construct actual binary linear lifts for the
original quadratic polynomial on the original box. Their integer counts are
respectively rank times depth, negative inertia times depth, and positive
inertia times depth. The wrappers use the proved spectral decomposition and
formulation constructions; no decomposition, negative slice, or formulation
existence is assumed by the headline caller. Conversion from the coordinatewise
box description to `Set.Icc l u` preserves exactly the same domain.

The depth uses `precisionWeight = spectralWeight + 1`. This is strictly
positive even when the quadratic vanishes or the input dimension is zero.
The spectral formulation error is bounded above by the depth guarantee for
this larger weight, because the normalized error factor is nonnegative. This
choice changes only the additive constants in the asymptotic count estimate;
it does not change the rank or inertia coefficient. It is not a claim that
this slightly larger depth equals the smallest explicit construction depth.
The sharper total-weight construction remains a separate result.

Each rate theorem supplies the lower and upper hypotheses of
`precisionRate_of_bounds` for the actual original-box feasibility predicate.
The convex upper bound comes from the binary construction's exact conversion
to an unrestricted-integer convex lift. The binary lower bound follows by the
same conversion before applying the unrestricted-integer obstruction. Thus
both directions retain the number of discrete coordinates. The principal-minor
rank lower theorem and the negative/positive spectral-slice lower theorems have
already constructed the relevant geometric data from the Hessian; none appears
as an additional headline premise.

The resulting `HasPrecisionRate` statements assert attained count minima and
one uniform bounded additive error for every sufficiently small positive real
tolerance. They do not restrict tolerances to dyadic values and do not assume
the existence of an arbitrary finite minimum. Positive-accuracy construction
provides that existence. The graph law assumes positive rank, while the
one-sided laws also cover zero inertia. For zero inertia the separately stated
minimum theorems supply an actual zero-binary lift at every positive tolerance,
and natural-count nonnegativity proves minimality.

The rank-zero theorem identifies the original polynomial with its affine
part, then uses an actual finite affine graph system to attain error zero with
zero binaries. This includes zero input dimension. Exact one-sided convex lifts
at zero inertia are established separately by `SpectralConvex`; the headline
assembly does not assert exact finite LP representability of a curved convex
epigraph or concave hypograph.

This review addresses the assembly and its use of lower-bound interfaces.
The reviewer authored the principal and negative-slice integration modules;
those implementations require their separate independent reviews. This report
does not substitute for them. It also does not certify the separate sharp
isodiametric constant from I2, which is unnecessary for the logarithmic exponent
and remains a distinct geometric obligation.

Targeted verification command from `formal/`, with `~/.elan/bin` on `PATH`:

```text
LEAN_NUM_THREADS=1 lake build --wfail Formal.QuadraticPrecision.PrecisionArithmetic Formal.QuadraticPrecision.PrecisionUpper Formal.QuadraticPrecision.ScalarHeadline
```

Result: passed after the final rank-zero helper and size-bound additions.
The final helper uses the established affine `linearFunctional`, and its
polynomial equality was rechecked. The additional uniform size estimate is
reviewed in [precision-arithmetic.md](precision-arithmetic.md). This was a
targeted module build, not a project-wide check or CI inspection. Final
kernel replay and axiom auditing are recorded separately.
