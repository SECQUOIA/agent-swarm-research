# Second review: compact pure-power reciprocal interpolation

Date: 2026-09-05. Reviewer: `constant_rank_review`.

**Status: PASS after the analytical dependency was supplied and audited.**
The formulation, error estimate, graph containment, integer count, and
polynomial rational construction pass. The full audit of approximation
lemma (A), including coefficient encoding and uniformity near zero, is
recorded below. No mathematical dependency remains conditional.

Reviewed:

- `notes/compact-pure-power-reciprocal-interpolation.md`.
- `notes/shared-prefix-rational-interpolation-gadget.md`.
- `notes/positive-rational-stieltjes-power-approximation.md`.

This review makes no publication-priority claim for interpolation,
reciprocal disaggregation, or the resulting theorem.

## Exact reciprocal interpolation uses no extra integers

For any selected binary prefix, `a` is a fixed grid endpoint in
`[0,1-h]`. The equations

```
(a+beta_k)v_k^- = 1-lambda,
(a+h+beta_k)v_k^+ = lambda
```

have unique solutions because every denominator is positive. Those
solutions are nonnegative and at most `1/beta_k`. Expanding `a` in its
binary digits makes each apparent bilinear term a sum of binary times
bounded continuous products. Their standard four inequalities are exact
on every integer-feasible point. The equation right sides are linear;
there is no unencoded product of `lambda` with another continuous variable.

The claimed expression for `x` is correct term by term:

```
1-beta_k(v_k^-+v_k^+)
 =(1-lambda)a/(a+beta_k)
   +lambda(a+h)/(a+h+beta_k).
```

Multiplying by `alpha_k` and summing gives the interpolated values of `R`.
Positive `alpha_k,beta_k` make `R` strictly increasing. With the exact
endpoints supplied by (A), its successive grid values cover the full
input interval through their line segments. Every `x in [0,1]` is thus
represented by some prefix and interpolation parameter, including both
global endpoints and all cell boundaries.

The two expressions `a^2=sum 2^(-ell)z_ell a` and
`a lambda=sum 2^(-ell)z_ell lambda` are also exact using bounded
continuous variables and the same bits. Consequently

```
y=a^2+2h a lambda+h^2 lambda
 =(1-lambda)a^2+lambda(a+h)^2
```

is imposed exactly. The formula uses `h^2 lambda`, not `h^2 lambda^2`;
this is the endpoint chord value that the proof requires. For `D=2`,
the separate equation `x=a+h lambda` is exact and needs no reciprocal
terms. The main construction always has `L>=2`.

## Error band and exact graph containment

Assuming (A), the interpolated exact inverse values define
`x_0=(1-lambda)g(a)+lambda g(a+h)` with `g(t)=t^(2/D)` and
`|x-x_0|<=delta`. Both coordinates belong to `[0,1]`. The previously
reviewed chord estimate applies between `g(a)` and `g(a+h)`: their
half-power coordinates differ by exactly `h`. Their endpoint function
values are `a^2` and `(a+h)^2`. Thus

```
0<=y-x_0^D<=4h^2.
```

The derivative bound for `x^D` on `[0,1]` is `D`, giving precisely

```
-D delta<=y-x^D<=4h^2+D delta.
```

This asymmetry is used correctly by the band
`y-(4h^2+D delta)<=q<=y+D delta`. For every original input represented
by a grid segment, `q=x^D` satisfies both inequalities. Conversely,
subtracting `x^D` from every possible band value gives absolute error
at most `4h^2+2D delta`.

With `L=ceil[(1/2)log2(1/p)]+2`, one has `4h^2<=p/4`.
With `delta=p/(16D)`, the other term is `p/8`. Therefore the bound
`|q-x^D|<=3p/8` is correct. The exact degree-two inverse satisfies
these same conservative bounds. All band endpoints use rational model
coefficients under (A).

Applying this argument independently to each active coordinate permits
every exact vector graph point simultaneously. The exact affine output
equations then give `|w-f(x)|<=(3/8)Cp`. Positive coefficients and
unconditional convexity place the admitted errors in `K`. There is no
need to represent the body itself by finitely many linear inequalities.

## Size, bit bounds, and integer count

For each coordinate, the construction uses `O((M+1)L)` rows and continuous
variables, and exactly its `L` prefix binaries. Assuming the total encoding
bound in (A), the coefficients `alpha_k,beta_k` and bounds `1/beta_k`
have polynomial encoding length. Exact reciprocation of a positive
rational does not increase its bit length beyond exchanging numerator
and denominator. The exact sums in the output equations, dyadic prefix
coefficients, and rational band widths also have polynomial encoding.

