# Independent review of latent-separator design bounds

Date: 2026-09-12. The mathematical construction in the
[author note](research-20260912-latent-separator-design.md) is accepted under
its stated assumptions, including the nested-anchor comparison and the
conditional bridge formulas. This review does not assess the producer
implementation, performance, or novelty. The reviewer did not import or read
the producer implementation while constructing the checks below.

The general representation requires independent latent and measurement
noise, a scalar first-order Gaussian Markov process, and invertible anchor
covariance. Positive measurement variance alone does not make a degenerate
anchor covariance invertible. The author added these assumptions after this
review identified the omission. The stationary assumptions `P>0` and
`|rho|<1` imply an invertible latent covariance. All covariance parameters
are fixed, independently of `theta`.

Conditional Gaussian residuals satisfy `Cov(z,U)=0`, hence independence.
The Markov property separates the open intervals between anchors after
conditioning on the anchors. At an anchor coordinate the latent residual is
identically zero. Its independent measurement noise may therefore be assigned
to either neighboring block, exactly once. This gives an exact block
diagonal covariance `D`, and `D` is positive definite because `r>0`.
Selected anchors count toward the sampling budget; the latent anchor prior
does not supply free observations. Empty selected blocks contribute the zero
increment. With no anchors, the entire observation covariance is the one
block `D=K+rI`.

The augmented information matrix is the Hessian of the joint Gaussian
quadratic in `(theta,U)` after including the two independent priors. Its
lower-right block is positive definite. Woodbury gives exactly

```text
Schur_theta M(S) = J0 + F_S^T (K_SS+rI)^-1 F_S.
```

Here marginalizing the Gaussian random effect is essential: the anchor
precision is present once, and the determinant produced by integrating out
the random effect is independent of `theta`. Omitting its prior, treating
the anchors as free data, or repeating that prior per block would describe a
different model. Direct dense rational calculations verify the identity for
every selected subset in the tested models.

For `M=[[A,B],[B^T,C]]`, write `J=A-BC^-1B^T` and
`G_*=-C^-1B^T`. For every conforming matrix `T`, completing the square gives

```text
[I;T]^T M [I;T] = J + (T-G_*)^T C (T-G_*).
```

Thus the Schur complement is an attained least matrix in positive
semidefinite order. If `M=lambda M1+(1-lambda)M2`, apply the same trial
matrix `T=G_*(M)` to the two summands. Each summand dominates its own Schur
complement, so

```text
Schur(M) >= lambda Schur(M1)+(1-lambda)Schur(M2).
```

Monotonicity and concavity of log determinant prove concavity of
`f(M)=logdet Schur(M)`. This argument justifies the matrix-minimum statement
without relying on an unsupported general rule about matrix infima.
Differentiation gives

```text
grad f(M) = E J^-1 E^T,  E=[I;G_*].
```

An independent identity is
`grad f(M)=M^-1-diag(0,C^-1)`, obtained from
`f(M)=logdet M-logdet C`. The gradient is positive semidefinite and has
rank exactly `p` on the positive definite domain because `E` has full column
rank. The author's weaker phrase "rank at most p" is valid. Also
`tr(grad f(M) M)=tr(J^-1 E^T M E)=p`, so the tangent intercept and dimension
constant in the note have the correct scaling.

For arbitrary symmetric positive definite `W` and arbitrary `G`, the same
completion of the square gives `Q_G(S)=[I;G]^T M(S)[I;G]>=J_true(S)`.
The ordinary logdet tangent at `W^-1` gives

```text
logdet J_true(S)
 <= -logdet W-p+tr(W J_true(S))
 <= -logdet W-p+tr(W Q_G(S)).
```

Expanding the last trace gives exactly equation (1) in the author note,
with the plus sign in `F+HG`, the term `-logdet W-p`, and the two prior
quadratics each included once. No feasibility or optimality condition is
needed on `G`. Rounding `G` is harmless to validity. Rounding `W` requires
preserving symmetry and checking positive definiteness. An actual numeric
certificate must also enclose its logarithm and accumulated support values
in the correct direction; an unchecked floating objective is not an exact
certificate.

At a reference matrix or augmented mixture, use `W=J^-1` and `G=G_*`.
Then `-logdet W=f(M)` and the displayed inequality is precisely the global
gradient tangent. Optimizing over arbitrary `W,G` is unnecessary for
validity. A converged continuous optimizer is also unnecessary for validity
when its support maximum is certified.

For one fixed `W,G`, let `q_l(T)` be the nonnegative score of pattern `T`
in block `l`, excluding both priors, and set

```text
a_l(t) = max {q_l(T): T subset I_l, |T|=t},
V_0(0)=0; V_0(c)=-infinity for c!=0,
V_l(c) = max_t {V_(l-1)(c-t)+a_l(t)}.
```

Every global selected set has exactly one within-block pattern in each
block, and conversely any tuple of patterns with total count `k` defines
one selected set of size `k`. Therefore `V_L(k)` is exactly the global
support maximum. Maximizing separate counts without this final convolution
would not enforce a common budget. An empty block contributes only its
zero-count, zero-score pattern. Adding
`-logdet W-p+tr(WJ0)+tr(WG^T K_A^-1G)` after this program adds the fixed
terms once, including when `k=0`. The result is exact for the stated
cardinality-only family; additional scheduling constraints require a
corresponding support oracle. The combinatorial count is polynomial in
`n,k,2^b`; this is not a bound on the bit lengths of exact intermediate
rationals or a claim that the nonlinear hull problem is an integer solver.

