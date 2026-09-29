# Sparse kernel rounding with polynomial constraints and geometric repair

Date: 2026-09-28. Completed theorem note; independent review and targeted
verification are recorded below. This note separates a global geometric assumption from local moment
positivity. A localizing matrix does not by itself produce a
measure supported on its constraint set.

## 1. Result and scope

Adding polynomial constraints to the box kernel construction gives a direct
bound on the expected **squared constraint violation**. A global Hölder
error bound then repairs the resulting actual law onto the feasible set.
For exponent `alpha` in that geometric bound, the full box-preordering
construction gives hierarchy error `O(R^-alpha)`. The ordinary-module SOS
kernel gives `O((log(R)/R)^alpha)` at fixed problem data. The latter
bound uses a direct squared-displacement estimate, which avoids the extra
logarithm in the kernel coefficient approximation error.

When a global linear error bound holds, these are first-order and nearly
first-order bounds. The affine-recourse example in
[affine-recourse-rate-boundary.md](affine-recourse-rate-boundary.md) has a
linear global error bound and a sparse hierarchy gap of order `1/R`, so
one cannot replace the exponent one by a larger exponent for this whole
class. This is a statement about sparse hierarchies with separator moment
matching; it does not contradict faster dense or univariate bounds.

A global error bound can be much worse than the local error bounds appearing
in existing sparse effective Positivstellensätze. No uniform comparison for
all semialgebraic sets is claimed. The useful regime consists of problems
with an independently justified and reasonably conditioned global linear
or Hölder repair bound. Convex polynomial constraints satisfying Slater's
condition provide one such regime.

## 2. Model and geometric assumption

Let bags `B_b` form a finite junction tree with running intersection and
cover all `n` coordinates. Set `w=max_b |B_b|>=1`. Let

\[
 f(x)=\sum_b f_b(x_{B_b}),\qquad
 K=\{x\in[-1,1]^n:g_{bj}(x_{B_b})\ge0\text{ for all }b,j\},
 \qquad K\ne\varnothing.                                      \tag{1}
\]

There are finitely many polynomial constraints; a maximum over an empty
family is zero. A constraint assigned to
more than one bag is counted more than once in the constants below; one
assignment is enough for the theorem. Equalities can be represented by a
pair of opposite inequalities. Let `f*=min_K f`.

Assume constants `H>=0` and `0<alpha<=1` satisfy the **global** bound

\[
 \operatorname{dist}_2(x,K)
 \le H V(x)^{\alpha/2}\quad(x\in[-1,1]^n),\qquad
 V(x)=\sum_{b,j}(-g_{bj}(x_{B_b}))_+^2.                       \tag{2}
\]

Let `L_f` be any Euclidean Lipschitz constant for `f` on the box. It is
finite. A bound from the Chebyshev coefficients is
`L_f <= sum_(b,beta) |c_(b,beta)| sum_i beta_i^2`, because
`|T_k'|<=k^2` on the interval. The constant term contributes zero.

For any polynomial `p=sum_beta p_beta T_beta` define

\[
 C(p)=\sum_\beta |p_\beta|,\qquad
 A(p)=\sum_\beta |p_\beta|\sum_i\beta_i^2,
 \quad A_f=\sum_b A(f_b),\quad
 G=\sum_{b,j}C(g_{bj})A(g_{bj}).                             \tag{3}
\]

These constants depend on the supplied polynomial generators, as does the
hierarchy. Redundant box generators `1-x_i^2` are explicitly included.
Replacing or adding generators is a change of the finite relaxation.

## 3. Full box-preordering localizers

At moment order `R`, each local functional `L_b` is defined through total
degree `2R`, normalized, and agrees with its neighbors on separator
polynomials through degree `2R`. For `I subset B_b`, put
`q_I=prod_(i in I)(1-x_i^2)`. Require

\[
 L_b(q_I p^2)\ge0\quad(2|I|+2\deg p\le2R),                 \tag{4}
\]

