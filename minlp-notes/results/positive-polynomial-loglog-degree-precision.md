# Positive polynomial graph precision with double-logarithmic degree overhead

Date: 2026-09-05. Status: independently reviewed theorem and construction.

For positive separable polynomial outputs, a supporting scalarization of
the optimal allocation removes degree dependence from the covariance lower
bound. A dyadic partition near the endpoint controls all monomial curvatures
with only a double-logarithmic degree contribution to the binary count.
Both ingredients use the same allocation as the existing polynomial theorem.

## Statement

Consider rational dense polynomial input

```
f_j(x)=l_j^T x+b_j+sum_(i=1)^r sum_(k=2)^(D_i) c_jik x_i^k,
x in [0,1]^r,         c_jik>=0,         D_i>=2.
```

Every coordinate is active. Coordinates occurring only affinely can be
retained continuously as in the earlier exact quotient. Let `K subset R^m`
be a compact convex unconditional body containing zero in its interior.
For the constructive claim, assume a polynomial-time rational strong
separation oracle and known positive rational inner and outer radii.
Define

```
C_ji=sum_k c_jik,
D_alloc=max{product_i p_i: 0<=p_i<=1, Cp in K},
Phi=-(1/2)log2 D_alloc,
A_r=(r/2)+log2[omega_r(r+2)^(r/2)]<7r/2,
J_i=ceil(log2 D_i),
S_i=ceil(log2(J_i+1)).
```

For the whole-graph approximation minima of the previous results,

```
max(0,Phi-A_r)<=p_conv<=p_bin<=Phi+r+sum_i S_i.          (1)
```

The finite statement allows real data and unrestricted formulation size.
For rational dense input under the stated oracle assumptions, there is
a deterministic polynomial-time construction of a rational MILP with
polynomially many rows and variables and

```
p_out<=p_conv+(9r/2)+sum_i S_i+1.                       (2)
```

Thus the extra integer count is `O(r+sum_i log log(D_i+2))`. There is no
claim of polynomial dependence on the encoding of arbitrarily large sparse
exponents; the exact power recurrences use polynomial time in the numerical
degrees, as appropriate for dense input.

## A supporting scalarization preserves the allocation optimum

Let `p*` maximize `sum_i log p_i` under `0<p<=1` and `Cp in K`. A small
positive common allocation is strictly feasible. The maximizer is positive,
so ordinary convex first-order optimality and the normal-cone sum rule give
vectors `lambda in N_K(Cp*)` and `mu>=0` with

```
1/p_i*=(C^T lambda)_i+mu_i,
mu_i(p_i*-1)=0.                                       (3)
```

Here `N_K(z)={lambda:lambda^T(y-z)<=0 for all y in K}` is the outward
normal cone. The constraint qualification follows from the strictly
feasible common allocation; no smoothness or strict convexity of `K` is
needed.

The multiplier can be chosen nonnegative. For any positive coordinate of
`Cp*`, the unconditional body's downward closure implies that a normal
component is nonnegative, by decreasing that coordinate slightly. A zero
coordinate of `Cp*` corresponds to a zero row of `C`, since `C>=0` and
`p*>0`. Set the corresponding normal components to zero. This remains a
normal: unconditionality makes `h_K(lambda)=h_K(|lambda|)` monotone in
`|lambda|`, and removing those components leaves `lambda^T Cp*` unchanged.
It also leaves `C^T lambda` unchanged.

Put

```
A_i=(C^T lambda)_i>=0,
b=lambda^T Cp*=h_K(lambda)>=0.
```

The one-constraint allocation

```
max{product_i p_i: 0<=p_i<=1, A^T p<=b}                 (4)
```

has the same optimum `D_alloc`. Indeed, `p*` is feasible, and concavity
of the logarithm together with (3) gives, for any positive feasible `p`,

```
sum_i log p_i-sum_i log p_i*
 <=sum_i (p_i-p_i*)/p_i*
 =A^T(p-p*)+sum_i mu_i(p_i-p_i*) <=0.
```

Points with a zero coordinate have zero product and cannot improve it.
If `lambda=0`, (3) forces every `p_i*=1`, so `D_alloc=1` and the claimed
lower bound is trivial. More generally, an index with `A_i=0` has `p_i*=1`.
The multipliers are used only to prove a lower bound; the construction does
not need to compute them or represent them rationally.