The nested-anchor hierarchy is also valid. Let `A` be a subset of `B` and
retain `(theta,U_A)` when eliminating `U_(B\A)` from `M_B(S)`. The joint
density `p(Y_S,U_B|theta)` becomes `p(Y_S,U_A|theta)` upon integrating those
coordinates. Its quadratic Hessian is exactly `M_A(S)`, including the
cross terms in the Gaussian anchor prior:

```text
M_A(S) = Schur_remove_(B\A) M_B(S).
```

This identity does not require the anchor prior to be block diagonal in
the retained and removed coordinates. For any common probability
distribution `alpha` over feasible schedules, Schur concavity gives

```text
sum_S alpha_S M_A(S)
 <= Schur_remove_(B\A) (sum_S alpha_S M_B(S)).
```

The parameter Schur complement is monotone in positive semidefinite order,
as follows directly by applying its minimizing trial matrix to a pair of
ordered matrices. Apply this monotonicity, then logdet monotonicity and
associativity of Schur elimination. The objective at the `A` mixture is
no larger than at the `B` mixture. Both full convex hulls are images of the
same distribution simplex, so maximizing preserves `U_A<=U_B`.
Removing anchors strengthens the mathematical hull bound while increasing
the conditional block sizes. Arbitrary nonnested anchor sets have no order
established here. Bounds from unfinished numerical iterations need not
follow the hull ordering. Even `A` empty can retain a logdet mixture gap to
the best individual information matrix.

The singleton-block reduction is an established baseline equivalence. For
any diagonal residual split `D=diag(d)` and selection weights `z`, the
singleton-pattern augmented mixture has Schur information

```text
J(z)=J0+F_T^T [R_TT+diag(d_i(1-z_i)/z_i : i in T)]^-1 F_T,
T={i:z_i>0}.
```

This follows by applying Woodbury to the positive-weight rows; zero weights
are omitted. It is the diagonal virtual-noise/Liu form. Anchoring every
candidate gives `D=rI`, hence the scalar split `a=r`. Under the author's
endpoint-omitting convention and `b=1`, for `n>=2` it instead gives
`D=diag(r,...,r+P(1-rho^2))`, a diagonal-split variant. For `n=1` there
are no anchors and the only residual variance is `P+r`; the final formula
does not apply. The author added this endpoint exception after review. These
equivalences were routed to the prior-art and sole literature agents. They
are mathematical reductions, not novelty findings.

For stationary covariance, conditioning on adjacent anchors gives the two
displayed interpolation coefficients by inverting their `2 by 2`
covariance. Farther anchors supply no additional conditional dependence.
All denominators are positive because the anchor gap is positive and
`|rho|<1`. Signed powers retain the correct signs when `rho<0`.
The one-anchor exterior formulas and unit row at a selected anchor agree
with the full dense conditional mean. The anchor vector itself is a
nonuniformly sampled stationary Markov chain, with initial variance `P`,
transition `c_j=rho^(a_j-a_(j-1))`, and innovation variance
`P(1-c_j^2)`. Its quadratic density gives exactly the sparse prior formula
in the note. The first term occurs once. With no anchors the whole prior
quadratic is zero.

The conditional bridge variance and transition formulas are correct for
no anchors, one bounding anchor, and two bounding anchors. In a conditional
interval write its marginal residual variance as `V_t`. For selected
`s<t`, direct conditional covariance satisfies

```text
Cov(z_t,z_s) = a_ts V_s,
q_ts = V_t-a_ts^2 V_s >= 0.
```

When a right anchor `c` exists, the displayed denominator requires `s<c`.
The transition also remains valid when `s` is a left anchor with `V_s=0`;
the next innovation variance then equals `V_t`. At `t=c`, both the
transition and `V_t` vanish, and the observation innovation variance is
exactly `r`. These checks include negative and zero correlation. Because
the conditional process is Markov, the resulting innovations are independent
of its earlier residual states. The proposed noisy Kalman recursion follows
and reproduces the dense conditional information for arbitrary augmented
sensitivities `[F,H]`.

The saved reviewer code is
[review_latent_separator_theory.py](../code/research_20260912/review_latent_separator_theory.py),
with results in
[latent-separator-independent-theory-checks.json](../code/research_20260912/results/latent-separator-independent-theory-checks.json).
It uses only SymPy dense rational algebra, its own rational logarithm
enclosures, and enumeration. It imports no producer, support-oracle, or
certificate implementation. All assertions passed. The checks include:

- 564 stationary and 64 nonstationary all-subset information identities
  against the original dense selected covariance.
- 27 complete cardinality support comparisons, 564 block-additivity checks,
  and 564 exact completion-of-the-square and arbitrary-`G` PSD checks.
- 96 arbitrary-`W,G` certificates checked using rational logarithm
  enclosures, plus 16 gradient/tangent/concavity checks for general SPD
  block matrices.
- 576 nested-anchor single-schedule identities and 18 exact nested-mixture
  matrix-order checks, including empty and nonempty retained anchor sets.
- 864 all-subset conditional bridge Kalman information comparisons, 72
  bridge variances, and 183 transition covariances and nonnegative innovations.
- No anchors, one candidate, selected anchors, reassigned anchors, empty
  selected blocks, an explicit empty DP block, unequal end blocks, zero
  correlation, negative correlation, and the singleton virtual-noise
  reduction with zero selection weights. Three further cases check uneven
  anchor gaps against the full dense anchor precision and conditional mean.

Reproduction from the repository root:

```sh
code/research_20260912/.venv/bin/python code/research_20260912/review_latent_separator_theory.py
```

The tests provide exact finite-case checks; the arguments above establish
the general claims. No producer performance or end-to-end certificate
verification is inferred from this theory review.