\[
 L_b(g_{bj}q_I p^2)\ge0
       \quad(\deg g_{bj}+2|I|+2\deg p\le2R).               \tag{5}
\]

This uses each additional constraint times each box-preordering product.
It does not require products of two different additional constraints.
The full local preordering in all generators contains (4)--(5), and is
therefore at least as strong. Ordinary constrained Putinar localizers
alone do not imply (5).

Let `rho_R` be the infimum of `sum_b L_b(f_b)`. Put

\[
 d=\max\{1,\max_b\deg f_b,\max_{b,j}\deg g_{bj}\},\qquad
 R\ge\max(2d,d+w),\quad
 m=\lfloor(R-d)/w\rfloor+1\ge2,\quad D_m=2m^2+1.           \tag{6}
\]

**Theorem 1.** Every feasible moment collection in (4)--(5) has an
actual probability law `nu` supported on `K` such that

\[
 \int f\,d\nu
 \le\sum_bL_b(f_b)+{3A_f\over D_m}
                +L_f H\left({12G\over D_m}\right)^{\alpha/2}.
                                                                    \tag{7}
\]

Consequently the same expression without the pseudomoment objective
bounds `f*-rho_R` from above. For fixed data it is `O(R^-alpha)`.
No representation assumption about the input truncated moments is needed.

### Proof: smoothing and conditional positivity

Use the normalized squared-Fejér kernel `K_m` from
[sparse-kernel-rounding.md](sparse-kernel-rounding.md). Its one-coordinate
Chebyshev multipliers satisfy

\[
 0\le\lambda_k\le1,\qquad
 1-\lambda_k\le {3k^2\over D_m}.                            \tag{8}
\]

Its product on bag `b` has a box-preordering certificate of source degree
at most `2|B_b|(m-1)<=2(R-d)`. Denote this kernel by `K_b(x,y)` and
its diagonal Chebyshev operator by `A_b`. Define

\[
 h_b(y)=L_b(K_b(x,y)).                                      \tag{9}
\]

The kernel theorem gives nonnegative normalized densities `h_b` against
product arcsine measure `mu_b`, with exactly matching separator marginals.
Thus they are marginals of a global box-supported law `sigma`.
For every local objective,

\[
 \left|\int f_bh_b\,d\mu_b-L_b(f_b)\right|
 \le {3A(f_b)\over D_m}.                                  \tag{10}
\]

Fix one constraint `g=g_bj` and an output `y`. The degree reserve `d`
implies that `F_y(p)=L_b(K_b(x,y)p(x))` is positive on the squares of
all polynomials needed for the pair `1,g(x)`: multiply each term of the
kernel certificate by the square of an affine combination of `1,g`.
Its total degree is at most `2(R-d)+2d=2R`. The same certificate and
(5) give `F_y(g)>=0`.

If `g(y)<0`, let `a=-g(y)>0`. Cauchy--Schwarz for `F_y` gives

\[
 a h_b(y)\le F_y(g(x)-g(y)),\qquad
 a^2h_b(y)\le F_y((g(x)-g(y))^2).                          \tag{11}
\]

When `h_b(y)=0`, the second inequality is still true by positivity;
no division by zero is needed. When `g(y)>=0`, its left side is zero.
Hence for all `y`,

\[
 (-g(y))_+^2h_b(y)\le L_b(K_b(x,y)(g(x)-g(y))^2).            \tag{12}
\]

This proves small violation rather than false support preservation.

### Proof: integrated squared violation

Integrating (12), using exact normalization, gives

\[
 \int(-g)_+^2h_b\,d\mu_b
 \le L_b\bigl(A_b(g^2)-2gA_bg+g^2\bigr).                   \tag{13}
\]

The polynomial inside `L_b` has degree at most `2deg g<=2d<=R`.
The box moment inequalities imply `|L_b(T_beta)|<=1` at degree at most
`R`; therefore coefficient-norm bounds can be evaluated safely.
The multiplier estimate (8) gives

