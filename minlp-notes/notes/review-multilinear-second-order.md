# Independent audit of the second-order multilinear upper bound

Date: 2026-09-04. Reviewer: independent `review_fbbt` agent.

The proof in `results/positive-multilinear-second-order-upper.md` passes this independent audit. The harmonic integral bound, optimal scalar mixture, finite estimates, and second-order asymptotic constant were checked directly. The strengthened Lambert-W estimate proposed by the author during the audit also passes. This review uses the separately audited positive-multilinear deficiency representation and the easy-term independence estimate from the sharp-degree theorem.

The later cutoff-tuning improvement also passes; its audit is recorded at the end of this file. It improves the final denominator constant from `-1` to `0` when expressed using `L_0=1+ln(d-1)`. The earlier fixed-cutoff estimates remain correct as special cases.

The final consolidated text, headed *A finite harmonic-coupling bound with an optimized cutoff*, was reread in full. Its general-cutoff theorem, finite Lambert certificate, and tuned asymptotic proof pass. One minor presentation request was sent to the author: explicitly discard affine terms before defining the maximum high-coordinate failure marginal, so an empty maximum never arises. Affine terms have zero gap and do not affect any result.

## Harmonic integral and boundary cases

For a one-low-coordinate monomial, let the low anchor have mean `u<=1/2`, and write its high-coordinate failure marginals as `p_1,...,p_r`, where `r<=d-1`. Put `S=sum p_j`, `T=min(u,S)`, `M=d-1`, and `L=1+ln M`.

The harmonic normalizer is valid even at `d=2`, where `M=L=1`. For `p>0`, its cutoff `h=min(Mp,1)` satisfies `h>=p`, and its normalizer `1+ln(h/p)` lies in `[1,L]`. Direct integration of the constant part over `(0,p)` and the harmonic part over `(p,h)` gives exactly failure marginal `p`. Coordinates with `p=0` must be treated by the explicitly stated never-fail convention.

If `T=0`, the required deficiency lower bound is zero under every coupling, so no division by `T` is used. If `T>0`, at least one failure marginal is positive. Threshold coupling has deficiency exactly `min(u,p_max)`, hence at least `zT` for `z=min(p_max/T,1)`.

When `p_max<T`, integrate over `t in [p_max,T]`. The low anchor is one throughout this interval. Every `p_j<=t`, so an active high coordinate has conditional failure probability at least `p_j/(Lt)`. Since `t<=T<=1/2<1`, inactivity is equivalent to `p_j<t/M`. The inactive marginal sum is at most `r t/M<=t`; equality or strictness at isolated endpoints does not affect the integral. Thus the active marginal sum is at least `S-t>=T-t`.

Conditional independence gives union-failure probability at least

`1-exp(-(T-t)/(Lt))`.

Substitution `v=t/T` proves harmonic deficiency at least `T J_L(z)`. When `p_max>=T`, the same assertion reduces to the nonnegativity of deficiency because `z=1` and `J_L(1)=0`. In particular, the proof does not apply the active-coordinate estimate to a range containing marginals larger than `t`.

## Scalar root and mixture

For every `L>=1`, the integrand `F_L(v)=1-exp(-(1-v)/(Lv))` extends continuously to values one and zero at the two endpoints. It is strictly decreasing on `(0,1)`. Therefore `J_L` is decreasing and convex, and `J_L(z)-z` is strictly decreasing. Its endpoint signs are positive and negative, so exactly one root `z_L` lies in `(0,1)`.

With `a=F_L(z_L) in (0,1)`, the supporting-line inequality for the convex function `J_L` gives

`J_L(z)+a z >= (1+a)z_L`.

Consequently harmonic probability `1/(1+a)` and threshold probability `a/(1+a)` guarantee deficiency `z_L T` for every hard term. This is optimal for these two scalar lower-bound curves: at their crossing `z=z_L`, every convex combination has value exactly `z_L`. This does not claim optimality among all actual Bernoulli distributions or exploit attainability of every scalar `z` by an instance.

Mix this hard-term distribution and independence with weights proportional to `1/z_L` and `2/c`, respectively, where `c=1-exp(-1)`. The appropriate component supplies `T/Z` to each monomial for `Z=1/z_L+2/c`. Other contributions are nonnegative. Nonnegative polynomial coefficients therefore allow summation and give the claimed ratio bound. Terms of zero deficiency and affine terms cause no exception.

