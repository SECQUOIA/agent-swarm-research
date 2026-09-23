# Checks to carry into Stage 2

The uniform growing-degree pinned-gate source requires explicit accounting of
constants raised to the degree. Its estimates (17) and (22) display a constant
times r^2 times (k|x|)^(-2r-4), but the elementary shifted-denominator estimate
only gives (2/(k|x|))^(2r+4). A factor such as 2^(2r+4) cannot be absorbed in
a constant independent of r. It appears repairable by retaining C^(2r+4)
and choosing the leading k constant sufficiently large, but the entire
contractivity/high-band calculation must check that repair.

Do not silently replace sin(t) by t in ultra-high-accuracy lower bounds:
K may be far smaller than delta^2. The source's affine angle coordinate and
retained sine Taylor polynomial address this issue and need full verification.

The Fejer--Riesz lower route should remain independent of the exterior-Taylor
route. Its small-index/radius branch and large-index fixed-radius branch must
include all quantifiers, particularly arbitrarily large log(1/K).

The source pinned-gate theorem admits a subpolynomial gap in intermediate
joint limits. A complete paper must distinguish a proved theorem with a
limited parameter scope from an assertion of a fully matched uniform law.
Investigate whether the gap can be closed; do not label an unmatched bound
optimal merely to produce a more sweeping headline.

## Sharper intermediate comparison

Let ell=min{j:G_j<=K} tend to infinity with ell=o(D), D=log(1/delta).
The finite-index Fejer--Riesz lower bound at r=ell-1 directly gives

    Q >= c*ell*(G_(ell-1)-K)^(1/ell)*delta^(-1+1/(2ell)).

If K<=(1-gamma)G_(ell-1), fixed gamma>0, the root factor is bounded below
by a positive rho,gamma-dependent constant using the exact threshold
asymptotic. Hence lower and pinned upper share delta^(-1+1/(2ell)), with
prefactors ell and ell^3. The upper's additive D term is negligible here.
This leaves at most an ell^2 ratio away from upper tier boundaries and
includes K=G_ell, because G_ell/G_(ell-1) tends to R0^(-2)<1. It is stronger
than merely comparing logarithms or using a non-sharp constant in the
exp(-C D/log(1/K)) bound. Retain the exact threshold-distance factor when
K approaches the upper boundary; no uniform Theta is claimed there.