\[
 C(A_bp-p)\le 3A(p)/D_m.                                  \tag{14}
\]

Tensor Chebyshev multiplication satisfies

\[
 C(pq)\le C(p)C(q),\qquad
 A(pq)\le C(p)A(q)+A(p)C(q).                               \tag{15}
\]

For the second inequality, expand `T_a T_b` as the average of
`T_(a+b)` and `T_(a-b)` in each coordinate; the average squared
frequency is `a_i^2+b_i^2`. Triangle inequalities then prove (15),
including zero indices and repeated frequencies. Thus

\[
 C(A_b(g^2)-2gA_bg+g^2)
 \le {3\over D_m}\bigl[A(g^2)+2C(g)A(g)\bigr]
 \le {12C(g)A(g)\over D_m}.                               \tag{16}
\]

Summing (13)--(16) proves

\[
 \int V\,d\sigma\le12G/D_m.                               \tag{17}
\]

### Proof: global feasible repair

Since `K` is nonempty and compact, a finite epsilon-net in `K` gives a
Borel map `P_epsilon` whose distance from any box point is at most its
distance to `K` plus epsilon. Push `sigma` through this map. The global
error bound, the Lipschitz bound, and concavity of `t^(alpha/2)` imply

\[
 \int f(P_\varepsilon x)\,d\sigma(x)
 \le\int f\,d\sigma+L_fH\left(\int V\,d\sigma\right)^{\alpha/2}
                      +L_f\varepsilon.                    \tag{18}
\]

Take a weakly convergent subsequence of these repaired laws as epsilon
tends to zero. Compactness of `K` and continuity of `f` preserve (18)
in the limit. Equations (10),(17) prove (7). Some feasible point has
objective at most the resulting expectation. This proves existence,
not an efficient algorithm for global projection onto `K`. ∎

## 4. Ordinary constrained Putinar hierarchy

Replace (4)--(5) by the standard local conditions

\[
 L_b(p^2)\ge0,\quad L_b((1-x_i^2)p^2)\ge0,\quad
 L_b(g_{bj}p^2)\ge0,
 \qquad\text{each product of degree at most }2R.             \tag{19}
\]

Use `s,N,D,delta,a,eta,Gamma_v` from
[sparse-putinar-kernel.md](sparse-putinar-kernel.md), with even `N>=2`.
Take `d_infty` at least every coordinate degree of the objectives and
constraints, and take `s>=max(2,d_infty)`. Keep `d` from (6), and require

\[
 R\ge wD+2d.                                              \tag{20}
\]

Write `Q_b` for the product SOS source kernel, `A_b` for its integral
operator, and

\[
 h_b(y)=L_b(Q_b(x,y)),\quad Z_b=\int h_b\,d\mu_b,
 \quad a^{|B_b|}\le Z_b\le1,\quad
 \varepsilon_T=\min\{1,\sum_e\varepsilon_e\},               \tag{21}
\]

where the edge bounds `epsilon_e` are those of the companion note.
Let `E_(s,N)` denote its objective bound (5), with the present objective
and degree parameter. Define

\[
 G_2=\sum_{b,j}C(g_{bj})^2,\qquad
 c_s={4\over sC_s}\le{6\over s^2},\qquad
 U_{s,N}=c_s\sum_{b,j}{A(g_{bj})^2\over a^{|B_b|}}
                         +G_2\varepsilon_T,
 \quad C_s={2s^2+1\over3s}.                               \tag{22}
\]

**Theorem 2.** Every feasible collection for (19) admits a probability
law `nu` on `K` with

\[
 \int f\,d\nu\le\sum_bL_b(f_b)+E_{s,N}
                             +L_fH U_{s,N}^{\alpha/2}.       \tag{23}
\]

For fixed problem data choose `N=2ceil((3/2)log_2 s)` and `s` of order
`R/(w log R)` satisfying (20). Then `U_(s,N)=O(log^2(R)/R^2)`, and