The rational allocation oracle gives positive feasible `p_i` with
polynomial encoding and product at least `exp(-1)D_alloc`. Therefore
`log(1/delta_i)=log(16D_i/p_i)` has polynomial magnitude in the full
input encoding. Lemma (A), audited below, has polynomial dependence on `D_i`
and this accuracy depth, so the total formulation construction is polynomial
for dense polynomial input. This does not assert polynomial complexity
in `log D_i` for sparse huge-degree input.

Summing the depths gives

```
p_out<=Phi+3r+1/(2 ln 2).
```

The reviewed pure-power lower bound has `p_conv>=Phi-A_r` with
`A_r<7r/2`. Hence the comparison
`p_out<=p_conv+(13r/2)+1` is correct. This step adds no hidden integer
variables or degree-dependent integer term.

## Broader rational endpoint gadget

The supporting gadget is correct for a supplied rational polynomial
denominator with the certified bound `Q(t)>=q_min>0` on `[0,1]`.
At a fixed binary prefix and endpoint `t=a+s h`, the exact recurrences
give `v_k=t^k v_0`. Its denominator equation becomes
`Q(t)v_0=theta`, so it uniquely gives `v_0=theta/Q(t)` and
`v_k=t^k theta/Q(t)`. All values lie in `[0,1/q_min]` for the two allowed
weights, and the numerator equation gives exactly `theta P(t)/Q(t)`.
Signs of the polynomial coefficients do not affect this reasoning.

I requested correction of the original `O(dL)` size expression, which
missed constant polynomials and an empty prefix. The author changed it
to `O((d+1)(L+1))`. With this correction, the size claim includes both
`d=0` and `L=0`, without affecting the main construction.

Exact endpoint values zero and one suffice for coverage even without
monotonicity: the continuous polygonal interpolant joins those endpoints,
so its range contains `[0,1]`. Retaining the original bound `0<=x<=1`
removes any portions outside that interval. A uniform approximation bound
on rational endpoint values transfers to their convex interpolation with
the same error. The gadget supplies neither an approximation algorithm
nor a denominator-certificate algorithm; both are correctly outside its
standalone statement.

## Supporting formulation checks

I inspected and reran
`code/quadratic_rank/check_pure_power_reciprocal_interpolation.py`.
All 3,348 exact chord checks through degree 32 and all 60 exact reciprocal,
endpoint-normalization, and shared-bit identities passed. These tests
verify the displayed algebra for their rational cases. They do not
verify uniform approximation lemma (A).

No defect remains in the formulation or supporting general rational
gadget after the size-bound correction. The analytical audit follows.

## Stieltjes approximation: tails and uniform quadrature

The unnormalized integral is finite for `0<gamma<1`, and the substitution
`s=t u` gives `I_gamma(t)=t^gamma I_gamma(1)` for positive `t`. Defining
the value at zero separately is consistent with this continuous limit.
Splitting at one gives the displayed integral bounds, including
`2<=I_gamma(1)<=D/2+3` for `gamma=2/D`, `D>=3`.

The chosen lower cutoff satisfies

```
2^(-L gamma)/gamma
 <=2^(-p-ell_D-8) D/2<=epsilon/512.
```

The upper cutoff uses `1-gamma>=1/3`, giving tail at most
`3 epsilon/256`. Their sum is `7 epsilon/512<epsilon/64`.
Both inequalities are uniform for all `t in [0,1]`, including zero.
The lower cutoff's dependence on `D` is essential and is explicitly
included in the size bound.

On the complex disk of radius one centered at `3/2`, the panel integrand
is analytic: the power uses the right-half-plane branch and its possible
pole is nonpositive. Its modulus bound is valid. The power factor has
modulus at most two. For `j<=0`, the remaining factors have product
modulus at most one. For `j>=0`, they have product modulus at most
`2*2^(-j(1-gamma))<=2`. Thus the uniform bound four holds even for
very negative panels, small positive `t`, and large `D`.

Cauchy's coefficient estimate then bounds the degree-`2m-1` Taylor
remainder on `[1,2]` by `8*4^(-m)`. Gaussian exactness through that
degree, together with positive weights summing to one, gives at most
twice this error for the panel integral. The note's choice of `m`
ensures `16N*4^(-m)<=epsilon/16` for the sum over all panels.