## Integral estimates and elementary finite constant

The elementary bounds `x-x^2/2<=1-exp(-x)<=x` hold for every `x>=0`; no small-argument restriction is needed. For `x=(1-v)/(Lv)`, the two exact integrals are

`integral_z^1 x dv = [ln(1/z)-1+z]/L`,

`integral_z^1 x^2 dv = [1/z+2ln z-z]/L^2`.

These confirm all signs in the draft's equation (7). In particular, the logarithmic term in the second integral has a plus sign.

For `z=A/L`, multiplication of the lower bound by `L` gives

`L J_L(A/L) >= ln L-ln A-1-1/(2A)`

after discarding the nonnegative terms `A/L`, `ln(L/A)/L`, and `A/(2L^2)`, assuming `0<A<=L`.

For `ell=ln L>=4`, set `A=ell-ln ell-2`. This function increases for `ell>=4` and its value at four exceeds one half, so `A>=1/2`. Also `A<=ell<L`. Hence

`ell-ln A-1-1/(2A) >= ell-ln ell-1-1/(2A) >= A`.

Thus `J_L(A/L)>=A/L`. Strict decrease of `J_L(z)-z` gives `z_L>=A/L`, proving the finite denominator `ln L-ln ln L-2` with the stated condition `L>=exp(4)`.

## Lambert-W certificates

Let `w>0` solve `w exp(w)=L/exp(1)`, equivalently `w+ln w=ln L-1`.

The original certificate `A=w-1/w`, under `w>=2`, is valid: `A>0`, `A<L`, and

`A+ln A+1/(2A)-(w+ln w) = -1/w+ln(1-1/w^2)+1/(2A)<=0`.

The author proposed the stronger choice

`A=w-1/(2w)`, under only `w>=1`.

This also passes. Here `A>=1/2`, `A<L`, and the same difference becomes

`ln(1-1/(2w^2))+1/(4Aw^2)`.

Using `ln(1-t)<=-t` and `A>=1/2` bounds it above by zero. The scalar integral lower bound therefore gives

`z_L >= [w-1/(2w)]/L`,

and hence the stronger finite ratio bound

`R(d) <= L/[w-1/(2w)] + 2/c`, whenever `w>=1`.

The latter condition is equivalent to `L>=exp(2)`. No numerical evaluation of Lambert W is needed for the proof; its positive root exists uniquely because `w exp(w)` is strictly increasing for `w>0`.

## Second-order asymptotic

Set `alpha=L z_L` and `ell=ln L`. The elementary finite bound gives `alpha>=ell-ln ell-2`, so `alpha->infinity`. At the scalar fixed point, the integral upper bound gives

`alpha<=ell-ln alpha-1+alpha/L`.

For sufficiently large `L`, `alpha>=1`, which justifies dropping the nonpositive terms `-ln alpha-1` and obtaining `alpha<=ell/(1-1/L)`. The lower and upper bounds imply `alpha/ell->1` and `alpha/L->0`.

The full integral bounds now imply

`alpha=ell-ln alpha-1+o(1)`.

Indeed, the quadratic correction has magnitude at most `1/(2alpha)` plus terms vanishing as `ell/L`, and all the omitted linear terms vanish. Finally, `ln alpha-ln ell=ln(alpha/ell)->0`, giving

`L z_L=ln L-ln ln L-1+o(1)`.

This verifies the constant `-1`, not merely the leading scale. It is an asymptotic expansion of the proved **upper-bound certificate**. It does not establish a matching second-order expansion of the true worst ratio.

The final draft also states the sharper Lambert comparison

`alpha=w-1/(2w)+O(w^-2)`.

This passes as well. The global upper Taylor bound `1-exp(-x)<=x-x^2/2+x^3/6` and `x<=(Lv)^-1` bound the integrated cubic remainder, after multiplication by `L`, by

`L integral_(alpha/L)^1 x^3/6 dv <= 1/(12alpha^2)`.

The previously discarded terms are `O(ln L/L)=o(alpha^-2)`, so

`alpha+ln alpha=ln L-1-1/(2alpha)+O(alpha^-2)`.