\[
 0\le f^*-\rho_R
 =O\left((\log(R)/R)^\alpha\right).                       \tag{24}
\]

Constants may depend on the tree size, the generators, `H`, and `L_f`.
There is no assertion uniform in the number of bags.

### A univariate squared-displacement bound

The kernel in the companion note is `Q(x,y)=p_(s,N)(x) S_s(x,y)^2`,
where `p_(s,N)` is globally SOS and
`0<=p_(s,N)<=2/C_s` on the interval. Define

\[
 J_s(x)=\int(x-y)^2S_s(x,y)^2\,d\mu(y),\qquad
 j_s(x)=p_{s,N}(x)J_s(x).
\]

Both polynomials are globally SOS, by integration of polynomial squares
and multiplication of SOS polynomials. Their degrees are at most `2s`
and `D+2`, respectively. We claim

\[
 0\le J_s(x)\le2/s,\qquad 0\le j_s(x)\le c_s
                    \quad(-1\le x\le1).                   \tag{25}
\]

For a direct proof, write `x=cos(theta)`, `y=cos(phi)` and let
`F_s(t)=sum_j b_j exp(ijt)` be the Fejér kernel, where
`b_j=(1-|j|/s)_+`. Then
`S_s(x,y)=[F_s(theta-phi)+F_s(theta+phi)]/2`.
The inequality `[(u+v)/2]^2<=(u^2+v^2)/2` and reflection of the
`phi` integral convert the upper bound on `J_s` to one circle integral.
Use
`[cos(theta)-cos(theta-t)]^2<=2(1-cos t)` to obtain

\[
 J_s(\cos\theta)
 \le\int_{-\pi}^{\pi}2(1-\cos t)F_s(t)^2\,{dt\over2\pi}
 =\sum_{j\in\mathbb Z}(b_j-b_{j-1})^2={2\over s}.
\]

There are exactly `2s` nonzero successive differences, each of absolute
value `1/s`. Multiplication by `p_(s,N)<=2/C_s` proves (25).
The univariate interval SOS theorem therefore supplies a certificate
for `c_s-j_s` in the module generated by `1-x^2`, of degree at most
`D+2`. This certificate, rather than a multivariate pointwise positivity
claim, is what allows evaluation under a pseudomoment functional.

### A degree-preserving constraint difference certificate

For `g=sum_beta c_beta T_beta`, put
`A_i(g)=sum_beta |c_beta| beta_i^2`, so `A(g)=sum_i A_i(g)`.
For every fixed output `y` in the bag box, the polynomial

\[
 A(g)\sum_i A_i(g)(x_i-y_i)^2-(g(x)-g(y))^2                \tag{26}
\]

belongs to the ordinary box module at degree at most `2deg g`.
For constant `g` the polynomial is zero.

To prove this for nonconstant `g`, telescope each tensor product in
coordinate order. For an index with `k=beta_i>0`, let

\[
 D_k(x_i,y_i)={T_k(x_i)-T_k(y_i)\over x_i-y_i},\quad
 v_{\beta i}=\operatorname{sign}(c_\beta)(x_i-y_i)
 {D_k(x_i,y_i)\over k^2}
 \prod_{\ell<i}T_{\beta_\ell}(x_\ell)
 \prod_{\ell>i}T_{\beta_\ell}(y_\ell).
\]

The divided difference is its polynomial extension when `x_i=y_i`.
The bound `|T_k'|<=k^2` implies `|D_k/k^2|<=1` on the interval.
With `w_(beta i)=|c_beta| beta_i^2`, telescoping gives
`g(x)-g(y)=sum_(beta,i) w_(beta i) v_(beta i)` and
`sum_(beta,i) w_(beta i)=A(g)`.
Weighted Cauchy--Schwarz is the SOS identity

\[
 A(g)\sum_r w_r v_r^2-\left(\sum_r w_rv_r\right)^2
       =\sum_{r<t}w_rw_t(v_r-v_t)^2.
\]

