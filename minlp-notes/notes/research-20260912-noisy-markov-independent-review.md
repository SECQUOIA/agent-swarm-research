# Independent review of the noisy scalar Markov memory bound

Date: 2026-09-12. Reviewer: a fresh research agent, independent of the draft
author. The reviewed draft is
[Uniform finite-history approximation for noisy scalar Markov design](research-20260912-noisy-markov-memory.md).

The theorem is correct under its stated scalar, stable-transition,
independent-noise, and fixed-covariance assumptions. I found no mathematical
counterexample. The proof correctly handles the dependence between overlapping
local residuals, and its relative precision sandwich has the correct direction.
The information and design-gap consequences follow. The finite-state model has
the asserted hull and integer-exactness properties, subject to the stated
qualification about extra linking constraints.

I obtained two tighter constants by retaining the finite length of each local
history and then bounding its Kalman gains. These do not establish research
priority or substantial practical value. This review did not perform the
separate prior-art assessment. No literature knowledge-base files were edited.

## 1. Assumptions that the proof needs

Use centered observation errors `E_t=X_t+v_t`. There is one scalar observation
per calendar index, and the scalar transition satisfies `|a_t|<=rho<1`, with
`rho>=0`. Initial state, process innovations, and observation noises are
mutually independent. Their variances are finite, `Var(X_t)<=Pbar`, and
`r_t=Var(v_t)>=rmin>0`. Selection is deterministic and does not alter these
dynamics. The covariance does not depend on the unknown mean parameters.

The positive nugget ensures that every principal observation covariance is
positive definite, even if all process innovations or the entire latent state
have zero variance. Thus all local regressions and the selected true precision
exist. A positive lower bound on process noise is unnecessary. The proof also
allows zero and negative transitions and time-varying variances.

Gaussianity supplies the stated Fisher-information interpretation. The
covariance manipulations themselves use linear prediction and second moments.
Extending the Fisher interpretation beyond the assumed Gaussian model would
require additional arguments.

The local predictor must restart with the **unconditional** marginal at its
first retained observation. Truncating coefficients from the full-history
predictor would define a different approximation. No such substitution occurs
in the draft.

## 2. Independent coefficient and covariance derivation

Let `H_t` be the selected times within the preceding `L` calendar positions.
For a time `j` in that history, process the members of `H_t` in order using
the scalar Kalman recursion. Write `P_j^-` for the prediction variance before
observing `E_j`. Its gain satisfies

```text
0 <= K_j=P_j^-/(P_j^-+r_j) <= kappa,
kappa = Pbar/(Pbar+rmin) <= 1.                       (R1)
```

The upper bound holds because conditioning cannot increase the Gaussian
prediction variance: `P_j^-<=Var(X_j)<=Pbar`. This also covers a zero prediction
variance, in which case the gain is zero.

The coefficient of `E_j` in the prediction of `X_t` is `K_j` times every
intervening transition, times `1-K_h` for the later retained observations.
Consequently,

```text
|b_tj| <= kappa rho^(t-j) <= rho^(t-j).              (R2)
```

For an excluded older observation `j<t-L`, start at the first local observed
time `h`. Before that local update, its covariance with the state prediction
error is `Cov(X_h,E_j)`, whose absolute value is at most
`Pbar rho^(h-j)`. Each transition multiplies this covariance by its scalar
transition. Each observation update multiplies it by `1-K_h`; the fresh
process and measurement noises are independent of `E_j`. The final fresh
noise `v_t` is also independent of `E_j`. Therefore,

```text
|Cov(Z_t,E_j)| <= Pbar rho^(t-j),       j<t-L.       (R3)
Cov(Z_t,E_j) = 0,                      j in H_t.    (R4)
```

If `H_t` is empty, (R3) follows directly from the latent covariance. This
derivation shows why arbitrary signs and zero innovations do not cause a
problem, and why a scalar contraction argument cannot be silently reused
for an arbitrary block observation model.

## 3. Overlapping residuals and tighter row bounds

For selected `s<t`, put `h=t-s`. Expand

```text
Cov(Z_t,Z_s) = Cov(Z_t,E_s)
              - sum_(j in H_s) b_sj Cov(Z_t,E_j).
```

When `h>L`, all terms refer to observations excluded from `H_t`. Put
`d=s-j`; the finite history restricts `d` to `1,...,L`. Equations (R2)–(R3)
give

