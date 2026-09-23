# Independent audit: compact rational pure-power interpolation

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS for the combined construction, including its rational approximation dependency.** This review covers:

- [Compact reciprocal interpolation](compact-pure-power-reciprocal-interpolation.md).
- [Shared-prefix rational interpolation](shared-prefix-rational-interpolation-gadget.md).
- [Positive rational Stieltjes approximation](positive-rational-stieltjes-power-approximation.md).

The formulation was first checked conditionally on approximation lemma (A). The subsequently completed Stieltjes proof was independently read in full, closing that dependency. The result has polynomial construction time and size under the stated dense-degree rational input and strong-oracle assumptions. This audit does not certify novelty.

## Exact formulation and error

For fixed grid bits, `a` is a rational grid endpoint. The equations

```
(a+beta)v^- = 1-lambda,
(a+h+beta)v^+ = lambda
```

have unique solutions because their denominators are positive. The bounds `0<=v^-,v^+<=1/beta` contain those solutions. Expanding `a` into its bits leaves only binary-times-bounded-continuous products, whose four standard linear inequalities impose the products exactly at every binary assignment. No additional discrete variable is needed.

The constant term in

```
1-beta(v^-+v^+)
```

is correct: it equals `(1-lambda)a/(a+beta)+lambda(a+h)/(a+h+beta)`. Thus summing with the positive coefficients evaluates precisely the interpolation of the rational endpoint values. Positive coefficients imply strict monotonicity, and exact normalization gives endpoints zero and one. The resulting consecutive intervals cover every original `x` in the unit interval, including zero, one and shared cell boundaries.

The identities for `a^2` and `a lambda` also use only existing bits. Their bounded product formulations are exact even though `a` itself is defined from those same bits. With the same interpolation parameter, `y` is the chord interpolation of the squared transformed endpoints.

Let `x_0` interpolate the exact inverse-power endpoints. Uniform rational approximation gives `|x-x_0|<=delta`; positivity and endpoint normalization keep both coordinates in the unit interval. The previously independently reviewed chord estimate gives `0<=y-x_0^D<=4h^2`, and the derivative bound for `x^D` gives

```
-D delta <= y-x^D <= 4h^2+D delta.
```

The proposed band for `q` therefore contains `x^D` at every original `x`. For all admitted points, adding the two error intervals gives `|q-x^D|<=4h^2+2D delta`. With `L=ceil(.5 log2(1/p))+2` and `delta=p/(16D)`, this is at most `3p/8`. The separate exact inverse for `D=2` obeys the same safe bound.

Sharing the scalar `q_i` among outputs gives coordinatewise absolute error at most `(3/8)Cp`. The allocation is exactly feasible, and convex unconditional `K` is closed under this domination. This proves both graph containment and the uniform output-error guarantee.

The allocation oracle supplies product at least `exp(-1)D_alloc`. Therefore the binary count is at most `Phi+3r+1/(2 ln 2)`. Combining with the independently reviewed lower bound `p_conv>=Phi-A_r`, `A_r<7r/2`, gives `p_out<=p_conv+13r/2+1`. The same bound covers large tolerances and allocations with some `p_i=1`; the deliberately spare two bits on such coordinates are included in the additive constant.

Each reciprocal requires `O(L)` product rows and variables, so the formulation size is polynomial once the approximation representation has polynomial size and coefficient lengths. Bounds `1/beta_k` may be large in value, but their binary lengths remain polynomial.

## General rational endpoint gadget

For `t=a+s h`, induction in the recurrence gives `v_k=t^k v_0`. The denominator equation then forces `v_0=theta/Q(t)`. The supplied denominator lower bound proves all required variable bounds, independently of coefficient signs in `P` and `Q`. Conversely, the true values satisfy every row. Multiplying by the numerator coefficients gives the exact weighted rational endpoint value.

Endpoint normalization alone suffices for coverage even without monotonicity: the continuous piecewise-linear interpolant joins zero to one, so the intermediate value theorem applies. Retaining `0<=x<=1` removes any overshoot. The approximation comparison uses the same endpoint weights and remains valid on the retained segments.

I flagged the harmless boundary issue in the initial size expression `O(dL)`: constant functions or a zero-bit grid need a nonzero number of rows. The author corrected it to `O((d+1)(L+1))`. The main reciprocal construction already has positive degree and `L>=2`.

## Independent audit of the Stieltjes lemma