Also `(x_i-y_i)^2-v_(beta i)^2` has an ordinary box-module certificate:
factor out the square `(x_i-y_i)^2`; telescope `1` minus the product of
the remaining squared factors. The factor
`1-(D_k/k^2)^2` has a univariate interval certificate of degree at most
`2(k-1)`. Each `1-T_l^2=(1-x^2)U_(l-1)^2` has degree `2l`,
and output factors have absolute value at most one. The telescoping
multipliers are products of squares; only one box generator occurs in
each summand. Multiplication by `(x_i-y_i)^2` leaves degree at most
`2|beta|`. Adding these certificates with weights `A(g)w_(beta i)`
to the weighted Cauchy--Schwarz identity proves (26).

### Constraint violation and global repair

Since `Q_b` is globally SOS in the source coordinates, (19),(20) imply
that `F_y(p)=L_b(Q_bp)` is positive on the squares needed for `1,g`,
and `F_y(g)>=0`. Thus (12) remains valid with `Q_b` in place of `K_b`.
Multiplying the certificate (26) by `Q_b` stays in the ordinary box
module, of degree at most `|B_b|D+2d<=R`. Apply this certificate for each fixed
`y`, and then integrate the resulting scalar inequality; no measurable
selection of SOS certificates is needed. Consequently

\[
 \int(-g(y))_+^2h_b(y)\,d\mu_b(y)
 \le A(g)\sum_iA_i(g)
   L_b\left(j_s(x_i)\prod_{\ell\ne i}n(x_\ell)\right)
 \le c_s A(g)^2.                                        \tag{27}
\]

The last inequality also has the required certificate. The companion
note proves `1-prod_(ell!=i)n(x_ell)` belongs to the ordinary box
module, while every `n` is globally SOS. Use

\[
 c_s-j_s(x_i)\prod_{\ell\ne i}n(x_\ell)
 =c_s\left(1-\prod_{\ell\ne i}n(x_\ell)\right)
   +(c_s-j_s(x_i))\prod_{\ell\ne i}n(x_\ell).
\]

Its degree is at most `|B_b|D+2<=R`, and its evaluation under `L_b`
is nonnegative. Dividing (27) by `Z_b>=a^|B_b|` bounds the squared
violation under the normalized bag law.

The companion tree repair couples all normalized bag laws into one
global box assignment, changing the records only on an event of
probability at most `epsilon_T`. On its complement the records agree
and are retained. Therefore the global law `sigma` satisfies

\[
 \int V\,d\sigma\le U_{s,N},\qquad
 \int f\,d\sigma\le\sum_bL_b(f_b)+E_{s,N},                \tag{28}
\]

because `sup_box V<=G_2`. Apply the global feasible repair (18) to
prove (23). The parameter choice gives `delta<=1/(2s^3)`,
`epsilon_T=O(s^-3)` for the fixed tree, and `U_(s,N)=O(s^-2)`.
The objective error is `E_(s,N)=O(log(s)/s^2)`. Since `0<alpha<=1`,
this objective term is smaller than `O(s^-alpha)`. Taking `s` of
order `R/log R` proves (24). For example, for every sufficiently large
`R`, `s=floor((R-2d)/(8w log_2(R+2)))` satisfies all conditions. ∎

An earlier bound used coefficient approximation on `g^2`, `g`, and `1`
to estimate the squared violation. It gave
`O((log^(3/2)(R)/R)^alpha)`. The direct displacement certificate above
replaces that estimate and improves its logarithmic factor. The older
finite coefficient checks remain useful checks of a valid weaker bound;
they are not the verification of (25)--(27).

## 5. An explicit global linear-bound regime

Suppose every supplied `g_bj`, interpreted as a function of all variables,
is concave on the box. Suppose a single box point `x0` satisfies
`g_bj(x0)>=sigma>0` for every constraint. For any box point `x`, let
`v=max_bj(-g_bj(x))_+`, and set