Compare with `w+ln w=ln L-1`. Since `alpha~w`, the derivative `1+1/t` of `t+ln t` and the mean value theorem first give `alpha-w=O(1/w)`. Substitution back then gives `alpha-w=-1/(2w)+O(w^-2)`. Thus the strengthened finite Lambert denominator has the asserted asymptotic precision.

## Numerical checks

As a supplementary check, adaptive quadrature and scalar root finding evaluated the exact integral after the stable substitution `v=exp(t)`. Tested values included `L=1`, `2`, `exp(2)`, `exp(4)`, `10^4`, `10^20`, and `10^100`. All applicable finite bounds held. Selected values of `alpha=L z_L` and the strengthened Lambert lower bound were:

| L | alpha | w-1/(2w) |
| --- | ---: | ---: |
| exp(2) | 0.967742466906 | 0.500000000000 |
| exp(4) | 2.123806905430 | 1.981484605760 |
| 10^4 | 6.294619847670 | 6.281656585090 |
| 10^20 | 41.318342777000 | 41.318012838900 |
| 10^100 | 223.845321990000 | 223.845310423000 |

These numerical checks supplement the symbolic proof and do not replace it. No counterexample or unresolved mathematical issue was found.

## General cutoff tuning and the improved denominator constant

The author proposed allowing any real cutoff `M>=r_0=d-1`, with

`L=1+ln M`, `rho=r_0/M in (0,1]`.

This is valid: the harmonic distribution does not require an integer cutoff. Its marginal normalization is unchanged. In the hard-term integration interval, inactive marginals have sum at most `r_0 t/M=rho t`, so the active marginal sum is at least `T-rho t`. This gives the generalized curve

`J_(L,rho)(z)=integral_z^1 [1-exp(-(1-rho v)/(Lv))] dv`.

The case `p_max>=T` still uses `z=1` and zero integral. The integrand is positive and strictly decreasing on `(0,1)`, and extends continuously to one at zero. Its value at one is now `1-exp(-(1-rho)/L)`, which is positive when `rho<1`. Only the primitive's endpoint value changes: `J_(L,rho)(1)=0` still holds. Thus the unique-root argument, convex tangent mixture, and deficiency guarantee all remain valid.

For `x=(1-rho v)/(Lv)` and `z=A/L`, direct integration gives

`L integral_z^1 x dv = ln L-ln A-rho+rho A/L`.

Since `0<=x<=1/(Lv)`, the quadratic correction satisfies

`L integral_z^1 x^2/2 dv <= 1/(2A)`.

Consequently

`L J_(L,rho)(A/L) >= ln L-ln A-rho-1/(2A)`.

Let `w exp(w)=L exp(-rho)`. The same proof with `A=w-1/(2w)` gives the certified lower bound on the scalar fixed point whenever `w>=1`. The identity needed in that proof becomes `w+ln w=ln L-rho`; no other step changes.

For completeness, the scalar expansion is uniform over `0<rho<=1`. The generalized curve is at least the original `rho=1` curve at the same `L`, giving the earlier lower bound `alpha>=ln L-ln ln L-2`. At the fixed point, the linear and quadratic estimates give

`ln L-ln alpha-rho-1/(2alpha) <= alpha`

and

`alpha <= ln L-ln alpha-rho+rho alpha/L`.

These imply `alpha/ln L->1` and then

`alpha=ln L-ln ln L-rho+o(1)`

uniformly in `rho`. The cubic-remainder argument also works uniformly and yields `alpha=w-1/(2w)+O(w^-2)` for the generalized `w`.

Now choose

`L_0=1+ln(d-1)`, `M=(d-1)L_0`.

Then `L=L_0+ln L_0` and `rho=1/L_0`. Therefore

`alpha=ln L_0-ln ln L_0+o(1)`.

To express the ratio with numerator `L_0`, rewrite `L/alpha=L_0/[alpha L_0/L]`. The denominator adjustment is only

`alpha-alpha L_0/L=O((ln L_0)^2/L_0)=o(1)`.

Hence this choice proves

`R(d) <= L_0/[ln L_0-ln ln L_0+o(1)] + 2/c`.

The tuned cutoff therefore removes the constant `-1` from the previous denominator. This is a stronger upper certificate; it still does not prove a matching second-order lower bound for the true worst ratio.