The substitution in the unnormalized integral is valid for `t>0`, while the separate definition at zero handles that endpoint exactly. Splitting at one gives the stated lower bound `I_gamma(1)>=2` and upper bound `D/2+3`. No trigonometric constant needs numerical evaluation.

With the prescribed truncation parameters, the lower tail is at most `epsilon/512` and the upper tail at most `3epsilon/256`; their sum is `7epsilon/512<epsilon/64`. These estimates remain uniform as `gamma=2/D` tends to zero. In particular, the lower cutoff has the required linear dependence on `D`.

On the complex disk centered at `3/2` with radius one, the real part is at least `1/2`. The principal power is analytic there and has modulus at most two. For nonpositive panel indices the remaining factor has modulus at most one. For nonnegative indices its bound is `2^(1-j(1-gamma))<=2`. Thus the claimed uniform disk bound four is valid. Taylor truncation at degree `2m-1` gives error `8*4^(-m)` on `[1,2]`; positive quadrature weights summing to one double this to panel error `16*4^(-m)`. The chosen `m` makes the sum at most `epsilon/16`.

Gaussian quadrature positivity and exactness through degree `2m-1` agree with the primary [NIST DLMF statement](https://dlmf.nist.gov/3.5#v). The candidate also supplies a direct polynomial-division and cardinal-polynomial proof, so its error estimate does not depend on an unquoted analytic quadrature theorem.

The bound `Q(1)<=I_gamma(1)+epsilon/16` is correct even though the absolute integral approximation error includes tails: the exact truncated integral is below the full integral, and only the quadrature error can increase it. Positive coefficients imply `Q(t)<=Q(1)<=D+4` throughout the interval.

Relative perturbations of both positive numerator and denominator coefficients by at most `tau` change each term by at most `4tau` times its original value. Summing positive terms gives uniform error at most `epsilon/32`. There is no factor involving the potentially very large sum of numerator coefficients. Together with the preceding errors, this gives `E<7epsilon/64<epsilon/8`.

The Legendre weight formula includes the correct factor for the interval of length one. The coefficient-sum bound `H_m=(m+1)(2m)!` yields `|P_m'|<=mH_m`, hence `w_i>=1/(mH_m)^2`; positivity and weight sum one give `w_i<=1`. The displayed bounds for every numerator and denominator coefficient then have logarithms polynomial in `L,U,m`.

Certified refinement of the roots of this degree-`m` rational polynomial takes polynomial bit time. The derivative-polynomial coefficient bounds also bound sensitivity of the weight denominator on the root interval. At the true root that denominator lies between one and `(mH_m)^2`, so interval refinement needs only polynomially many bits to obtain a positive enclosure and the required relative precision. This avoids an unstated assumption that the smallest Gaussian weight is numerically large.

The identity `A=(w/v)(2^j v)^(2/D)` reduces the only fractional power to a positive `D`th root of a bounded positive rational interval. Both the argument and its positive lower bound have polynomial binary length. Bisection with rational integer-power comparisons has polynomial bit cost in `D` and the requested precision. Worst-case conditioning can multiply the needed exponent length by `D`, which is still polynomial under the explicitly stated dense-degree model. Separate root intervals suffice; a common algebraic number field for all nodes is unnecessary.

Finally, rational normalization by `Qhat(1)>0` preserves positivity and fixes both endpoints exactly. The error estimate `2E/(2-E)<=epsilon` is valid since `I_gamma(1)>=2` and `epsilon<=1/4`. Summing and normalizing polynomially many polynomial-bit rationals keeps polynomial total encoding length. The term bound `M=O(D(1+log(1/delta)+log D)^2)` follows from the specified truncation and quadrature orders.

## Additional exact checks and limits

An independent exact rational checker verified **248 grid/interpolation cases**, including every grid endpoint index for depths one through five and interpolation weights zero, one-third, one-half and one. Each case checked both general rational endpoint recurrences using a denominator with a negative coefficient but certified positivity, numerator coefficients of mixed signs, and the exact quadratic chord identity. All checks passed. The earlier independent finite-power audit also checked 8,316 exact chord and Jensen cases through degree 100.

The construction does not claim polynomial time in the binary encoding length of an arbitrarily large sparse exponent. It applies to one common power per coordinate across outputs, nonnegative coefficients, and the stated unconditional output body. The analytic lemma itself does not establish a formulation result without the exact interpolation construction; both dependencies have been checked here.
