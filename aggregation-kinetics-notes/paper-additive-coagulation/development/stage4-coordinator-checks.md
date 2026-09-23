# Coordinator checks during Stage 4 authorship

These checks supplement the later five independent manuscript reviews.

## Entropy and second moments

The earlier entropy calculation can be completed under the accepted locally bounded second-moment solution class. Let f(x)=x log x and use its tangent continuation f_R above R, for R at least one. Then f_R-(1+log R)x is bounded, so the bounded weak equation and conserved mass give its exact balance. Both f_R and f-f_R are convex and vanish at zero. Their ratios to x are increasing; consequently their fragmentation losses are nonnegative, and the truncated loss is at most the full loss. Jensen bounds the full loss by x log 2 under the expected daughter count and mass constraints.

The merger increments satisfy 0 <= Delta f_R <= Delta f, and (x+y)Delta f <= (log 2)(x+y)^2. The latter is integrable with locally bounded second moment and finite count and mass. Endpoint dominated convergence uses |f_R| <= 1/e+x^2. This proves the complete absolutely continuous entropy balance without a third moment.

There is a stronger sharp production constant than the original note's 1-log 2. Divide the accepted sharp fractional pair inequality by 1-p and let p tend to one. It yields

(x+y) Delta(x log x) >= 4(log 2)xy.

The coagulation contribution is therefore at least 2 lambda m^2 log 2. Critical fragmentation loses at most lambda m^2 log 2, leaving H' >= lambda m^2 log 2. Monodisperse initial data and equal splitting attain the instantaneous coefficient. The stage author independently reached the same truncation method and constant before receiving the coordinator's derivation.

Tangent continuation of x^2 works similarly: subtracting its linear tail leaves a bounded test; merger increments are bounded by 2xy and fragmentation losses by x^2. This establishes the exact second-moment balance under the accepted finite-second-moment class. Expected daughter count two, mass x, and daughter sizes below x already imply x^2/2 <= integral z^2 b_x(dz) <= x^2. An actual complementary pair is unnecessary for this deterministic inequality.

## Finite count and mass ceiling

The exact count generator has drift b and squared-state drift 4bL-b. Its compensated bracket gives variance b(2L0-1)t+b^2t^2, and Doob gives the stated uniform o(n)-horizon bound when L0=O(n). At t=C log n, the mass ceiling nm and the continuum fractional bound give discrepancy at least 1-c_n^(1-p)n^(-eta), eta=bC kappa_p-(1-p)>0. The fixed choice of p is valid because kappa_p/(1-p) tends to log 2 as p tends to one. This does not identify the first failure time.

The omitted diagonal contributes exactly lambda(2-2^p) M_(p+1)/n to the empirical moment generator. Its sign is positive for fractional p. A formal factor 1/n need not remain small when large sizes develop.

## Power-kernel boundary

For 0<alpha<=1, D=M_alpha is finite. The stationary jump-rate weighting q(x)=xD+2m x^alpha has total flux 3mD, and x^(-alpha) is integrable under that weighting because D M_(1-alpha)+2mN is finite. Stationary gain equality justifies the singular test without a negative population moment.

Symmetrizing the coagulation loss and using concavity of z^alpha gives loss <=alpha mN. Fragmentation gives gain >=2mN(2^alpha-1), strictly larger. The explicit alpha=1, p=1/2, R=64 drift is 27 sqrt(2)+2 sqrt(65)-54 >151/500, using rational strict lower bounds for the two roots. These are instantaneous generator statements, not an existence assertion for the faster kernel.

## Figure inspection

The original six-panel plot is correct but its three-column layout makes type small at manuscript width. Requested a paper-specific two-column, three-row layout with unchanged data and reference curves, reproducible from the copied plotting script. No particle rerun is needed for this layout change. The figure must retain its distinction between finite realizations and continuum reference bounds.
