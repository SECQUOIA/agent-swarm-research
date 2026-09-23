# Exact block-pattern bounds from latent-state separators

Date: 2026-09-12. The derivation passed
[fresh independent proof review](research-20260912-latent-separator-independent-review.md),
and the [numerical prototype](research-20260912-latent-separator-implementation.md)
passed [separate implementation review](research-20260912-latent-separator-implementation-independent-review.md).
[Exact certificates](research-20260912-latent-separator-certificates.md) are
documented separately. The matrix identities, nuisance-parameter criterion
and block-pattern enumeration have established antecedents. The
[priority audit](research-20260912-latent-separator-priority-audit.md) limits
the candidate contribution to the specialized hierarchy and its demonstrated
strengthening/cost tradeoff; publication priority remains unresolved.

The motivation is a practical limitation of calendar-history truncation.
Refining a time grid while holding the physical correlation process fixed
increases correlation per step. The sufficient history length can then make
the explicit mask graph too large. This proposal retains temporal correlation
through separator variables and enumerates observation patterns only inside
short blocks. It has no truncation error parameter.

## Conditional block representation

Let the observations be

```text
Y = F theta + X + v,
X ~ N(0,K),  v ~ N(0,r I),  r>0,
```

with independent `X,v`, known scalar Gauss–Markov latent covariance `K`, and
a positive definite parameter-information prior `J0`. Choose latent anchor
coordinates `U=X_A` with positive definite anchor covariance `K_A`.
The stationary assumptions below guarantee this. A degenerate latent model
requires separate treatment and is not covered by the inverse formulas here.
Write their covariance as `K_A`, and decompose

```text
X = H U + z,
H = K_:A K_A^-1,
D = Cov(z+v) = K-K_:A K_A^-1 K_A: + r I.
```

The residual `z` is independent of `U`. Conditioning on the anchor values
makes disjoint intervals between anchors independent. Assign each anchor-time
observation to exactly one neighboring block; its residual is just its own
independent measurement noise. The resulting `D` is block diagonal and SPD.
For block length at most `b`, each selected within-block covariance has order
at most `b`. The first and last intervals need only one bounding anchor.

A concrete partition is `I_l={lb,...,min((l+1)b,n)-1}` with anchors at
`b-1,2b-1,...` strictly below `n-1`. Each anchor observation belongs to the
block ending there. The last block has no required right anchor. For `b>=n`,
there are no anchors and a single full observation block.

## Exact information as a Schur complement

For a common selected set `S`, retain `F_S,H_S,D_SS`. Define the augmented
matrix, with the parameter coordinates first,

```text
M(S) = diag(J0,K_A^-1)
       + [F_S,H_S]^T D_SS^-1 [F_S,H_S].
```

Equivalently it is the fixed prior plus one PSD increment for each chosen
within-block pattern. The lower-right block is positive definite. Eliminating
the latent coordinates gives

```text
Schur_theta M(S)
 = J0+F_S^T[D_SS^-1
   -D_SS^-1 H_S(K_A^-1+H_S^T D_SS^-1 H_S)^-1 H_S^T D_SS^-1]F_S
 = J0+F_S^T R_SS^-1 F_S,
R = D+H K_A H^T = K+r I.
```

The second equality is the matrix inversion lemma. This is the original
marginal selected information, not information conditional on observing the
anchors for free. The Gaussian anchor prior supplies the term `K_A^-1`.
The representation is exact even when no observations are selected in some
blocks. With no anchors, it reduces to ordinary selected information.

## Concave objective and common support price

For a positive definite block matrix `M=[[A,B],[B^T,C]]`, put

```text
J = A-B C^-1 B^T,
G = -C^-1 B^T,
E = [I;G],
f(M) = log det J.
```

The Schur complement is matrix concave on this domain: it is the attained
matrix minimum of `[I;T]^T M [I;T]` over `T`. Composing with monotone concave
logdet makes `f` concave. Its gradient is the PSD matrix

```text
grad f(M) = E J^-1 E^T,
tr(grad f(M) M) = p.
```

Consequently a fully corrective mixture of augmented matrices can propose a
tangent, and the global linear support maximum over all feasible schedules
gives a valid original-objective upper bound. A mixture is not reported as
a feasible experiment. The number of nuisance coordinates grows with the
number of anchors; the support gradient nevertheless has rank at most `p`.

A direct certificate avoids needing a full augmented reference matrix. For
any SPD `W` of order `p` and any anchor-by-parameter matrix `G`, elimination
and the ordinary logdet tangent imply

```text
logdet J_true(S)
 <= -logdet W-p + tr(W J0) + tr(W G^T K_A^-1 G)
    + sum_blocks tr{W (F_Sl+H_Sl G)^T
                         D_SlSl^-1 (F_Sl+H_Sl G)}.       (1)
```

The quadratic matrix inside this upper bound is
`[I;G]^T M(S)[I;G]`, which dominates its Schur complement. The choices
`W=J^-1` and `G=-C^-1 B^T` at a proposed augmented mixture recover its
tangent. Arbitrary rounded `G` remains valid, and only positive definiteness
of the rounded `W` must be checked for (1).

For fixed `W,G`, enumerate each block's at most `2^b` observation patterns.
Every pattern has a nonnegative scalar score from (1) and a cardinality.
An exact count dynamic program over blocks maximizes the sum for total
cardinality `k`. It enforces one common feasible selection and adds the
fixed prior and anchor quadratic once. Its combinatorial cost is polynomial
in `n,k,2^b`; no factor `2^L` from a long temporal window appears.

