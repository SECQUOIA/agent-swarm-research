# Stage 1, round 1: independent review 3

Reviewed `sections/02-model.tex`, `sections/03-exact.tex`, and
`sections/04-fixed-accuracy.tex`, together with the four Stage 1 source notes
listed in `audit/source-map.md`. No peer reports were read and no manuscript
files were changed. The applicable repository environment instructions were
read; no Python execution or package installation was needed.

**Findings: 0 major, 1 minor.** The minor finding concerns the stated domains
of auxiliary inequalities, not the fixed-accuracy theorem or its proof on the
domains actually used.

## Minor finding: state the domains of auxiliary positivity claims

- **Location:** `sections/04-fixed-accuracy.tex:161` and `:169`; also make the
  domain explicit in the pinned-tail display at `:127`.
- **Demonstration:** The phrase “the nonnegative polynomial
  `G_r-e(y)`” is only true on `[1,rho]`. Indeed,
  `G_r-e(y)=G_r[1-T_{2r}((y-m_rho)/h_rho)]` is negative outside that interval.
  More directly, the claim `d(x)=1-x-S_N(x^2) in [0,1] for x>=0` is false
  without the upper endpoint `x<=1`: with the permitted choice `N=1`,
  `S_1(u)=u(1-u)/2`, and `d(2)=5`. Every subsequent use is within `[0,1]`,
  so this does not invalidate the argument. Similarly, the pinned-tail
  estimate is proved using `arcsin x` and should state the ambient domain
  instead of leaving it implicit.
- **Actionable repair:** Say that `G_r-e(y)` is nonnegative **on `[1,rho]`**;
  change “for `x>=0`” to “for `0<=x<=1`”; and write
  `C_0 delta <= |x| <= 1` in the pinned-tail display.

## Substantive checks completed

- **Pinned gate:** Pairing the positive and negative pin angles gives an
  even, pi-periodic trigonometric polynomial and hence an even algebraic
  polynomial. Its stated degree, range, exact pins, local order
  `2r+2`, and tail order `2r+4` follow from the displayed construction.
  The tail denominator bound holds uniformly up to `|x|=1` for sufficiently
  small delta and fixed sufficiently large `C_0`.
- **Global contractivity:** The three-region estimate gives
  `delta P(x/delta)W <= C delta + C delta^(1-2r)m^(-2r)`.
  Substitution of `m asymp M delta^(-1+1/(2r))` cancels the delta exponent in
  the second term. Choosing fixed `M` first and then sufficiently small
  delta proves both sides of the contractivity bound, including at the
  negative pins. No positivity of the unweighted low polynomial on the
  whole interval is being assumed.
- **Exact threshold equality:** The contact slack bounds the leakage with
  a spare factor `delta^(1/r)`. The signed error expression controls the
  negative error by `e>=-G_r` and the positive error by the pinned slack.
  It therefore gives exactly `G_r delta`, including endpoint and interior
  contacts, rather than merely `(G_r+o(1))delta`.
- **High interval and singleton:** Both leakage exponents are sufficient
  for every fixed `r>=1`, including the smallest case `r=1`, where
  `delta P W=O(delta^2)`. For the coarse tier, the high-interval construction
  reaches equality at `G_0`, while the degree-four singleton construction
  satisfies `W(delta)=1`, `W(1)=0`, and the required interval contractivity
  for sufficiently small delta. The zero-query obstruction establishes the
  lower half of the singleton `Theta(1)` statement. The high-interval
  interpolation lower bound uses a positive-length arc and is not applied
  to the singleton.
- **Threshold formula and limits:** The exterior Chebyshev argument,
  global admissibility, uniqueness of the exterior maximizing point,
  strict decrease, first-threshold formula, and exponential asymptotic
  constant are consistent. The inverse asymptotic correctly retains
  bounded integer-rounding uncertainty. Constants are used with fixed
  `rho,c,K,r`; no uniform joint-limit claim is needed here.
- **Other claims:** Checked the two-point error factorization, corrected
  pairwise constant, differentiated normalization bound, exact-interval
  obstruction, nonnegative Taylor-limit hierarchy, explicit Markov
  constant for even parity, rounded Fejer construction, and the scope of
  the single-transform parity comparison. The scalar and walk arguments
  respect the requirement of arbitrary oracle completion.

The joint-accuracy, LP, and full introductory/literature stages were outside
this review's scope; their absence is not a finding.
