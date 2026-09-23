# Prior-work reduction for scalar noisy Markov design

Date: 2026-09-12. Status: detailed inference from a primary prior algorithm;
the algebra, focused specialization, and approximation/conditioning bounds
passed [fresh independent review](research-20260912-scalar-gmrf-prior-independent-review.md).
The cited algorithm's spectral-rounding numerical model is retained, as
qualified in §5. This is a priority-disproof investigation, not a
claim of a new approximation scheme. It substantially weakens the novelty of
the existence claim in the [scalar finite-history corollary](research-20260912-scalar-noisy-design-fptas.md).
The finite-history algorithm and its explicit complexity remain distinct.

## 1. Exact prior statement and the two small adaptations

Mahalanabis and Štefankovič, [*Subset Selection for Gaussian Markov Random
Fields*, arXiv:1209.5991](https://arxiv.org/pdf/1209.5991), §3.2 Theorem 43,
pp. 37–38, approximates total conditional variance within `1+gamma` on a
Gaussian precision graph of fixed treewidth `w`. Its runtime is

```text
(N w cond(Lambda)/gamma)^(O(w^2)) k^2 + N 2^(O(w^3)).
```

The corresponding result is Theorem 47, pp. 66–68, in Mahalanabis's
[2012 thesis](https://urresearch.rochester.edu/fileDownloadForInstitutionalItem.action?itemFileId=84355&itemId=25220).
The displayed theorem allows all nodes as observations and sums every
unobserved node's variance. It is not literally a focused-target theorem.

Two adaptations appear to follow from its proof:

1. Replace each local trace in recurrences (39)–(40), and their rounded
   versions (44)–(47), by a nonnegative weighted sum of diagonal covariance
   entries. Definition 18, equation (37), then has the same weights.
   Observation 33 follows from relative Loewner order before taking trace;
   the same order bounds each variance and every nonnegative weighted sum.
   Lemmas 41–42 add these nonnegative local costs and thus retain the same
   multiplicative proof. Zero local costs require writing inequalities
   without division, but cause no change to the induction. The thesis's
   earlier tree treatment explicitly permits nonnegative weights at p. 25.
2. Restrict every local observed-node subset to a prespecified candidate set.
   This only removes feasible choices in the exact and rounded recurrences.
   The rounding argument keeps the observation subset fixed, so it cannot
   introduce forbidden observations or remove the witness for an allowed
   optimal observation set.

These are interpretations of the primary algorithm, with locations sufficient
for independent checking. They are not claimed as published theorem wording.
If valid, they allow minimizing the conditional variance of one unobservable
target node while observing only designated sensor nodes, with the same
complexity bound.

The fresh reviewer confirmed an inverse/block-order error in the
printed local-cost formula (39), also present in the thesis's (2.59): its
literal private-principal-block inverse does not generally equal the
private-coordinate block of the full bag covariance required by Definition
18. The independent review supplies an exact two-variable witness, with
correct cost `3/5` versus printed cost `1/2`; the error must not be silently inherited.
For the scalar specialization there is a useful simplification: attach a
singleton `{vartheta}` bag before the empty root and retain `vartheta` in all
preceding separators. Every earlier private-node cost has weight zero; the
only positive local cost occurs in the singleton bag, whose separator is
empty. At that final step the two inverse/block orders coincide. This avoids
using a nonzero local cost in the disputed form, as the fresh reviewer
confirmed. Run messages toward the empty root; any required singleton copies
when making the decomposition binary preserve this property. The
information-message transformations still use the stated Schur complements.

## 2. Rational normalization of the noisy Markov input

Use the fixed input class of the scalar corollary: `|a_t|<=rho0<1`,
`Var(X_t)<=Pbar`, observation variances `r_t>=rmin>0`, and
`Pbar/rmin<=B0`, where `rho0,B0` are fixed constants. Assume `k>=1` and some
sensitivity is nonzero. The empty or zero-sensitivity case is trivial.
For this reduction impose only the cardinality constraint.

Choose powers of two `s,d_t>0` such that

```text
s^2 <= rmin < 4s^2,
d_t^2 <= r_t < 4d_t^2.
```

They have polynomial-size rational encodings. Let

```text
U_t = X_t/s,
Z_t = Y_t/d_t,
c_t = s/d_t,
h = max_t |f_t/d_t| > 0,
g_t = f_t/(d_t h).
```

Then `|c_t|<=2`, `|g_t|<=1`, at least one `|g_t|=1`, and the observation
noise variance `r_t/d_t^2` is in `[1,4)`. The normalized mean parameter is
`vartheta=h theta`. Information for this parameter is original data
information divided by `h^2`, so schedules have identical rankings and
multiplicative ratios. Also `Var(U_t)<=4B0`, and

```text
|Cov(U_i,U_j)| <= 4 B0 rho0^|i-j|,
||Cov(U)||_2 <= 4 B0 (1+rho0)/(1-rho0).
```

All normalization uses rational operations. No exact square root is required.

## 3. Regularization handles arbitrarily small process variances

The original latent Gaussian may be singular because process variances are
allowed to vanish. Add an independent initial innovation of variance `zeta`
and an independent innovation of variance `zeta` at every later time in the
normalized latent chain. Let `T=(I-A)^(-1)`, where `A` has entry `a_t` just
below the diagonal. Then `||A||_2<=rho0`, and the covariance increment is

```text
E = zeta T T^T,
zeta/(1+rho0)^2 I <= E <= zeta/(1-rho0)^2 I.
```

The regularized latent covariance `K_plus` is SPD and satisfies

```text
zeta/(1+rho0)^2 I <= K_plus
 <= [4 B0 (1+rho0)/(1-rho0)+zeta/(1-rho0)^2] I.
```

Let `R` now denote the normalized observation error covariance and put
`C=diag(c_t)`. It has `R>=I`. The new covariance is
`R_plus=R+C E C^T`, so

```text
R <= R_plus <= R + [4zeta/(1-rho0)^2] I.
```

Choose `tau=epsilon/4` and `zeta=tau(1-rho0)^2/4`. Every selected covariance
then satisfies `R_SS<=R_plus,SS<=(1+tau)R_SS`, hence

```text
I(S)/(1+tau) <= I_plus(S) <= I(S),
I(S)=g_S^T R_SS^(-1)g_S.
```

This is an elementary perturbation bound and is uniform over subsets. It
uses the stable generative filter and positive observation noise, without
any finite-history approximation.

## 4. A well-conditioned Gaussian model of constant treewidth

Introduce an artificial independent prior `vartheta~N(0,1)` and the joint
Gaussian model

```text
U ~ N(0,K_plus),
Z_t = g_t vartheta+c_t U_t+noise_t,
Var(noise_t) in [1,4).
```

Only the `Z_t` are observable candidates. Only `vartheta` has nonzero
posterior-variance weight. Since the prior is artificial and the parameter
is scalar, maximizing `I_plus(S)` is exactly equivalent to minimizing

```text
v(S) = Var(vartheta | Z_S) = 1/(1+I_plus(S)).
```

The precision graph has path-decomposition bags
`{vartheta,U_t,U_(t+1),Z_t}` for `t<n`, followed by
`{vartheta,U_n,Z_n}`. Thus its treewidth is at most three. These bags cover
latent-chain edges and the triangle produced by each observation density;
the running-intersection property holds.

For conditioning, the independent vector `(vartheta,U,noise)` has covariance
`diag(1,K_plus,D)`, where `I<=D<4I`. The transformation to `(vartheta,U,Z)`
is a unit block-triangular shear with bottom block `[g,C,I]`. Both the
transformation and its inverse have norm at most `1+sqrt(n+4)`, because
`||g||<=sqrt(n)` and `||C||<=2`. Therefore its joint covariance, and its
inverse precision, have condition number bounded by

```text
(1+sqrt(n+4))^4
 * max(4,4 B0 (1+rho0)/(1-rho0)+zeta/(1-rho0)^2)
 / min(1,zeta/(1+rho0)^2)
 = O_(rho0,B0)(n^2/epsilon).
```

The matrix entries remain rational with polynomial bit length. This also
covers arbitrarily varying original noise scales and arbitrarily large or
small original sensitivities: the rational coordinate changes remove those
magnitudes from the condition-number bound.

## 5. Converting posterior-variance accuracy into information accuracy

At the index with `|g_t|=1`, the regularized observation-error variance
`R_plus,tt`, excluding the artificial parameter prior contribution, is at most

```text
D0 = 4+16 B0+4zeta/(1-rho0^2).
```

Thus `I_plus(S_star)>=1/D0` for `k>=1`, since information cannot decrease when
more observations are added. The bound on `D0` follows from the marginal
variance recursion: added latent variance is at most
`zeta/(1-rho0^2)`, and `c_t^2<=4`.

Apply the adapted prior algorithm with
`gamma=epsilon/[4(D0+1)]`. If it returns a schedule whose posterior variance
is at most `1+gamma` times optimum, then

```text
I_plus(S_hat) >= [I_plus(S_star)-gamma]/(1+gamma)
 >= [(1-gamma D0)/(1+gamma)] I_plus(S_star)
 >= (1-epsilon/4) I_plus(S_star).
```

The output may use fewer than `k` candidates; padding it to cardinality `k`
can only improve true or regularized information. Combining with §3 gives

```text
I(S_hat) >= (1-epsilon/4)/(1+epsilon/4) max_(|S|=k) I(S)
          >= (1-epsilon) max_(|S|=k) I(S).
```

Returning to the original parameter multiplies both sides by `h^2`.
A nonnegative original scalar prior can then be added without weakening the
multiplicative ratio. The precision condition number and `1/gamma` are
polynomial in `n,1/epsilon`, with fixed `rho0,B0`, so the cited bounded-width
runtime is polynomial. Exact finite-precision realization of the prior
algorithm's spectral rounding should be checked against its numerical model
before treating this as a fully implemented bit-complexity reduction; this
is not grounds for claiming novelty of the FPTAS existence statement.

## 6. Priority conclusion and what remains useful

Subject to the two transparent recurrence adaptations, this reduction derives
an FPTAS for the full fixed scalar input class from the 2012 algorithm. It
also handles zero original process variances by regularization. Accordingly,
a claim of first FPTAS for scalar AR-plus-nugget measurement selection would
be unsafe and is presently rejected.

The finite-history method has a different concrete complexity: after local
weights, one `O(n k 2^L)` path computation with
`L=O(log(1/epsilon))`, and explicit relative information certificates valid
for arbitrary sensitivity dimension. The 2012 construction instead
quantizes constant-width covariance messages and has a large polynomial
bound involving `n` and conditioning. Whether the specialized method has a
meaningful new complexity or implementation advantage requires a direct
comparison. This note does not turn such a possible advantage into a claim
of originality or practical superiority.

The reduction here has a scalar latent state. For a block latent state of
dimension `d`, its graph width grows with `d`; the old fixed-width runtime
does not by itself prove polynomial dependence on an unrestricted input
dimension. The separately reviewed full-block finite-history bound has no
dimension factor in `delta`. That distinction warrants a separate scope and
priority check if an application observes complete vector blocks. It is not
a novelty conclusion of this note.