The objective over the convex hull can have a nonzero gap to the best single
schedule. Small block size may also yield a weak bound after latent nuisance
elimination. Avoiding truncation does not imply an exact integer solver or a
monotone hierarchy for arbitrary, nonnested choices of anchors. Both bound
strength and computational cost need measurement.

### Nested anchors give a monotone relaxation hierarchy

There is a stronger statement for nested anchor sets over the same feasible
schedule family. Let `A` be a subset of `B`, and order the larger augmented
matrix by `(theta,U_A,U_(B\A))`. Gaussian marginalization gives exactly

```text
M_A(S) = Schur_(B\A) M_B(S).
```

This includes the Gaussian prior cross blocks. Integrating the removed
coordinates from `p(Y_S,U_B | theta)` leaves `p(Y_S,U_A | theta)`;
the Gaussian integration normalizer depends only on known covariances.
Equivalently, the identity follows by block elimination of the joint
quadratic form.

For any distribution `alpha` over the same feasible schedules, Schur
concavity implies

```text
sum_S alpha_S M_A(S)
 <= Schur_(B\A) [sum_S alpha_S M_B(S)].
```

Apply the monotone parameter Schur complement and logdet, then maximize
over the common distribution. The full hull optima satisfy `U_A<=U_B`.
Removing anchors and merging their conditional blocks therefore tightens
the relaxation. This compares mathematical hull optima; unfinished numerical
tangent bounds need not appear monotone. Empty `A` yields the hull of the
true information matrices, which may still have a gap to a single schedule.
The conclusion does not compare arbitrary nonnested partitions.

At `b=1` and `n>=2`, the stated convention leaves the last candidate unanchored.
Its conditional covariance is
`D=diag(r,...,r+P(1-rho^2))`. Singleton-pattern convexification is then
exactly the diagonal virtual-noise/Liu relaxation for that split. Anchoring
every candidate instead gives the familiar scalar split `D=r I`.
For `n=1`, the stated no-anchor convention has `D=[r+P]` instead.
Neither is a new baseline relaxation.

## Stationary scalar formulas for implementation

For `K_ij=P rho^|i-j|`, `P>0`, `|rho|<1`, a point `i` between neighboring
anchors `a<c` has only two nonzero anchor loadings. Write `l=i-a`, `u=c-i`:

```text
H_i,a = rho^l (1-rho^(2u))/(1-rho^(2(l+u))),
H_i,c = rho^u (1-rho^(2l))/(1-rho^(2(l+u))).
```

Before the first anchor or after the last one the single loading is the
corresponding power of `rho`; at an anchor it is the unit coordinate.
Compute each block of `D` as its stationary latent covariance minus the
anchor-explained covariance, then add `r I`. These expressions are rational
for rational data, including signed correlations. Exact calculations should
verify the claimed cross-block zeros rather than infer independence from
small floating entries.

For anchors `a_1<...<a_m`, their prior quadratic is also sparse. Put
`c_j=rho^(a_j-a_(j-1))`. For the rows of `G`,

```text
tr(W G^T K_A^-1 G)
 = G_1 W G_1^T/P
   + sum_(j=2)^m (G_j-c_j G_(j-1)) W (G_j-c_j G_(j-1))^T
                       /[P(1-c_j^2)].
```

Thus neither the support score nor its exact certificate requires a dense
inverse of the anchor covariance. Interior blocks of equal length also
share their conditional covariance patterns, although sensitivities differ.

An exact scalar Kalman recursion can avoid repeated block inversions.
Let `V_t` be the unconditional variance of the residual latent process inside
one block. With a left anchor `a` and right anchor `c`,

```text
V_t = P(1-rho^(2(t-a)))(1-rho^(2(c-t)))/(1-rho^(2(c-a))).
```

With only the right anchor use `P(1-rho^(2(c-t)))`; with only the left
use `P(1-rho^(2(t-a)))`; with neither use `P`. Between selected times
`s<t` in the same block, the residual transition is

```text
a_ts = rho^(t-s)(1-rho^(2(c-t)))/(1-rho^(2(c-s)))
```

when a right anchor exists, and `rho^(t-s)` otherwise. The denominator
is positive because an earlier selected time precedes the right endpoint.
Its innovation variance is `V_t-a_ts^2 V_s>=0`. Starting a fresh filter
with the appropriate `V_t`, propagate a posterior variance as
`Ppred_t=V_t-a_ts^2 V_s+a_ts^2 Ppost_s` and use measurement variance `r`.
At a right-anchor observation the residual latent variance and transition
are zero, leaving variance `r`. These are conditional Gauss–Markov formulas,
not a new filtering method; independent exact checks are part of the review.

## Validation and practical test

The independent reviews compared every tiny selected subset against direct
inversion of its original covariance, including selected anchors, empty blocks,
unequal end blocks, negative correlations and no anchors. They checked
concavity, gradients, exact count prices and bridge filtering. The numerical
prototype was then tested on the fixed-physical-kernel grid-refinement problem
with budget 16 and explicit cooperative time/workspace limits. Its physical-step
correlations are rational powers of `4/5`; five original-objective certificates
were recomputed exactly. The implementation and certificate notes retain the
results and failures, including a nonzero discrete gap.

The source audit distinguishes established random-effects Schur complements,
D_s-optimality, nuisance-variable design and block formulations from the
candidate hierarchy. The finite benchmark establishes a particular bound
strengthening at 192 candidates, not a first-method claim or general solver
superiority.