```text
|Cov(Z_t,Z_s)|
 <= Pbar rho^h [1+kappa sum_(d=1)^L rho^(2d)].       (R5)
```

When `1<=h<=L`, `s` itself is in `H_t`, so the direct term vanishes. The
remaining nonzero terms must satisfy `j<t-L`, equivalently
`L+1-h<=d<=L`. Thus

```text
|Cov(Z_t,Z_s)|
 <= kappa Pbar sum_(d=L+1-h)^L rho^(h+2d).          (R6)
```

In particular, two residuals at distance at most `L` need not be uncorrelated.
An exact example has stationary latent variance one, transition `rho=1/2`,
observation-noise variance one, all three times selected, and `L=1`:

```text
R = [[2, 1/2, 1/4], [1/2, 2, 1/2], [1/4, 1/2, 2]],
Z_2 = E_2-E_1/4,
Z_3 = E_3-E_2/4,
Cov(Z_3,Z_2) = -1/32,
Var(Z_2) = Var(Z_3) = 15/8,
Corr(Z_3,Z_2) = -1/60.
```

Every residual variance is at least `rmin`. For a fixed row there is at most
one other observation at each positive calendar distance on **each** side.
Using both sides, (R5)–(R6) yield the valid uniform constant

```text
delta_gain = (2 Pbar/rmin) rho^(L+1)/(1-rho)
             [1+kappa rho(1-rho^L)/(1-rho)].         (R7)
```

Set this to zero when `rho=0`. The displayed formula itself has that value
when the usual integer-power convention is used.

For clarity, the finite geometric sums with the weaker `kappa=1` coefficient
bound give

```text
delta_finite = (2 Pbar/rmin)
               rho^(L+1)(1-rho^(L+1))/(1-rho)^2.    (R8)
```

One way to check the simplification is to separate the direct far-history
term:

```text
base_tail = (2 Pbar/rmin) rho^(L+1)/(1-rho),
delta_gain = base_tail+kappa(delta_finite-base_tail).
```

The draft's original constant is larger because it extends finite sums to
infinity. All three are valid, and

```text
delta_gain <= delta_finite <= delta_draft
           <= (2 Pbar/rmin) rho^(L+1)/(1-rho)^2.
```

The gain refinement can help when observation noise is large relative to the
latent variance. These constants remain conservative. If `L>=n-1`, the
approximation is exactly the full-history factorization, so its actual error
is zero even when one of the displayed uniform bounds is positive.

## 4. Spectral, information, and design conclusions

Let `A` be the selected residual transformation and `D` its diagonal residual
variance matrix. Both are nonsingular: `A` is unit triangular and `D` is
positive diagonal. The row bounds and symmetry imply

```text
||D^(-1/2) A R_SS A^T D^(-1/2)-I||_2 <= delta.
```

The precision conclusion is not obtained by incorrectly inverting this
display. Instead put `B=D^(-1/2) A R_SS^(1/2)`. The residual covariance is
`B B^T`, whereas `R_SS^(1/2) Q R_SS^(1/2)=B^T B`. These two positive-definite
matrices have the same eigenvalues. Consequently,

```text
(1-delta) R_SS^(-1) <= Q <= (1+delta) R_SS^(-1).     (R9)
```

This is correct for any of the valid row constants above. When `delta>=1`,
the lower bound is still a true matrix inequality but gives no positive
relative lower approximation guarantee.

Congruence by any finite sensitivity matrix `F_S`, and addition of a fixed
positive-semidefinite prior `J0`, preserve the sandwich with factors
`1±delta`. A strictly positive-definite prior makes all log determinants
well defined, including the empty design. For `delta<1`, the resulting
logdet error is between `p log(1-delta)` and `p log(1+delta)`.

Thus a valid upper bound `U_L` on the surrogate design maximum gives the
true-design upper bound `U_L-p log(1-delta)`. A feasible selection whose
surrogate objective is within `tau` of the surrogate optimum has true
suboptimality at most `tau+p log((1+delta)/(1-delta))`. These statements need
an actual feasible selection; a fractional mixture of designs is not an
incumbent selection. The draft makes the necessary numerical-bound
qualification.

Independent scalar chains can be added before applying a maximum of their
individual constants. Shared budget or selection restrictions do not change
this argument because the bounds already hold for every selection subset.
It would be invalid to extend this assertion to mutually correlated chains
without a new proof.

## 5. Finite-state formulation

