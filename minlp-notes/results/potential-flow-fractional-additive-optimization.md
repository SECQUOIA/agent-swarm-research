# High-precision optimization with fractional flow laws

Date: 2026-09-05. Status: two independent proof and bit-complexity reviews passed: [first](../notes/review-potential-flow-fractional-additive.md), [second](../notes/review-potential-flow-fractional-additive-second.md). The approximation ingredients are established prior work; the [source audit](../notes/potential-flow-fractional-law-approximation-sources.md) identifies their precise scope. The result combines those ingredients with the new bounded-block-rank nomination theorem and fixed-core optimization method. No matching combined network theorem was found in the bounded source check; this is not an exhaustive novelty certificate.

The result provides polynomial-time additive optimization even though exact arc comparison for the common exponent `3/2` has a [Square-Root-Sum arithmetic barrier](../notes/potential-flow-fractional-power-arc-barrier.md) on one cycle. It does not resolve that exact comparison problem.

## 1. Theorem and scope

Fix a maximum cycle rank `r` per biconnected block and a finite family of rational exponents in `(1,3)`. On each edge choose an exponent `q_e` from this family and impose

```
pi_u-pi_v = beta_e sign(x_e)|x_e|^(q_e).
```

The graph is connected. Nomination intervals are finite rational intervals, arbitrarily shifted, with a nonempty intersection with the exact balance equation. Resistances vary independently in positive finite rational intervals, which may be singletons.

**Theorem.** One can compute a certified additive optimum-value interval and rational feasible near-optimal nomination/resistance inputs for any terminal potential difference, in time polynomial in rational input size and requested precision bits. The same guarantee holds for maximum and minimum signed flow on any edge. The polynomial exponent and constants may depend on `r` and the fixed exponent family. No additional flow or pressure restrictions enter these physical-extremum problems. Exact pressure or edge-flow threshold comparison is not claimed, and exact rational physical-state witnesses are not claimed.