## A degree-independent covariance lower bound

For each `i` with `A_i>0`, define the normalized positive polynomial

```
phi_i(x)=sum_k [(sum_j lambda_j c_jik)/A_i] x^k,
g_i(x)=sqrt(phi_i(x)).
```

The coefficients in `phi_i` are nonnegative and sum to one.
Consequently `g_i` is a strictly increasing continuous map of `[0,1]`
onto itself. It is convex: write it as the Euclidean norm of the vector
whose components are `sqrt(d_ik) x^(k/2)`; every component is nonnegative
and convex, and the Euclidean norm is convex and coordinatewise monotone
on the nonnegative orthant. For `A_i=0`, set `g_i(x)=x`.

For any nonnegative convex function `g`, the identity

```
(g(a)^2+g(b)^2)/2-g((a+b)/2)^2
 >=(g(a)-g(b))^2/4                                    (5)
```

follows from `g((a+b)/2)<=(g(a)+g(b))/2`. The scalarized nonlinear map is
`sum_i A_i phi_i(x_i)`, up to affine terms. For exact graph points in a
single parity support, its Jensen error is at most `h_K(lambda)=b`.
After the coordinatewise homeomorphism `t_i=g_i(x_i)`, (5) gives

```
(1/4)sum_i A_i(t_i-s_i)^2 <=lambda^T J(x,y)<=b.
```

For independent uniform points of a positive-volume transformed support,
with covariance `Sigma`, taking expectation yields
`(1/2)sum_i A_i Sigma_ii<=b`. Thus `p_i=Sigma_ii/2` is feasible for (4),
including its coordinate caps. Equality of the allocation optima implies
`product_i (Sigma_ii/2)<=D_alloc`. The standard covariance-volume bound
and Hadamard's inequality give

```
vol(transformed support)
 <=2^(r/2)omega_r(r+2)^(r/2)sqrt(D_alloc).
```

The transformed supports cover the unit cube. This proves the lower bound
in (1), independently of every degree. Zero-volume supports and closure
are handled as in the reviewed parity-volume proof. No assertion that the
coordinate homeomorphism preserves volume is used.

## Dyadic endpoint layers bound every normalized monomial curvature

For one coordinate with maximum degree `D`, put `J=ceil(log2 D)`. Partition
`[0,1]` into `J+1` intervals:

```
I_j=[1-2^(-j),1-2^(-j-1)],   j=0,...,J-1,
I_J=[1-2^(-J),1].
```

Write `I_j=[ell_j,ell_j+s_j]`, with positive rational length `s_j`.
For every power `x^k`, `2<=k<=D`, its second derivative in the normalized
local coordinate `u=(x-ell_j)/s_j` obeys

```
k(k-1)s_j^2 x^(k-2)<=2 on I_j.                         (6)
```

On the final interval, `s_J=2^(-J)<=1/D`, so the bound is at most one.
On any earlier interval, `s_j<=1/2` and `x<=1-s_j`. For `k=2`, the bound
is at most `2s_j^2<=1/2`. For `k>=3`, set `v=(k-2)s_j>=0`. Then

```
k(k-1)s_j^2(1-s_j)^(k-2)
 <=(v+1)^2 exp(-v)<=4/e<2.
```

The first inequality uses `ks_j=v+2s_j<=v+1`; the scalar maximum occurs
at `v=1`. Therefore every polynomial output has second derivative at most
`2C_ji` in that coordinate's normalized layer variable.

## Compact layer selection and exact shared powers

For each coordinate, choose a layer using
`S=ceil(log2(J+1))` binary variables. Give the `J+1` layers distinct binary
strings. Introduce continuous selectors `theta_j>=0`, `sum_j theta_j=1`,
and impose `theta_j<=z_b` for bits equal to one in the assigned string and
`theta_j<=1-z_b` for bits equal to zero. At any integer bit assignment,
only the matching selector can be nonzero, and it must equal one. Unused
binary strings are infeasible. Thus every `theta_j` is exactly zero or
one at integer-feasible points without being an additional integer
variable. Its products with bounded continuous variables are represented
exactly by the ordinary four binary-product inequalities.

For a positive allocation `p_i`, choose local grid depth

```
L_i=ceil[(1/2)log2(1/p_i)],       h_i=2^(-L_i).
```

Write the local normalized coordinate as `u=a_0+eta`, where `a_0` is its
`L_i`-bit prefix and `0<=eta<=h_i`. The original coordinate satisfies