At stage `t`, the previous `L` calendar selection bits determine exactly the
local covariance regression and the information contribution of choosing
time `t`. Earlier bits have no further effect on this surrogate. Each
complete selection sequence therefore defines one path in the layered mask
graph, and every source-to-sink path defines one selection sequence. Its
information is the sum of the corresponding choose-arc matrices plus `J0`.

Every nonnegative unit flow in an acyclic graph decomposes into a convex
combination of such paths. Projecting arc flow onto visits and the affine
information matrix consequently gives exactly the convex hull of surrogate
selection/information pairs. If every visit marginal is binary, every path
with positive weight must choose exactly those visits. The mask evolution is
deterministic, so the paths coincide. This proves integer exactness with
continuous arc variables.

The hull statement concerns the information graph, not the logdet hypograph.
Adding a fixed-count state preserves the corresponding count-restricted
graph hull. General external linking constraints preserve integer exactness
but need not preserve a continuous convex-hull description.

The complexity is `O(n 2^L)`. The draft's original literal statement of at
most `n 2^L` states omits the final mask layer if it is explicitly retained.
One safe explicit count is at most `(n+1)2^L+1` states and
`2n2^L+2^L` arcs. Alternatively, terminal decisions can connect directly to
the sink. This is a counting-wording correction, not a formulation defect.

Reindexing a selected subsequence gives a valid analogous last-`m`-selected
memory theorem: a transition across a nonempty calendar gap still has
modulus at most `rho`, and the aggregated process innovations remain
independent. Its straightforward state must also record the retained
calendar indices, so it does not have the same `O(n 2^m)` size bound.

## 6. Independent numerical verification

The review implementation is
[review_noisy_markov_independent.py](../code/research_20260912/review_noisy_markov_independent.py).
It imports no author implementation or proposed production solver. It
constructs latent covariances from independent innovation loadings and
obtains local regressions from dense principal submatrix solves.

