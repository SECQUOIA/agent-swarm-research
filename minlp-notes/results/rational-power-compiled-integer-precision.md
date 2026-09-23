# Rational pure-power graphs with near-minimum integer counts

Date: 2026-09-05. Status: independently reviewed theorem and rational construction.

For positive separable pure-power outputs with rational exponents greater than
one, a rational MILP can be constructed in polynomial input bit time whose
integer count is within `7r+1` of the minimum for arbitrary convex
mixed-integer lifts. Exponents are encoded in binary: construction size depends
polynomially on their bit lengths, not their numerical magnitudes.

## Main theorem

Consider rational data

```
f_j(x)=l_j^T x+b_j+sum_(i=1)^r c_ji x_i^(alpha_i),
x in [0,1]^r,     c_ji>=0,     alpha_i>1 rational.
```

Every coordinate is active; coordinates occurring only affinely can be kept
continuous. Let `K` be a compact convex unconditional error body containing
zero in its interior, with the rational strong-separation oracle and rational
inner/outer radius assumptions of the
[rational log-product allocation oracle](../notes/rational-log-product-convex-body-oracle.md).
Let `p_conv` denote the minimum integer dimension among arbitrary convex lifts
that contain the exact graph and admit only errors in `K`. Integer variables
in that comparison may be unrestricted, and continuous formulation size is
unrestricted.

There is a deterministic polynomial-time rational MILP construction, in the
input and oracle encoding, of polynomial total encoding length satisfying

```
p_out<=p_conv+7r+1.
```

If every `alpha_i>=2`, the sharper bound is
`p_out<=p_conv+(13r/2)+1`. The whole graph is contained, and every admitted
output error belongs to `K`. The result does not assert that the MILP is
polynomial-time solvable or that its continuous relaxation is ideal.

The construction computes interpolation knots from cell-index bits. Internal
Boolean-circuit wires and products use continuous variables forced by those
bits. Certified rational logarithm and exponential series compute the inverse
power knots with polynomial bit cost. Circuit compilation and interpolation
are established tools; the contribution under investigation is the resulting
sparse rational-power whole-formulation guarantee.

Both [the first full audit](../notes/review-compiled-rational-knot-formulations.md)
and [the second full audit](../notes/review-compiled-rational-knot-formulations-second.md)
passed, including the final `alpha_i>1` scope. A separate
[bit-conditioning audit](../notes/review-compiled-rational-knots-bit-conditioning.md)
checks the sparse integer-exponent primitive. The
[bounded source audit](../notes/compiled-rational-knot-formulations-novelty.md)
found no matching complete count guarantee among the sources checked;
publication priority remains unestablished.

The proof first establishes the indexed-knot formulation and a direct
integer-exponent primitive. It then proves the `alpha>=2` case and extends
it to every rational `alpha>1` using a scaled curvature estimate.

## 1. A circuit representation of rational knot interpolation

Fix rational instance data and a nonnegative integer `L`. Suppose a deterministic
algorithm, given an `L`-bit index `k in {0,...,2^L-1}`, returns dyadic vectors
`a_k,b_k in [0,1]^d`, with a common prescribed output precision `B`. Assume its
running time is bounded by a polynomial in the instance encoding, `L`, and `B`.

There is a rational mixed-integer linear formulation for

```
u=(1-theta)a_k+theta b_k,   0<=theta<=1,
```

using exactly `L` declared binary variables, with polynomial total size and
polynomial construction time in those parameters. This assertion concerns the
integer-feasible set; it makes no claim that the continuous relaxation is ideal.

To prove it, unroll the bounded deterministic computation into a Boolean circuit
of polynomial size. The instance data are constants; only the `L` index bits are
inputs. Use AND and NOT gates, introducing every internal and output wire as a
continuous variable in `[0,1]`. A NOT gate is `v=1-u`. An AND gate is

```
0<=v,  v<=u_1,  v<=u_2,  v>=u_1+u_2-1.
```

Induction through the acyclic circuit proves that integral input bits force
every wire to its exact Boolean value. Each dyadic output coordinate is a linear
combination of its output bits, with coefficient encoding length `O(B)`.
For each output bit `v`, the product `theta v` is represented exactly by