The positivity and exactness facts are established Gaussian quadrature
properties, also verified from the cited [DLMF section 3.5(v)](https://dlmf.nist.gov/3.5#v).
The note's polynomial-division and squared-cardinal-polynomial arguments
are sufficient for their use here. All Legendre nodes are simple and
inside the interval. The length-one interval weight formula has the
correct factor: it is half the usual `[-1,1]` weight.

Consequently the unrounded partial-fraction approximation has two-sided
error less than `5 epsilon/64`. Its one-sided upper bound at one is
even better: `Q(1)<=I_gamma(1)+epsilon/16`, because the omitted integral
tails are nonnegative. This justifies the stated `Q(t)<=D+4` used in
the rationalization step.

## Relative rationalization and exact normalization

If both coefficients of a positive term are perturbed by relative error
at most `tau<1/2`, its value for positive `t` changes by relative error
at most `4tau`. This follows from bounding its value ratio between
`(1-tau)/(1+tau)` and `(1+tau)/(1-tau)`. At zero both terms vanish.
Positivity allows these bounds to be summed using `Q(t)`, rather than
the potentially much larger sum of numerator coefficients.

Thus `tau=epsilon/[128(D+4)]` gives total perturbation at most
`epsilon/32`, and the total error is less than `7 epsilon/64<epsilon/8`.
The exact rational normalizer `Qhat(1)` is positive and at least `2-E`.
Dividing all numerators by it gives exact endpoints zero and one. The
displayed bound `2E/(2-E)<=epsilon<=delta` is valid for the chosen
`epsilon<=1/4`. This proves uniform accuracy on the entire closed
interval, with no excluded interval near zero.

## Certified coefficient construction has polynomial bit complexity

The coefficient bound `H_m=(m+1)(2m)!` for the Legendre polynomial is
conservative and sufficient; its logarithm is `O(m log m)`. It implies
`|P_m'|<=m H_m` on `[-1,1]`. From the weight formula and positivity,

```
(m H_m)^(-2)<=w_i<=1.
```

This gives the stated positive lower and upper bounds on every `A_ji`
and `B_ji`, all with polynomial logarithmic magnitude. It also directly
controls weight evaluation. In fact, `w_i<=1` implies
`(1-r_i^2)P_m'(r_i)^2>=1`; combining this with the derivative upper
bound gives `1-r_i^2>=(m H_m)^(-2)`. The denominator in the weight
formula is bounded away from zero, and the roots are separated from
the interval endpoints by an inverse-exponential-polynomial amount.
Coefficient bounds similarly control its derivative on that interval.
Rational interval refinement therefore computes weights to the necessary
relative precision in polynomial time.

For a specific primary justification of the root-isolation import, I
checked Sagraloff and Mehlhorn's [Theorems 2, 3 and 36](https://arxiv.org/pdf/1308.4088).
They give deterministic polynomial bit bounds for integer-polynomial
root isolation and refinement to prescribed binary accuracy. Clearing
denominators of the explicit square-free Legendre polynomial preserves
polynomial coefficient length. Their result therefore applies directly;
there is no need to place all nodes in a common algebraic number field.

The identity
`A_ji=(w_i/v_i)*(2^j v_i)^(2/D)` is correct. Computing its power via
the positive root of `z^D=(2^j v_i)^2` needs only polynomial-depth
rational intervals. Indeed, `2^j v_i` stays between `2^(-L)` and
`2^U`. The derivative of its `2/D` power on that range is at most
an exponential with polynomial exponent. Root bisection thus needs
only polynomially many additional input-precision bits. Rational test
powers have at most `D` times the test-point bit length, which is
polynomial in the dense degree parameter. Signed panel indices of size
`O(D(p+log D))` cause large magnitudes but only polynomial encoding.

The number of panels is `O(D(p+log D))`, and the Gaussian order is
`O(p+log D)`. Hence the stated term bound
`M=O(D(1+log(1/delta)+log D)^2)` follows. Every coefficient needs only
polynomially many bits. Summing the rational terms at one, normalizing,
and optionally combining denominators add bit lengths over polynomially
many factors, and therefore retain polynomial total encoding and running
time. All coefficients stay strictly positive.

I also inspected and reran `code/quadratic_rank/check_positive_rational_stieltjes.py`.
Its 5,776 positive rational terms and 62 sample points passed, with exact
endpoint normalization and worst sampled error/tolerance below `0.00044`.
The test computes Gaussian nodes numerically and is explicitly not the
certified root-isolation algorithm. The proof and checked root-refinement
import establish the uniform and bit-complexity guarantees.

The full analytical lemma (A) therefore passes independent audit. Combined
with the formulation audit above, it closes the polynomial rational
construction with `p_out<=p_conv+(13r/2)+1` for the stated pure-power,
dense-input, unconditional-error family. No unresolved mathematical or
encoding defect remains.