```
a=sum_j theta_j(ell_j+s_j a_0),
rho=sum_j s_j theta_j eta,
x=a+rho.
```

The products here use only the prefix bits and the implied-binary selectors.
To compute exact powers of `a` and their residual products, use
`v_0=1`, `t_0=rho`, and `v_k=a v_(k-1)`, `t_k=a t_(k-1)` as in the previous
polynomial construction. A multiplication `a v` can be implemented by
first computing `a_0 v` with the prefix bits, and then writing

```
a v=sum_j [ell_j(theta_j v)+s_j(theta_j(a_0 v))].
```

Each selector product is exact at integer-feasible points. Bounds
`0<=v_k<=1`, `0<=t_k<=h_i` suffice, because `0<=a<=1` and `rho<=h_i`.
The same argument applies to both recurrences. Thus the construction uses
`O(D_i(L_i+J_i+1)+J_i S_i)` continuous variables and rows per coordinate,
with only `L_i+S_i` binaries. The interpretation also covers `L_i=0`:
then the prefix is identically zero and all associated products disappear.

All layer endpoints are dyadic rationals with `O(log D_i)` bits. The exact
power recurrences and coefficient sums have polynomial rational encoding
length for dense degree input.

## Error rectangle and final count

Let the exact prefix Taylor expression be

```
T_j(x)=l_j^T x+b_j+sum_i sum_k c_jik
                   [v_ik+k t_i,k-1].
```

The segment from `a_i` to `x_i` stays in its chosen layer, and its local
normalized residual is at most `h_i`. By (6) and nonnegative coefficients,

```
0<=f_j(x)-T_j(x)<=sum_i C_ji h_i^2<=(Cp)_j.
```

The rational rectangle `T_j<=w_j<=T_j+(Cp)_j` contains every exact graph
point and implies `|w-f(x)|<=Cp`. Unconditionality gives the required
whole-body error guarantee. The binary count is

```
sum_i (L_i+S_i)<=-(1/2)log2 product_i p_i+r+sum_i S_i.
```

An optimal allocation proves the finite upper bound in (1). The reviewed
rational log-product oracle returns a positive exactly feasible allocation
with product at least `exp(-1)D_alloc`. This adds at most `1/(2ln2)` to
the count. Combining with `A_r<7r/2` proves (2).

## Verification and novelty boundary

The normal-cone multiplier argument, convexity of Euclidean norms of
nonnegative convex functions, dyadic partitions, and exact binary-product
linearizations are established tools. The proposed result is their combined
whole-formulation guarantee with the stated degree dependence. The [bounded source audit](../notes/positive-polynomial-loglog-degree-novelty.md)
credits proportional-fair allocation, convex duality, dyadic approximation,
and binary-product methods. It found no matching whole-formulation count
theorem. Publication priority remains unestablished.

The [first independent audit](../notes/review-positive-polynomial-loglog-precision.md)
and [second independent audit](../notes/review-positive-polynomial-loglog-precision-second.md)
both passed. The [exact checker](../code/quadratic_rank/check_positive_polynomial_loglog.py)
passed 276 square-root convexity identities, 1,021 layer curvature bounds,
1,021 prefix/Taylor bounds, and 30 scalarization KKT cases. The first
reviewer additionally checked 737 curvature inequalities and 33,165
power/Taylor cases, including unused layer codes and zero-depth prefixes.

The degree term in this construction is not asserted necessary relative
to the true optimum. The pure-power subclass admits a stronger linear
dimension construction. The separate benchmark-gap investigation concerns
the limitations of the coefficient-sum allocation itself.

The [allocation degree-gap example](../notes/positive-polynomial-allocation-degree-gap.md)
shows that an additive `O(r)` upper characterization using this same
coefficient-sum benchmark is impossible uniformly in the degrees: one
variable already has gap `0.5 log2 log2 D+O(1)`. Both independent audits
of that obstruction passed. This does not prove that a `log log D`
excess over the true optimum is necessary for every construction.

The [compiled sparse-input extension](sparse-positive-polynomial-circuit-precision.md)
retains this integer-count bound with polynomial construction time and size
in binary exponent lengths. It replaces numerical-degree power recurrences
by downward-rounded endpoint evaluation compiled into continuous Boolean
gates, retaining only the same layer and cell index binaries.