Run from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_noisy_markov_independent.py
```

The project environment and lockfile record the dependencies. The output is
[noisy-markov-independent-validation.json](../code/research_20260912/noisy-markov-independent-validation.json).
Both the finite-window-bound run and the stronger gain-based-bound run passed:

- 29 covariance families with eight candidate times each, including stationary
  transitions from zero to `0.985`, three nugget levels, signed nonstationary
  transitions, zero transitions, degenerate process innovations, deterministic
  latent evolution, and the zero latent process.
- Every nonempty selected subset and every `L=0,...,8`: 66,555 local models.
- 311,808 retained regression coefficients, 155,904 excluded covariances,
  467,712 residual pairs, and all normalized row/spectral bounds.
- 66,555 prior-augmented Fisher checks, including generalized eigenvalues of
  `(Q,R_SS^(-1))`, the independent information-contribution expansion, and
  every applicable two-sided logdet bound.
- 1,088 LP comparisons between the mask graph and exhaustive selected-subset
  enumeration, across `L=0,1,2,4`, unrestricted or layered counts
  `0,1,3,7`, random linear information/visit objectives, and fixed binary
  visit vectors. The maximum objective discrepancy was `1.1e-14`.
- Direct finite-series checks at 53 contraction values through `0.9999` and
  31 window lengths, plus the exact overlapping-residual example above.

The saved report uses the stronger gain-based bounds. Its largest coefficient,
excluded-covariance, residual-pair, and precision-sandwich excesses were all at
most `2.3e-16`. No row, spectral, or logdet bound violation occurred; the
information-expansion discrepancy was at most `8.6e-14`. Numerical testing
supports the formal derivation; it is not interval arithmetic, a proof of
newness, or a benchmark demonstrating useful runtime or solution-quality
improvements.

## 7. Remaining work and scope

No theorem-correctness blocker remains within the stated scalar model.
Preserve the known-covariance and scalar-observation restrictions, both sides
of each row sum, and the distinction between a surrogate Gaussian model and
the true information. The finite-sum and gain refinements are safe optional
improvements. The substantive unresolved questions are prior art and whether
the certified window lengths lead to a useful optimization method on
meaningful cases.

## 8. Additional review: full vector blocks after noise whitening

The parent researcher and draft author subsequently proposed the full-block
extension now included in the source note. I independently checked that
extension. It is sound under its explicit contraction condition in coordinates
where the measurement noise has identity covariance. The scalar review above
remains unchanged.

Let every selected candidate reveal the complete `d`-dimensional block
`Y_t=m_t(theta)+X_t+v_t`, with state transition
`X_t=A_t X_(t-1)+w_t` and independent measurement covariance `V_t>0`. Keep
the stated Gaussian and independence assumptions. Define the deterministic,
time-dependent coordinate change

```text
W_t=V_t^(-1/2),
X'_t=W_t X_t,
E'_t=W_t(Y_t-m_t),
F'_t=W_t F_t,
T_t=W_t A_t W_(t-1)^(-1).
```

The hypotheses are

```text
||T_t||_2 <= rho < 1,
Cov(X'_t) <= beta I.
```

Whitening does not create correlations between different independent noise
blocks. The transformed process innovation is `W_t w_t`, still independent
of the other innovations and observation noises. Thus the transformed model
is a valid vector state-space model with measurement noise covariance `I`.
Time variation of `W_t` is fully accounted for by `T_t`; there is no omitted
transition factor.

For each local filter, its prediction covariance satisfies
`0<=P^-<=Cov(X'_t)<=beta I`. Because the observation noise is `I`, its gain
is the symmetric matrix

```text
K=P^-(P^-+I)^(-1),
0<=K<=kappa I,       kappa=beta/(beta+1),
0<=I-K<=I.
```

Gains at different times need not commute with each other or with the
transitions. The proof uses only the submultiplicative operator norm, so
noncommutativity does not invalidate it. In particular, a retained regression
coefficient is a correctly ordered product of intervening transitions,
later factors `I-K`, and the gain at the retained observation, giving
`||b_tj||_2<=kappa rho^(t-j)`.

For an excluded older observation, the initial cross covariance is a product
of transitions times `Cov(X'_j)`, so its norm is at most
`beta rho^(h-j)`. Each subsequent transition and local update acts by left
multiplication with the same bounded factors as in the scalar proof. Thus
`||Cov(Z_t,E'_j)||_2<=beta rho^(t-j)`. Included-history cross-covariance blocks
are zero by regression orthogonality.

The residual-pair expansion must retain the matrix orientation:

```text
Cov(Z_t,Z_s) = Cov(Z_t,E'_s)
              -sum_(j in H_s) Cov(Z_t,E'_j) b_sj^T.
```

Applying operator norms to this identity gives exactly the scalar majorants
(R5)–(R6), with `Pbar=beta`. Each residual covariance block `D_t` is at least
`I`, so multiplying on either side by `D_t^(-1/2)` cannot increase the block
norm.

Let `E=C_L-I`. Its diagonal blocks are zero. Define the ordinary symmetric
nonnegative matrix `M` by `M_ts=||E_ts||_2`. For any block vector `u`, put
`v_t=||u_t||_2`. Then

```text
||(Eu)_t||_2 <= (Mv)_t,
||Eu||_2 <= ||M||_2 ||u||_2,
||M||_2 <= max_t sum_s M_ts.
```

Both sides of each calendar row give the same bound as before:

```text
delta_block = 2 beta rho^(L+1)/(1-rho)
              [1+kappa rho(1-rho^L)/(1-rho)].
```

There is no explicit multiplier depending on block size `d`. The assumption
`Cov(X'_t)<=beta I` may of course require a larger `beta` in a different
physical model. The relative precision sandwich follows from the same
`B B^T` versus `B^T B` argument in the full selected dimension.

For a selected block set `S`, write `W_S` for the block-diagonal coordinate
change. Then `R'_SS=W_S R_SS W_S^T` and `F'_S=W_S F_S`, which directly proves

```text
F'_S^T (R'_SS)^(-1) F'_S = F_S^T R_SS^(-1) F_S.
```

The local residuals transform as `Z'_t=W_t Z_t`, with
`D'_t=W_t D_t W_t^T` and `G'_t=W_t G_t`. Hence
`G'_t^T (D'_t)^(-1)G'_t=G_t^T D_t^(-1)G_t`: the surrogate information also
is invariant. Its choose-arc contribution is the positive-semidefinite
`p`-by-`p` matrix `G_t^T D_t^(-1)G_t`. Complete block selection still uses one
bit per calendar candidate, so the graph proof is unchanged. The logdet
factor remains `p`, the number of mean parameters, not `d`.

The contraction condition must be checked after whitening. An unwhitened
Euclidean gain need not be a contraction: with

```text
P=diag(100, 0.01),
V=[[1, 0.9], [0.9, 1]],
K=P(P+V)^(-1),
```

the spectral norms of `K` and `I-K` are approximately `1.33679` and `1.33081`.
This is not a counterexample to the whitened theorem; it illustrates why the
additional metric condition and identity observation-noise covariance are
needed for this proof. Arbitrary partial block selection or observation
matrices `H_t` are not covered.

### Independent block checks

The separate implementation
[review_noisy_markov_blocks.py](../code/research_20260912/review_noisy_markov_blocks.py)
imports no author implementation. It generates noncommuting transitions and
latent covariances directly in whitened coordinates, assigns independently
varying positive-definite observation noise matrices, constructs the original
model, and then recovers its whitened covariance through an independent dense
calculation.

Run it with:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_noisy_markov_blocks.py
```

The report is
[noisy-markov-block-independent-validation.json](../code/research_20260912/noisy-markov-block-independent-validation.json).
The suite covers 20 six-candidate covariance families with block sizes two
and three, transition norms through `0.96`, time-varying non-diagonal noise,
zero transitions, zero process innovations, and zero latent variance. It
checks every nonempty block subset at every `L=0,...,6`:

- 8,820 subset/window models and Fisher-information checks;
- 22,400 regression-coefficient blocks;
- 11,200 excluded cross-covariance blocks;
- 33,600 residual pairs, plus the block comparison-matrix bound, the full
  normalized spectral bound, and generalized precision eigenvalues;
- true and surrogate information invariance under whitening, and the sum of
  local block information contributions.

The run passed all checks. Its maximum transition/marginal covariance
commutator norm exceeded two, confirming that the test was not restricted to
commuting examples. The independently reconstructed covariance error was at
most `1.1e-14`; true-information whitening error was at most `1.6e-13`.
Precision, spectral, and logdet excesses were below `4.5e-15`.
Surrogate-information invariance error was at most `1.5e-13`. These are
floating-point checks supporting the formal argument, not verified interval
certificates or evidence of newness.

## 9. Additional review: full-calendar innovation normalization

The author subsequently proposed replacing the generic residual-variance
lower bound by the smallest innovation variance from observing every earlier
calendar candidate. This refinement is also sound.

For the scalar model, define

```text
Dfull,t = Var(E_t | E_1,...,E_(t-1)),
d_star <= min_t Dfull,t.
```

For the whitened complete-block model, use conditional covariance matrices
and require `d_star<=min_t lambda_min(Dfull,t)`. In either case choose a
positive lower bound `d_star`; the generic noise lower bound is always an
available fallback within the theorem's assumptions.

Every local history is a subset of the earlier calendar observations.
Gaussian conditioning order therefore gives

```text
D_(t,H) >= Dfull,t >= d_star I.
```

This statement is independent of the selected subset, including any
installation or budget restrictions. The full observation sequence is used
only to calculate a covariance lower bound; it need not be a feasible
experimental design. The matrices can be computed with one full-calendar
Kalman sweep.

The normalized residual-pair bounds consequently divide by `d_star`.
Replace the **leading** normalization denominator `rmin` in (R7)–(R8), or
the denominator one in the whitened block bound, by `d_star`. Keep the gain
cap `kappa=Pbar/(Pbar+rmin)` or `beta/(beta+1)` unchanged. That cap concerns
the measurement-noise covariance in a Kalman update; it is not obtained by
substituting a residual variance for measurement noise.

For a stationary scalar model with latent variance one, measurement-noise
variance one, and transition magnitude `rho`, the prediction variance obeys

```text
s_1=1,
s_(t+1)=rho^2 s_t/(s_t+1)+(1-rho^2).
```

Its nonnegative fixed point is `sqrt(1-rho^2)`. The update is increasing in
`s`, preserves the interval above this fixed point, and decreases `s` in that
interval. Hence the analytic choice

```text
d_star = 1+sqrt(1-rho^2)
```

is valid for every finite horizon. It can be used directly without relying on
the numerical lower accuracy of a covariance eigenvalue computation.

A computed minimum eigenvalue is an estimate of `d_star`; obtaining a formal
floating-point certificate requires a valid lower error allowance or a
verified calculation. This does not affect the exact-arithmetic theorem.

The final block verification script additionally checks the full Loewner
inequality `D_(t,H)>=Dfull,t` for every retained block in all 8,820 local
models, and checks the resulting smaller spectral and information bounds.
The saved JSON identifies this strengthened normalization explicitly.