The fixed-exponent scope includes `q=1.852=463/250`, a water-network head-loss exponent used in [Klimm, Pfetsch, Raber, and Skutella, On the robustness of potential-based flow networks](https://link.springer.com/article/10.1007/s10107-021-01760-w). The theorem concerns the stated stationary passive law and its uncertainty sets.

The proof is first given for the common exponent `3/2`; the final section verifies the fixed finite heterogeneous extension. The exponent family is fixed in the complexity statement. Arbitrary binary-encoded exponent input, uncertain exponents, and uncertain topology are outside its scope. This is a bit-complexity result with potentially large parameter-dependent exponents, rather than a practical runtime or fixed-parameter tractability claim.

Handle an edgeless connected graph or `B=0` directly: its objective and all physical flows are zero. The formulas below concern `m>0` and `B>0`.

The route has three parts: construct increasing rational approximants with polynomial degree and coefficient bits; extend the fixed-core local optimizer to rational laws by clearing positive denominators; and bound physical-flow changes from uniform constitutive errors.

## 2. Positive rational approximation without a transcendental normalization

For `0<alpha<1`, define

```
I_alpha(t)=integral_0^infinity [t s^(alpha-1)/(t+s)] ds,   t>=0.
```

Substitution `s=t u` gives `I_alpha(t)=t^alpha I_alpha(1)` for `t>0`, with the identity also valid at zero. Thus no evaluation of `sin(pi alpha)/pi` is required if a quadrature is normalized at `t=1`.

Fix `alpha=1/4` and consider `0<=t<=1`. Truncate the integral to `[2^(-L),2^L]`. Its lower and upper tails are bounded by

```
4*2^(-L/4),   (4/3)*2^(-3L/4),
```

respectively. Split this interval into dyadic panels `[2^k,2^(k+1)]`, `k=-L,...,L-1`, substitute `s=2^k u`, and use the positive `n`-point Gauss-Legendre rule on `u in [1,2]`. This gives

```
Q(t)=sum_(k,j) w_j 2^(k alpha) u_j^(alpha-1)
                     * t/(t+2^k u_j).
```

Every node and weight is positive. Consequently `Q(t)` is increasing, vanishes at zero, and is a positive sum of terms `a t/(t+s)`.

An elementary quadrature error bound is uniform in `t`. On the complex disk `|u-3/2|<=1`, the panel integrand

```
F_k,t(u)=2^(k alpha) u^(alpha-1) t/(t+2^k u)
```

is analytic and has modulus at most `2*2^(k alpha)`: the disk has real part at least `1/2`, the principal power is analytic there, and the last ratio has modulus at most one. The Taylor polynomial at `3/2` through degree `2n-1` therefore has uniform error at most `4*2^(k alpha)*2^(-2n)` on `[1,2]`. The Gauss rule is exact on this Taylor polynomial; positivity and weights summing to one imply its integration error is at most twice that uniform error. Summing panels gives the safe bound

```
|I_alpha(t)-Q(t)|
 <= 4*2^(-L/4)+(4/3)*2^(-3L/4)
       +16 L*2^(L-2n).                         (A)
```

Taking `L=O(p)` and `n=O(p+log L)` makes (A) at most `2^(-p)`, with `2Ln=O(p^2)` positive rational-fraction terms before coefficient rounding.

The Gauss nodes and weights are real algebraic numbers of polynomial encoding length and can be approximated to prescribed rational intervals in polynomial bit time: isolate roots of the degree-`n` rational Legendre polynomial and evaluate the standard positive weight formula. The fixed rational powers in the weights are algebraic and likewise approximable. Nodes satisfy `u_j in(1,2)`, and all dyadic scales have `O(L)` bits. Round the positive nodes `s=2^k u_j` and weights `a=w_j 2^(k alpha)u_j^(alpha-1)` upward to positive dyadic rationals from rigorous enclosures at the stated absolute precision. This preserves even very small positive weights without requiring a uniform positive lower weight bound. A crude uniform sensitivity bound suffices:

```
|partial[a t/(t+s)]/partial a|<=1,
|partial[a t/(t+s)]/partial s|<=a/s
```

for `t>=0,s>0`. Lower bounds `s>=2^(-L)` before rounding, safe magnitude bounds `a<=2^(L+2)`, and a factor of two margin after rounding show that `O(p+L+log(Ln))` coefficient precision bits preserve uniform error `O(2^(-p))`. Therefore the rounded rational sum `Q_R` has polynomial encoding length, positive coefficients, and the same qualitative properties.

Finally normalize `R(t)=Q_R(t)/Q_R(1)`. The denominator is a positive rational number. Since `I_alpha(1)>=1/6` by integrating on `[1,2]`, an approximation error at most `1/12` gives `Q_R(1)>=1/12`. For an absolute quadrature-plus-rounding error `zeta<=1/12`,

```
|R(t)-t^alpha|<=24 zeta,     0<=t<=1.           (B)
```

The integral representation and positive quadrature are standard ingredients. The specific elementary bounds above and the rational normalization are included to make the bit model explicit, and were checked in both independent proof reviews.

## 3. An increasing rational constitutive law

Let `B=sum_v max(|l_v|,|u_v|)` and choose a rational power of four `T>=max(1,B)`. Its positive square root `S` is rational. Set

```
psi(x)=S*x*R(x^2/T^2).
```

By (B), `|psi(x)-phi(x)|<=24 S B zeta` for `|x|<=B`. Each term is a positive multiple of `x^3/(x^2+c)` with `c>0`, whose derivative is

```
x^2*(x^2+3c)/(x^2+c)^2 >=0.
```

The sum is strictly increasing, vanishes at zero, is smooth, and is unbounded in both directions. Its denominator is a product of positive quadratics. Its rational coefficients, dense numerator/denominator degrees, and expanded encoding lengths are polynomial in input size and `log(1/zeta)`. Thus arbitrary constitutive accuracy `delta` needs only polynomial degree and coefficient bits. Polynomial-degree approximants without rational denominators would not establish this claim near the fractional-power singularity.

## 4. Rational-law local optimization

The nomination face theorem uses only strict monotonicity and its analytical smoothing argument, so it applies to `psi`. After face selection, each local flow is affine in the fixed-dimensional core. The denominator of every substituted `psi(x_e(z))` is strictly positive for real core values. Multiply each cycle equation by the product of these denominators, obtaining polynomial equations linear in the resistance leaves. The resulting degree is polynomial in graph size and approximant degree. In fixed core dimension, expansion has polynomial monomial count and coefficient bit length.

For a potential-difference objective, introduce its value `v` as one additional core coordinate and impose the denominator-cleared equality between `v` and the linear-in-resistances rational potential sum. Minimize or maximize the core coordinate `v`. This adds one aggregate equation and one core variable, both fixed increases. Rational bounds on `v` follow from the acyclic flow bound and explicit numerator/denominator bounds. The dense-degree fixed-core theorem gives exact local algebraic optimization. Inactive-block values are approximated separately before summation, as in the polynomial-law theorem.

Rational near-optimal input recovery uses the same electrical Lipschitz estimates, now with rational bounds for `psi` and `psi'` on `[-B,B]`. Positive denominator factors have explicit rational lower bounds, so these bounds have polynomial bit length even if numerically large. A simpler derivative bound is also available: for the normalized positive weights `a_j` in `R`, each derivative factor `z(z+3)/(z+1)^2` is at most `9/8`, so `psi'(x)<=9*S*sum_j a_j/8` on the whole line. No exact rational physical flow is claimed.

## 5. Physical error from constitutive error

Fix any feasible nominations and resistance vector, and let `x` be its original physical flow and `y` its rational-approximant flow. Both have absolute coordinates bounded by `B`. Their difference is a circulation. Taking its scalar product with the difference of physical potential gradients gives

```
sum_e beta_e [phi(x_e)-phi(y_e)](x_e-y_e)
 =sum_e beta_e [psi(y_e)-phi(y_e)](x_e-y_e).
```

The signed power satisfies

```
[phi(a)-phi(b)](a-b) >= (1/2)*|a-b|^(5/2).
```

The sharp constant is larger, but the displayed rational constant suffices. Let `beta_L=min_e beta_lower_e`, `beta_U=max_e beta_upper_e`, and `m=|E|`. If `|psi-phi|<=delta` on the flow interval, then with `D=||x-y||_infinity`,

```
(beta_L/2)*D^(5/2) <= beta_U*delta*m*D,
D <= [2*m*beta_U*delta/beta_L]^(2/3).          (C)
```

The zero-difference case is immediate. To ensure `D<=eta<=1`, the rational choice

```
delta <= beta_L*eta^2/(2*m*beta_U)
```

is sufficient. The original law has derivative at most `2*max(1,B)` on this interval. Thus every terminal potential difference changes by at most

```
m*beta_U*[2*max(1,B)*eta+delta].              (D)
```

These estimates hold uniformly over the whole nomination/resistance uncertainty set. Choose `eta` and `delta` with polynomial encoding lengths so that (D) is at most a prescribed fraction of the requested additive tolerance. Optimize the rational surrogate to another fraction of that tolerance and return its rational inputs. The two uniform objective discrepancies and the surrogate optimization error give the desired original-law guarantee. Formula (C) similarly transfers approximate edge-flow extrema. The required law accuracy is a fixed power of the requested objective accuracy, so the rational approximation construction remains polynomial in precision bits.

## 6. Rational near-extremal edge-flow inputs

For edge-flow optimization, start from an exact algebraic optimizer of the rational-surrogate edge-flow objective. Do not substitute a pressure optimizer when resistances vary. Uniform estimate (C) places its original-law edge flow close to the original-law optimum. Its algebraic input coordinates can be rounded to rational feasible nominations and resistances without computing the possibly high-degree original physical state.

For the original law, let `D,D'` be the endpoint potential drops of an edge under two input vectors, with signed flows `x,y` and edge resistances `beta_e,gamma_e`. Put `M=2*max(1,B)`, `N=B*max(1,B)`. Scalar strong monotonicity and the endpoint equations imply

```
|x-y|^(3/2) <= (2/beta_lower_e)
              [|D-D'|+N*|beta_e-gamma_e|].
```

The original-law pressure adjoint bounds, obtained by adding a positive linear smoothing term, give

```
|D-D'| <= beta_upper_e*M*||b-c||_1
          +N*||beta-gamma||_1.
```

Thus input coordinate accuracy of a fixed power of the desired edge-flow error suffices. Recover nominations by rational LP inside small isolating boxes and balance; round resistances independently. All constants have polynomial rational encoding length. This yields rational near-extremal inputs for the original edge-flow problem as well as a certified additive extremum-value interval. The argument controls the original edge flow directly; it does not require a uniform inverse derivative bound for the surrogate near zero.

## Initial literature leads

[Bonito and Pasciak, Numerical Approximation of Fractional Powers of Elliptic Operators](https://arxiv.org/abs/1307.0888) study positive quadrature representations for fractional powers. [Bonito, Lei, and Pasciak, On Sinc Quadrature Approximations of Fractional Powers of Regularly Accretive Operators](https://arxiv.org/abs/1709.06619) give exponential sinc-quadrature error estimates. Those established approximation tools should be credited; no novelty is claimed for rational approximation of fractional powers itself. The network contribution is combining positive rational approximants, the bounded-block-rank nomination structure, and fixed-core algebraic optimization to obtain a network optimization bit-complexity theorem. The two proof audits are complete. The focused source audit confirms the approximation ingredients and keeps the network-combination novelty claim qualified.

## Reproducible evidence

[`fractional_rational_checks.py`](../code/potential_flow_mpd/fractional_rational_checks.py) builds four positive rational surrogates at nominal precision parameters 4, 8, 12, and 16, verifies sampled uniform errors against the analytical quadrature/normalization bound, and checks monotonicity across zero. It also checks the strong-monotonicity constant on 10,000 independently generated pairs, including opposite signs. The observed errors decrease from `2.20e-4` to `5.37e-8`; the largest observed error divided by its proven-form bound is `0.00156`. These are numerical mechanism checks, not certified coefficient-rounding or global-optimization implementations. The deliberately loose construction uses 3,072 to 12,096 fractions in these runs; the theorem is a bit-complexity claim rather than a practical runtime claim.

Run with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/fractional_rational_checks.py`.

A source reviewer independently identified a direct prior positive-approximation theorem in [Bonito and Pasciak (2013 preprint)](https://arxiv.org/abs/1307.0888), Section 3.3, equation (37), Lemma 3.4, and Remark 3.1 (PDF pages 14–15). Their uniform approximation of `lambda^(-beta)` for `lambda>=1` becomes a uniform approximation of `t^beta` on `(0,1]` under `lambda=1/t`, with positive terms proportional to `t/(t+s)` and a continuous extension equal to zero at `t=0`. Their Section 3.2 (PDF pages 10–13) also uses positive Gaussian quadrature on dyadic panels. Thus the approximation mechanism is explicitly prior work; the present contribution, as verified in the proof audits, is its application to the new network optimization structure with rational encoding and quantitative physical-error transfer.

For rigorous Gauss node/weight computation, a direct primary reference is [Johansson and Mezzarobba (2018)](https://marc.mezzarobba.net/ecrits/JohanssonMezzarobba_Legendre_v3_2018.pdf), DOI `10.1137/18M1170133`. The author PDF gives the positive weight formula on page 1, degree-`2n-1` exactness on page 2, polynomial bit complexity for arbitrary precision nodes and weights on page 3, and rigorous interval enclosures in Section 7.2. This supports the rational coefficient construction rather than requiring any nonconstructive existence of quadrature nodes.

## 7. A fixed finite family of rational exponents in `(1,3)`

The same proof covers any fixed rational `q in(1,3)`, or a fixed finite family of such exponents assigned to different edges. Both independent reviewers checked this extension. Put `alpha=(q-1)/2`. The dyadic integral tails become `2^(-alpha L)/alpha` and `2^(-(1-alpha)L)/(1-alpha)`. For a fixed exponent, both are exponentially small in `L`; the same disk bound and positive quadrature apply. Choose `T>=max(1,B)` to be a power of two whose exponent is divisible by the denominator of `q-1`, so `T^(q-1)` is rational. Use

```
psi_q(x)=T^(q-1)*x*R_alpha(x²/T²).
```

Its terms are still positive multiples of `x³/(x²+c)`, so strict increase and rational encoding are unchanged. The uniform error is at most `B*T^(q-1)` times the scalar approximation error.

For every `1<q<3`, signed-power strong monotonicity has the safe rational bound `1/4*|a-b|^(q+1)` after multiplication by `a-b`. The derivative is bounded on the flow interval by `M=3*max(1,B)²`; the law itself is bounded by `N=B*max(1,B)²`. In a heterogeneous fixed family, let `D` be the maximum flow-coordinate difference and select an edge achieving it, with exponent `q_e`. The same circulation identity gives

```
D^(q_e) <= 4*m*beta_U*delta/beta_L.
```

For `0<eta<=1`, choose `delta<=beta_L*eta³/(4*m*beta_U)`. If `D>eta`, then `D^(q_e)>eta³`: for `D<=1`, use `q_e<3`, and for `D>1` use positivity. This contradiction proves `D<=eta`. Pressure error and rational input recovery follow with the displayed `M,N` and the safe coefficient `1/4` in the inverse Hölder bound. All law-accuracy and input-rounding requirements are fixed powers of the desired tolerance, hence polynomial in precision bits.

The exponent or finite family must be fixed. If an exponent approaches one or three exponentially closely in its binary input encoding, the present dyadic truncation bound can require exponentially many panels. No polynomial-time claim is made for arbitrary binary-encoded exponent input. The endpoint integer laws can be handled by their already-reviewed polynomial representations.

## Error-budget convention and dependencies

For a requested tolerance, choose the uniform original/surrogate objective discrepancy below one quarter of that tolerance, and run the surrogate optimization and rational-input recovery to an additional fraction of the tolerance. Enlarging the certified surrogate-value interval by the uniform discrepancy gives the original-law value interval. For witnesses, account for the original-to-surrogate discrepancy at the original optimum and at the returned input separately. For edge objectives, use the original-law Hölder rounding estimate of Section 6. All required accuracy levels are fixed powers of the requested tolerance and have polynomial binary encoding length.

The structural and computational antecedents are the [bounded-block-rank nomination theorem](potential-flow-bounded-block-rank.md), [dense polynomial-law optimization extension](potential-flow-polynomial-law-uncertainty.md), and [fixed-core polyhedral-block theorem](fixed-core-block-polyhedral-optimization.md). Rational laws are used through the explicit positive-denominator reduction in Section 4. Independent-block algebraic values are approximated separately, so the proof never assumes that a common field for all block optima has polynomial degree.