```
0<=t,  t<=theta,  t<=v,  t>=theta+v-1.
```

Linear combinations of these products give the interpolation equation. No wire
or product variable needs a separate integrality declaration. Multiple knot
coordinates or other computed quantities can share the same input bits.

In particular, a huge list of knots need not be explicitly enumerated. What is
needed is a polynomial-time algorithm for the requested indexed knots, not a
polynomial-time algorithm that enumerates the entire list.

## 2. Certified inverse-power knots with binary exponents

Let `D>=2` be an integer supplied in binary, `L>=1`, and `0<delta<1/2` rational.
For any integer `k in {0,...,2^L}`, put

```
t=k/2^L,     u=t^2,     g(t)=t^(2/D).
```

There is a deterministic algorithm producing a dyadic `R_k in [0,1]` with

```
R_0=0,  R_(2^L)=1,  |R_k-g(k/2^L)|<=delta,
```

in time polynomial in `L`, `log D`, and the encoding of `delta`. Its output
precision and all intermediate bit lengths have the same polynomial bound.
It does not require deciding exact equality between a large power and a
rational target.

For an interior index, `u>=2^(-2L)`. Choose

```
tau=delta*2^(-2L)/16,
R=ceil(log2(2/delta)),
P>=max(R+1, ceil(log2(D/tau))).
```

At a dyadic bisection point `s in [0,1]`, evaluate `s^D` by exponentiation by
squaring, rounding every multiplication downward to `P` fractional bits.
Denote the result by `A`. Then

```
0<=s^D-A<=D*2^(-P)<=tau.                         (1)
```

Here is a direct error proof. Every approximate factor stays in `[0,1]` and is
no greater than its exact value. If approximate powers of exponents `a,b>=1`
have errors at most `(a-1)2^(-P)` and `(b-1)2^(-P)`, multiplication and one
downward rounding give error at most `(a+b-1)2^(-P)`. The base `s` is exact
because `P` exceeds its dyadic precision. Induction over the squaring/product
computation proves the stronger bound `(D-1)2^(-P)`. Multiplication by an
initial exact accumulator one is handled without rounding error.

Use `[A,A+tau]` as a certified enclosure. If `A+tau<u`, the test point is
strictly below the desired root. If `A>u`, it is strictly above. Update the
root bracket accordingly. In the remaining case, `u in [A,A+tau]` and
`|s^D-u|<=tau`. Since `tau<=u/16`, both endpoint power values are at least
`u/2`. On the segment between `s` and `u^(1/D)`,

```
D z^(D-1)>=z^D>=u/2.
```

The mean value theorem then gives

```
|s-u^(1/D)|<=2tau/u<=delta/8.
```

Thus an uncertain comparison permits safe termination with output `s`. If no
uncertain comparison occurs, after `R` bisection steps the bracket width is at
most `delta/2`, so its midpoint is also a valid output. All outputs can be
represented with `R+1` fractional bits, padding earlier outputs with zeros.
The endpoints zero and one are handled separately and exactly.

There are `O(log(1/delta))` bisections and `O(log D)` rounded multiplications
per bisection, on `P=O(log D+L+log(1/delta))` bits. The target `u` has at most
`2L` fractional bits. Rational comparisons, branch decisions, and all arithmetic
therefore have polynomial bit cost. Early termination can be implemented by a
flag and fixed-length computation, as needed for circuit compilation.

## 3. The sparse pure-power graph gadget

Given rational `0<p<=1` and binary integer `D>=2`, choose

```
L=ceil[(1/2)log2(1/p)]+2,
h=2^(-L),
delta=p/(16D).
```

For an `L`-bit cell index `k`, the algorithm in Section 2 computes both `R_k`
and `R_(k+1)`. It also computes the exact dyadic values `(kh)^2` and
`((k+1)h)^2`, using ordinary binary integer multiplication. Apply Section 1 to
form, for a single continuous `theta in [0,1]`,