\[
 \theta={v\over\sigma+v},\qquad y=(1-\theta)x+\theta x_0.
\]

Concavity gives `g_bj(y)>=-(1-theta)v+theta sigma=0`. Hence
`y in K`, and

\[
 \operatorname{dist}_2(x,K)
 \le2\sqrt n\,\theta
 \le{2\sqrt n\over\sigma}v
 \le{2\sqrt n\over\sigma}V(x)^{1/2}.                       \tag{29}
\]

Thus Theorems 1 and 2 apply with `alpha=1`, `H=2sqrt(n)/sigma`.
The objective can be nonconvex. This gives a first-order or nearly
first-order sparse lower-relaxation guarantee for polynomial nonconvex
optimization over such convex feasible sets. Its significance depends
on the geometric constants and on solving the resulting relaxations;
the precise prior comparison is recorded in the companion audit.

More generally Hoffman bounds yield `alpha=1` for nonempty polyhedra,
including lower-dimensional feasible sets where strict feasibility is
unavailable. Compact semialgebraic sets admit some Hölder bound, but
its exponent and constant can be unusable. Local Slater conditions at
different bag points do not establish the common global point in (29).

## 6. Limitations and verification status

- The feasible repair is global. Cheap local projection is not a substitute
  unless an independent consistency-repair theorem justifies it.
- No gap-free sparse SOS dual conclusion is asserted here. Equality
  constraints and empty interior can invalidate the strict-feasibility
  argument available for the box-only hierarchy. The proved bound is for
  the primal moment relaxation; dual attainment or an exact certificate
  needs its own argument under the supplied generators.
- The exponent in the geometric error bound is representation dependent.
  A vanishing high power of a constraint can make this route much slower
  even when the underlying feasible set is unchanged. This method need
  not yield the true sharp hierarchy rate.
- The theorem treats continuous polynomial constraints. Finite integer
  labels require the support-preserving discrete extension and compatible
  geometric repair; no rounding of a continuous surrogate is silently used.
- The completed [primary-source comparison](general-constraints-prior.md)
  identifies dense support repair and the preordering exponent as prior.
  The ordinary-module transport estimate improves the logarithmic factor
  over the inspected lift-plus-box-theorem composition. It is not a claim
  of priority. Global versus local error bounds prevent an unqualified
  comparison with every Korda--Magron--Ríos-Zertuche bound.
- The affine-recourse lower bound makes the power one sharp when
  `alpha=1`; it does not establish a necessary logarithm for the ordinary
  module or sharpness for every smaller geometric exponent.

The independent [proof review](general-constraints-fresh-review.md)
checked both hierarchy constructions, the displacement and constraint
certificates, all degree reserves, normalization, simultaneous objective
and violation repair, and the global geometric assumption. It found no
remaining defect. The root review independently rederived the strengthened
ordinary-module certificate.

Targeted commands actually run:

```text
python3 -B research-20260928/solver/check_general_constraints_review.py
python3 -B research-20260928/solver/check_general_constraints_transport_review.py
```

Both passed. The first script checked 4,368 exact tensor basis products,
120 signed polynomial products, 480 Jackson residual bounds, 16 weaker
ordinary-kernel residual bounds, 79 Fejér displacement constants, 18
normalized displacement bounds, and 81 simultaneous objective/violation
coupling cases. The independently written second script checked 63 exact
Fejér constants, 8 kernel degree/mass/product identities, 200 rational
inequality samples, and 24 multivariate divided-difference and weighted
square identities. The rational sample inequalities are finite checks;
the all-parameter inequalities follow from the analytic proof, not sampling.
Neither script verifies an arbitrary pseudomoment point or a numerical SDP
solution. No Lean proof, project-wide verification, or CI inspection was
performed for this note.

The stated continuous constrained theorems and their sharpened rate are
complete at this scope. Efficient global feasible projection, exact dual
attainment, and a sharper or sharp logarithmic factor are outside the
claims; none is silently assumed in the proofs.
