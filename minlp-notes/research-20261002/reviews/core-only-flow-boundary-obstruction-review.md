# Review of the core-only flow boundary obstruction

Date: 2026-10-02. Verdict: **pass**. This is a fresh actual-file,
analytical review of the
[uniform-label obstruction](../new-direction/core-only-flow-boundary-obstruction.md).
It verifies a limitation of the stated uniform-label-plus-enumeration
strategy, not a hardness result or a limitation of all exact certificates.

The two residual flows give exactly the value function in (1). On the
event `gamma_i>=1/2`, each nonzero feasible core point has positive
value, so the origin is its unique core optimum. Since `v_i>=v_i²`
on `[0,1]` and `min(v_1,v_2)>=0`, the projected growth inequality is
valid with `g=1/2+min_i gamma_i`. At the unit vector for a smallest
noise coefficient, the minimum residual cost is zero and the ratio
of value gap to squared distance equals this constant. Thus the
claimed growth constant is exact, not merely a lower bound.

Both residual flows are optimal at the origin. Distance to the full
mixed optimal set is exactly the core norm: a feasible flow can be
paired with its own origin point. The same growth bound therefore
holds for distance to that set, and equality is attained using the
opposite arc at the selected unit vector. Growth relative to one
chosen mixed optimizer fails because the other origin flow is tied.

For the endpoint-inclusive `M`-point law, a coordinate atom is
`-1+2j/(M-1)`. When `M>=4` is a power of two, the condition that this
be at least `1/2` is precisely `j>=3M/4`. There are `M/4` such atoms.
Independence gives the exact probability `1/16` for the two-coordinate
event, including the smallest allowed grid `M=4`.

Every positive-width origin rectangle contains two points with
opposite unique optimal residual labels. The perturbation does not
affect their difference. The corresponding residual cycles have costs
`v_2-v_1` and `v_1-v_2`; potential differences telescope to zero on
each cycle. Hence no valid nonnegative-reduced-cost certificate can
make a single label optimal throughout that rectangle, regardless
of the representation of its potentials.

The dyadic origin cell has exact minimum corner value zero and
corrected lower bound `-h²/4`. It survives at every positive mesh
size under the stated corrected-grid pruning rule. A retained hull
containing that cell consequently cannot pass the uniform-label
certificate at any finite level. This does not exclude a different
stopping rule based on value, an exposed core face, or all optimal
flows; the note explicitly restricts its claim.

Adding serial tied two-arc stages preserves the conditional value
and closure failure while giving exactly `2^m` feasible integral
flows. A strategy that insists on that certificate and then
literally enumerates all flows therefore incurs at least
`2^m/16` expected enumeration work. The input uses only a polynomial
number of bits in `m`. This is a lower bound on that specified
strategy; the example itself remains easy, as the main text states.

No numerical solver or duplicate diagnostic was run for this review.
The existing boundary-search checker's results are not claimed as
independently rerun. The review passed scoped local-link, fence,
trailing-whitespace and `git diff --check` checks. No index or CI
checks were made.