```
x=(1-theta)R_k+theta R_(k+1),
y=(1-theta)(kh)^2+theta((k+1)h)^2.                 (2)
```

This uses exactly `L` binaries. Its rational size and construction time are
polynomial in the encoding of `p` and `D`; in particular, they are polynomial
in `log D`, not the numerical exponent.

Let `g(t)=t^(2/D)` and introduce the comparison coordinate

```
x_0=(1-theta)g(kh)+theta g((k+1)h).
```

Then `|x-x_0|<=delta`. The uniform chord estimate is

```
0<=y-x_0^D<=4h^2.                                (3)
```

For completeness, on the first interval the error is
`h^2(theta-theta^D)<=h^2`. On another interval write `a=kh>=h`, `b=a+h`,
and `alpha=2/D<=1`. The input interval length is at most
`alpha a^(alpha-1)h`. The maximum second derivative of the power is
`D(D-1)b^(2-2alpha)`. The standard chord bound `M(length)^2/8` gives at most

```
[(D-1)/(2D)] (b/a)^(2-2alpha)h^2 <=2h^2,
```

which implies the stated safe bound (3). Both `x,x_0` lie in `[0,1]`; the power
is `D`-Lipschitz there. Consequently

```
-D delta<=y-x^D<=4h^2+D delta.
```

Introduce the graph output `q` through the rational band

```
y-(4h^2+D delta)<=q<=y+D delta.                    (4)
```

Every exact graph point is admitted. Indeed, the sequence of segments in
(2) forms a continuous polygonal path from `R_0=0` to `R_(2^L)=1`, so its
input projection covers `[0,1]`. Monotonicity of the approximate knot sequence
is unnecessary. At a selected segment, the displayed error bound places
`q=x^D` in (4). Conversely, every admitted point satisfies

```
|q-x^D|<=4h^2+2D delta<=3p/8.                     (5)
```

Possible reversed or duplicate knot segments therefore cause no problem:
all their points obey the same error bound and their union still covers the
domain. The two computations for a shared endpoint use the same deterministic
algorithm, ensuring the polygonal path joins exactly.

## 4. Whole-system consequence with sparse binary degrees

Consider rational positive pure-power outputs

```
f_j(x)=l_j^T x+b_j+sum_(i=1)^r c_ji x_i^(D_i),
x in [0,1]^r,     c_ji>=0,     D_i>=2,
```

with each exponent supplied in binary and all coordinates active. Let the
unconditional error body `K` satisfy the rational strong-separation and radius
assumptions of the existing allocation theorem. Define

```
D_alloc=max{product_i p_i: 0<=p_i<=1, Cp in K},
Phi=-(1/2)log2 D_alloc.
```

The reviewed allocation algorithm supplies a positive rational feasible `p`
with product at least `exp(-1)D_alloc`, in polynomial oracle bit time and with
polynomial output encoding. Apply (2)--(4) to each coordinate and set
`w_j=l_j^T x+b_j+sum_i c_ji q_i`. Equation (5) and unconditionality give the
whole-graph error guarantee, and choosing each `q_i=x_i^(D_i)` proves exact
graph containment.

The binary count is unchanged from the dense pure-power theorem:

```
p_out<=Phi+3r+1/(2ln 2)
      <=p_conv+(13r/2)+1.                         (6)
```

The second inequality imports its reviewed degree-independent parity-volume
lower bound `p_conv>=Phi-A_r`, with `A_r<7r/2`. The construction itself is
polynomial in the sparse rational input and oracle encoding, including
`sum_i log D_i`. The degree lower bound applies to these finite exponents
without an encoding restriction. Thus (6), removes
the dense-degree restriction on compact pure-power near-minimal precision.

## 5. Attribution and open scope

The positive rational Stieltjes construction remains a distinct explicit
algebraic formulation; this circuit construction does not invalidate it.
The gain is sparse binary exponent complexity, not a better
integer-count constant. It does not yet extend the additive `O(r)` comparison
to arbitrary positive mixtures of many powers of one coordinate.

