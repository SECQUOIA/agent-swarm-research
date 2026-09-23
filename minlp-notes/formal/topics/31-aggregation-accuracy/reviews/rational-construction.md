# Independent semantic review of the exact rational construction

Reviewed `AccuracyRational`, `AccuracyRationalMesh`, and
`AccuracyRationalBound`, including the complete Hausdorff bridge.

The integer coefficients are exactly `(m²,j²,2*m*j)` and
`(j²,m²,2*m*j)`. The implemented family includes the first branch through
`j=m` and the second branch only through `j<m`, so the shared diagonal
cut is counted once. Each branch is injective for `m>0`, and the branches
are disjoint with those index ranges. The proved cardinality is exactly
`2*m+1`. The positive-ray uniqueness theorem also rules out hidden
duplicates created by proportional vectors.

All coefficients are natural numbers at most `2*m²`, and the exact cone
discriminant identity proves goodness through the existing source-good
classification. The nonzero coordinate `m²` handles the endpoint cuts.
The construction includes both axes, and `rationalMeshSize` implements
`floor((N-1)/2)` with a positive size and at most `N` cuts for `N≥3`.

The binary encoding theorem concerns actual natural-number coefficients
and `Nat.size`, including its zero convention. It proves a bound of
`2*Nat.size N+1`, and the explicit logarithmic consequence is
`2*Nat.log 2 N+3`. Thus the logarithmic bit claim has a formal integer
encoding bound, not merely a real magnitude estimate or rounding argument.

For angular coverage, nearest integer rounding approximates a slope in
`[0,1]` within `1/(2*m)`. The global derivative bound for arctangent proves
it is 1-Lipschitz. Applying this to `tan(theta)` covers the first half
quadrant, and reflection around `pi/4` covers the second half. Both axes
are included. Every angle therefore has a rational sample within
`1/(2*m)`, giving the precise radius required for the advertised constant.
The proof does not assume the angular gap or round the three coefficients
independently.

The exact coefficient-to-angle identities multiply the normalized angular
weight by `m²+j²>0`. The two branches use the arctangent angle and its
reflection, respectively. Thus every point satisfying the actual integer
cuts satisfies the corresponding angular tests; this step preserves the
cut inequalities because the scaling factor is positive, including at
the coordinate endpoints.

`hausdorffError_rationalCuts_le` applies the whole-relaxation repair theorem
with covering radius `1/(2*m)` and the actual source-good family. It obtains
exactly `5*sqrt(2)/(4*m²)` in the true Euclidean Hausdorff metric. For the
budget choice `m=floor((N-1)/2)`, the proved comparison `N≤4*m` yields the
explicit bound `20*sqrt(2)/N²` for every `N≥3`. Together with the family
count and logarithmic integer encoding theorem, this establishes A07–A09
with all constants uniform in `r≥2`.

No cardinality, coefficient, bit-size, mesh-coverage, Hausdorff, or
source-correspondence defect was found. The result does not make a claim
about numerical conditioning or the computational cost of solving the
resulting finite relaxation.