The [bounded source audit](../notes/compiled-rational-knot-formulations-novelty.md)
identifies direct antecedents:
[Avis–Bremner–Tiwary–Watanabe, *Polynomial size linear programs for problems in P*](https://arxiv.org/pdf/1408.0807),
Section 3, Lemma 1, and
[Avis–Bremner, *Sparktope*](https://arxiv.org/pdf/2005.02853), Sections 2–4,
explicitly compile computations into linear constraints with continuous
internal state. The former credits Valiant's earlier construction.
[Filos-Ratsikas–Hansen–Høgh–Hollender, *PPAD-membership for Problems with Exact Rational Solutions*](https://www.pure.ed.ac.uk/ws/portalfiles/portal/413786593/PPAD-Membership_FILOS-RATSIKAS_DOA08022024_AFV_CC_BY.pdf),
Section 3.4, also interpolates outputs of Boolean circuits using products of
output bits and a continuous interpolation coordinate, in its distinct
piecewise-linear pseudo-circuit model. The generic compiler and interpolation
mechanism therefore are supporting tools, not independent priority claims.
Also, [Adams–Henry, *Base-2 Expansions for Linearizing Products of Functions of Discrete Variables*](https://www.osti.gov/servlets/purl/1648449),
Section 2, already represents arbitrary values on a finite index set and their
products with a continuous interpolation weight using only the original
index binaries. Its general construction has size linear in the number of
indices. The circuit method supplies polynomial size in the index bit length
for the computable knot family used here. The source audit records this
distinction explicitly.
The source audit found no matching sparse-exponent whole-formulation count
guarantee among the checked sources; publication priority remains unestablished.

## 6. Rational exponents through elementary rational series

The whole-system consequence extends further to exponents `alpha_i>=2` that
are rational numbers supplied in binary. This strengthening has passed both independent full reviews. It uses the same geometric proof and binary count, with a
different polynomial-time inverse-knot algorithm. The integer-exponent
algorithm above remains a simpler option for integer data.

Let `alpha>=2` be rational, `beta=2/alpha in (0,1]`, and
`t=k/2^L`, with `0<=k<=2^L`. Given rational `0<delta<1/2`, a dyadic
approximation to `t^beta` with absolute error at most `delta` can be computed
in time polynomial in `L`, the encoding of `alpha`, and the encoding of
`delta`, with polynomial intermediate and output bit lengths.

Handle `k=0` and `k=2^L` exactly. Otherwise find an integer `1<=e<=L` such
that `v=2^e t in [1,2)`. For `w in [1,2]`, define

```
z(w)=(w-1)/(w+1) in [0,1/3],
H_N(w)=2 sum_(j=0)^(N-1) z(w)^(2j+1)/(2j+1).
```

The elementary logarithm series gives

```
0<=log(w)-H_N(w)<=3*9^(-N).                       (7)
```

This bound follows by dropping the odd denominators in the positive tail
and summing a geometric series. The series identity itself follows by
integrating the geometric series for `2/(1-z^2)` on `[0,1/3]`.

Choose `N` with `3(L+1)9^(-N)<=delta/8`, and compute the rational number

```
A=beta[H_N(v)-e H_N(2)].
```

Because every term of `H_N` increases with its argument and `v<2`, we have
`-L<=A<=0`. Also `a=beta log t` lies in `[-L,0]`, and (7) gives
`|A-a|<=delta/8`. All sums and powers here may be computed exactly as
rational numbers: there are only `O(log(L+1)+log(1/delta))` terms, of
polynomial degree in a rational argument of polynomial bit length.

Let `M` be the smallest power of two with `M>=2L`, so `M<4L`. Then
`q=A/M in [-1/2,0]`. Choose an odd integer `J>=1` large enough that
`2^(-(J+1))<=delta/(16M)` and put

```
P_J(q)=sum_(j=0)^J q^j/j!.
```

The alternating-series estimate gives

```
1/2<=P_J(q)<=exp(q)<=1,
0<=exp(q)-P_J(q)<=2^(-(J+1))<=delta/(16M).
```

The first lower bound also follows by grouping successive terms after
`1+q`: for odd `J`, each remaining even/odd pair is nonnegative.
Since the `M`-th power is `M`-Lipschitz on `[0,1]`,

```
|P_J(q)^M-exp(A)|<=delta/16.
```

Moreover, the exponential is one-Lipschitz on the nonpositive real axis,
so `|exp(A)-t^beta|<=delta/8`. Compute `P_J(q)^M` exactly by squaring and
round it downward to a dyadic grid of width at most `delta/4`. The final
error is at most `7delta/16<delta`, and the output stays in `[0,1]`.

This procedure has polynomial bit cost without a black-box elementary-function
oracle. Exact rational series evaluation gives polynomial numerator and
denominator bit lengths. The final exponentiation multiplies these bit
lengths by at most `M<4L`, which is still polynomial. The integers `N,J`
are `O(log(L+1)+log(1/delta))`, and normalization and rational comparisons
are elementary polynomial-time operations. All output fractions are padded
to one fixed dyadic precision. Endpoints are exact, as before.

To apply this to the graph `x^alpha`, use

```
L=ceil[(1/2)log2(1/p)]+2,
delta=p/(16alpha),
g(t)=t^(2/alpha).
```

The chord proof in Section 3 uses only the real inequality `alpha>=2`:
replace `D` by `alpha` and its parameter `2/D` by `2/alpha`. Its curvature
estimate and the `alpha`-Lipschitz bound remain valid, including at zero.
The same output band has error at most `3p/8`. The coordinate change in
the imported lower bound is `x -> x^(alpha/2)`, a convex increasing
homeomorphism, so its proof also has no integrality requirement on the
exponents.

Therefore the whole-system theorem is:

> For rational positive pure-power systems with rational exponents
> `alpha_i>=2` encoded in binary, and under the stated rational allocation
> oracle assumptions, a rational MILP can be constructed in polynomial
> input/oracle bit time and polynomial total encoding length, with
> `p_out<=p_conv+(13r/2)+1`.

The exponent-dependent polynomial size is in the bit encoding of the rational
exponents. This claim concerns whole-graph approximation and retains the
unrestricted convex-lift comparison. The logarithm and exponential series,
the circuit compiler, and circuit-output interpolation are supporting
classical tools; the proposed consequence is this sparse rational-power
near-minimal precision guarantee.

## 7. Every rational exponent strictly greater than one

The final extension covers `alpha_i>1`, including powers between
one and two. Define the rational curvature scale

```
s_i=min(1,alpha_i-1),
C_eff,ji=c_ji s_i,
D_eff=max{product_i p_i: 0<=p_i<=1, C_eff p in K},
Phi_eff=-(1/2)log2 D_eff.
```

The resulting theorem is a polynomial-time rational construction satisfying

```
p_out<=p_conv+7r+1,                              (8)
```

with polynomial total encoding length in the binary rational exponents and
the other stated input/oracle data. The sharper `(13r/2)+1` bound remains
available when every exponent is at least two.

### Scaled Jensen inequality

For every `alpha>1`, `s=min(1,alpha-1)`, and `0<=a<=b<=1`,

```
[a^alpha+b^alpha]/2-((a+b)/2)^alpha
 >=(s/8)(b^(alpha/2)-a^(alpha/2))^2.              (9)
```

For `alpha>=2`, the earlier square-of-a-convex-function inequality supplies
the stronger constant `1/4`. For `1<alpha<2` and `b>0`, the power has
second derivative at least `alpha(alpha-1)b^(alpha-2)` on `(a,b)`.
Subtracting the corresponding quadratic proves the Jensen lower bound
`alpha(alpha-1)b^(alpha-2)(b-a)^2/8`. This argument extends to `a=0` by
continuity. For `u=a/b`, the inequality `u^(alpha/2)>=u` gives

```
b^(alpha/2)-a^(alpha/2)
 <=b^(alpha/2-1)(b-a).
```

Combining these estimates, and using `alpha>=1`, proves (9). The case
`a=b=0` is immediate.

Apply (9) coordinatewise after the homeomorphism `t_i=x_i^(alpha_i/2)`.
On each transformed parity support, the nonnegative midpoint Jensen vector
belongs to `K`, and it componentwise dominates
`C_eff[(t-u)^2]/8`. Unconditionality and convexity of `K` permit taking
expectations over independent uniform points of a positive-volume support.
With covariance `Sigma`, this gives

```
C_eff diag(Sigma)/4 in K.
```

The allocation `p_i=Sigma_ii/4` obeys its caps since the support lies in the
unit cube. Hadamard's determinant inequality and the covariance-volume
bound then give

```
vol(support)<=2^r omega_r(r+2)^(r/2) sqrt(D_eff).
```

Closure, zero-volume supports, and coverage are handled exactly as in the
reviewed pure-power parity proof. Thus

```
p_conv>=Phi_eff-A'_r,
A'_r=r+log2[omega_r(r+2)^(r/2)]<4r.               (10)
```

No volume-preservation assertion about the coordinate change is needed.

### Scaled chord bound

Let `g(t)=t^(2/alpha)`, `h=2^(-L)`, and let `(x_0,y)` interpolate
`(g(a),a^2)` and `(g(a+h),(a+h)^2)`, where `a=kh`. Then

```
0<=y-x_0^alpha<=4s h^2.                          (11)
```

For `alpha>=2`, this is the previous bound with `s=1`. Suppose
`1<alpha<2`. On the first interval the error is
`h^2(theta-theta^alpha)`. The inequality `1-exp(-v)<=v` implies
`theta-theta^alpha<=s theta(-log theta)<=s/e`, including the endpoints by
continuity.

For another interval write `b=a+h<=2a` and `beta=2/alpha in (1,2)`.
The input interval length is at most `beta b^(beta-1)h`, and its maximum
curvature is `alpha(alpha-1)a^(2-2beta)`. The chord bound is therefore

```
[s/(2alpha)] (b/a)^(4/alpha-2)h^2<=2s h^2,
```

which implies (11).

### Rational construction and count

Use the same depths `L_i=ceil[(1/2)log2(1/p_i)]+2` but set
`delta_i=s_i p_i/(16alpha_i)`. The circuit computes inverse-power knots
within `delta_i`. The inverse-power algorithm of Section 6 extends from
`beta<=1` to `beta=2/alpha<2` with just these changes:

```
6(L+1)9^(-N)<=delta/8,
-2L<=A<=0,
M is a power of two with 4L<=M<8L.
```

All remaining series estimates and the final `7delta/16` error bound are
unchanged. In particular `A/M in [-1/2,0]`, and exact rational squaring
still increases bit lengths only by `M=O(L)`. The scale `s` and tolerance
`delta` have polynomial rational encoding even when `alpha` is close to
one; dependence on their small magnitudes is through their bit lengths.

Replace the output band (4) by

```
y-(4s h^2+alpha delta)<=q<=y+alpha delta.
```

The scaled chord bound, Lipschitz estimate, and endpoint path coverage prove
exact graph containment and error at most
`4s h^2+2alpha delta<=3s p/8`. Apply the rational allocation oracle to
`C_eff` and assemble the positive outputs as before. The total binary count
is at most `Phi_eff+3r+1/(2ln2)`. Combining with (10) proves (8).

This extension concerns convex pure powers with exponents strictly greater
than one. Affine powers can be removed from the active-coordinate list.
Concave powers below one and arbitrary positive mixtures are not covered by
this statement.

## Supporting verification

The exact-rational implementation
[check_compiled_power_knots.py](../code/quadratic_rank/check_compiled_power_knots.py)
passed 1,479 exact rounded-power error checks, 60 integer inverse checks,
48 rational-exponent inverse checks, and 1,158 scaled Jensen/chord checks.
The numerical checks use 300-digit reference arithmetic and include exponents
larger than `10^34` and an exponent within `10^(-30)` of one. Reference
precision was increased to control amplified roundoff in high-power endpoint
identities. These checks support signs, branch conventions, and endpoint
handling; they do not replace the uniform analytic proofs or independent
reviews. The compiled MILP circuit itself is established constructively by
Section 1, rather than generated by this numerical checker.
