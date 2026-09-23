# Uniform finite-history approximation for noisy Markov design

Date: 2026-09-12. Status: scalar theorem and full-block extension passed fresh
independent proof review and separate numerical checks. Publication
priority and practical value are not established. No production
Markov solver is changed by this investigation. The full-observation exact
hull was found to be known; see the
[priority audit](research-20260912-markov-priority-audit.md).

The candidate capability is a certified finite-history MINLP for scalar
Gauss–Markov errors observed with independent measurement noise. The
approximation is the established Vecchia conditional approximation. The
potentially useful bridge is a spectral bound uniform over *every* selected
subset, followed by a finite-state optimization model and a true D-optimal
upper certificate. Its constants are conservative; large correlation may
make the required state space prohibitive.

The [independent review](research-20260912-noisy-markov-independent-review.md)
checks the scalar proof and improves its constant. It reports 66,555
independent subset/window checks and 1,088 graph LP checks without a defect.
Its separate full-block suite passed 8,820 subset/window models with
noncommuting transitions and time-varying, non-diagonal observation noise.

## 1. Model and approximation

There is one scalar observation candidate at each calendar index `1,...,n`:

```text
Y_t = m_t(theta)+X_t+v_t,
X_t = a_t X_(t-1)+w_t,                t=2,...,n.
```

All errors are jointly Gaussian and centered; `X_1`, the process innovations
`w_t`, and the measurement noises `v_t` are mutually independent. Assume

```text
|a_t| <= rho < 1,
Var(X_t) <= Pbar,
Var(v_t) = r_t >= rmin > 0.
```

Process variances can be zero. Covariance parameters are known and fixed with
respect to the mean parameter `theta`. Let `F_t` be the row derivative of
`m_t` at the chosen nominal parameter, with `p` columns. Neither a bound on
`F_t` nor a positive lower bound on process noise is needed below. Sampling is
deterministic and does not change the dynamics. Negative/time-varying
transitions and nonstationary variances are allowed.

Fix any selected subset `S` and an integer window `L>=0`. At each selected
time `t`, define the selected recent history

```text
H_t(S) = S intersect {max(1,t-L),...,t-1}.
```

Use the true error covariance `R` to form local regression coefficients and
conditional variances

```text
b_t = R_(t,H_t) R_(H_t,H_t)^{-1},
d_t = R_tt-R_(t,H_t) R_(H_t,H_t)^{-1} R_(H_t,t),
Z_t = (Y_t-m_t)-sum_(j in H_t) b_tj (Y_j-m_j).
```

Empty histories have no regression term and `d_t=R_tt`. Let `A_L(S)` be the
unit lower-triangular map from selected errors to `Z`, and let `D_L(S)` be the
diagonal matrix of the `d_t`. The normalized local residual covariance and
Vecchia precision are

```text
C_L(S) = D_L^{-1/2} A_L R_SS A_L^T D_L^{-1/2},
Q_L(S) = A_L^T D_L^{-1} A_L.
```

The diagonal of `C_L` is exactly one. The approximate information is

```text
J_L(S) = J0+F_S^T Q_L(S) F_S
       = J0+sum_(t in S) G_(t,H_t)^T G_(t,H_t)/d_t,
G_(t,H_t) = F_t-sum_(j in H_t) b_tj F_j.               (1)
```

This is the information of a proper Gaussian working model formed by the
product of the local conditional densities. It is not asserted to be the
true Fisher information or the sandwich covariance information of an
estimator under misspecification. The true mean Fisher matrix is
`J(S)=J0+F_S^T R_SS^{-1}F_S`.

## 2. Uniform spectral theorem

Define

```text
delta_L = (2 Pbar/rmin)
          rho^(L+1)(1-rho^(L+1))/(1-rho)^2
        <= (2 Pbar/rmin) rho^(L+1)/(1-rho)^2.           (2)
```

This constant retains finite geometric sums, as suggested and independently
checked by the fresh mathematical reviewer. It tightens the first draft's
infinite-sum constant. For `rho=0`, set `delta_L=0`. Under §1's assumptions, for every nonempty
subset `S`,

```text
||C_L(S)-I||_2 <= delta_L,
(1-delta_L) R_SS^{-1} <= Q_L(S)
                       <= (1+delta_L) R_SS^{-1}.     (3)
```

Inequalities between symmetric matrices are in the positive-semidefinite
order. The first statement is useful without requiring `delta_L<1`; the
second lower bound becomes useful when `delta_L<1`. The bound contains no
`n`, `|S|`, sensitivity norm, or minimum prior eigenvalue.

### Proof, step 1: local regression coefficients and excluded observations

Within `H_t`, calculate the scalar Kalman predictor starting with the
unconditional marginal variance at its first member. At an observed index
`j`, the gain is `K_j=P_j^-/(P_j^-+r_j)`, so `0<=K_j<=1`. Across a gap the
transition is the product of the calendar transitions. The contribution of
`Y_j-m_j` to the prediction at `t` is its gain, multiplied by all intervening
transitions and factors `1-K_h` at later observations in `H_t`. Hence

```text
|b_tj| <= rho^(t-j),                    j in H_t.     (4)
```

For an excluded selected `j<t-L`, propagate covariance of the filter error
with `Y_j-m_j`. At the first local observation, update multiplies that
covariance by `1-K_h`; each subsequent transition and update does the same
kind of multiplication. New process and observation noises are independent
of the older `Y_j`. Also
`|Cov(X_h,Y_j-m_j)|<=Pbar rho^(h-j)`. Therefore

```text
|Cov(Z_t,Y_j-m_j)| <= Pbar rho^(t-j),    j<t-L.       (5)
```

The same bound holds if `H_t` is empty, directly from latent covariance decay.
For selected `j in H_t`, the covariance is exactly zero by linear regression
orthogonality. All bounds use absolute values, so signs of transitions cause
no change. The use of an unconditional initial local marginal is essential:
these are coefficients of the stated local conditional, not full-history
filter coefficients silently truncated.

### Proof, step 2: residual pairs including overlapping histories

Take selected `s<t` and let `h=t-s`. From the definition of `Z_s`,

```text
Cov(Z_t,Z_s) = Cov(Z_t,Y_s-m_s)
              -sum_(j in H_s) b_sj Cov(Z_t,Y_j-m_j).
```

If `h>L`, apply (4)–(5) to `s` and all of `H_s`, retaining that
`s-L<=j<s`:

```text
|Cov(Z_t,Z_s)|
 <= Pbar rho^h(1-rho^(2L+2))/(1-rho^2).             (6a)
```

If `1<=h<=L`, then `s in H_t`, so the first covariance is zero. The terms
with `j>=t-L` are also zero, but older terms in `H_s` need not vanish.
For the remaining terms put `L+1-h<=d=s-j<=L` and use (4)–(5):

```text
|Cov(Z_t,Z_s)|
 <= Pbar sum_(d=L+1-h)^L rho^(h+2d)
  = Pbar rho^(2L+2-h)(1-rho^(2h))/(1-rho^2).        (6b)
```

This explicitly handles the overlapping-window cross terms. Simply declaring
all residuals within a window uncorrelated would be incorrect.
For example, `rho=1/2`, unit latent/noise variances, all three times selected,
and `L=1` give `Cov(Z_3,Z_2)=-1/32`, as independently supplied by the reviewer.

### Proof, step 3: both sides of each row and the precision sandwich

Every `d_t>=rmin`. For a fixed row, there is at most one other candidate at
each positive calendar distance on either side. Equations (6a)–(6b) therefore
give

```text
sum_(s!=t) |(C_L)_ts|
 <= [2 Pbar/(rmin(1-rho^2))]
    [sum_(h=1)^L rho^(2L+2-h)(1-rho^(2h))
     +(1-rho^(2L+2)) sum_(h=L+1)^infinity rho^h]
  = delta_L.
```

The matrix is symmetric. Gershgorin's theorem, or its absolute row-sum norm,
bounds every eigenvalue of `C_L` within `delta_L` of one. With
`B=D_L^{-1/2} A_L R_SS^{1/2}`, we have `C_L=B B^T` and
`R_SS^{1/2} Q_L R_SS^{1/2}=B^T B`. Since `B` is square and invertible, these
two SPD matrices have the same eigenvalues. Congruence by `R_SS^{-1/2}`
proves (3).

### Reviewed refinement using the gain bound

Each local prediction variance is at most the unconditional variance, so
`K_j<=kappa=Pbar/(Pbar+rmin)`. Thus (4) can be strengthened to
`|b_tj|<=kappa rho^(t-j)`. In (6a), retain the direct term
`Pbar rho^h` and multiply only its regression sum by `kappa`; multiply all of
(6b) by `kappa`. The resulting row bound is

```text
delta_gain = (2 Pbar/rmin) rho^(L+1)/(1-rho)
             [1+kappa rho(1-rho^L)/(1-rho)]
           = base_tail+kappa(delta_L-base_tail),
base_tail = (2 Pbar/rmin)rho^(L+1)/(1-rho).            (2g)
```

It is no larger than (2), and can replace `delta_L` in every conclusion.
The independent reviewer derived this refinement and checked it separately.
The table below keeps (2) for direct reproducibility with the author script;
an implementation should use the tighter certified constant (2g).

Another elementary refinement uses a uniform lower innovation variance:

```text
d_star = min_t Var(Y_t | Y_1,...,Y_(t-1)).
```

One full-grid Kalman sweep computes it. Conditioning on all earlier candidates
gives no larger a variance than conditioning on `H_t(S)`, so every local
`d_t>=d_star>=rmin`. Replace the leading normalization denominator `rmin` in
(2) and (2g) by `d_star`, while retaining
`kappa=Pbar/(Pbar+rmin)`. No new assumption is needed. The independent reviewer
accepted this refinement separately. A computed `d_star` must be rounded down
with an appropriate numerical error allowance before serving as a formal
certificate.

For stationary unit latent and measurement variances, the full-grid scalar
prediction variance decreases to `sqrt(1-rho^2)`, by the scalar Riccati fixed
point. Hence `d_star>=1+sqrt(1-rho^2)` uniformly in `n`. At `rho=0.6`, this
refinement lowers the first window satisfying `delta_gain<=0.05` from `L=10`
to `L=8`, reducing the maximum mask count from 1,024 to 256. These are model
size estimates, not optimization runtime measurements.

### Full observed blocks after noise whitening

The following extension uses a stronger, explicit stability metric. The fresh
reviewer checked its proof and ran separate noncommuting numerical examples.
Let each candidate be a complete `d`-vector block:

```text
Y_t=m_t(theta)+X_t+v_t,
X_t=A_t X_(t-1)+w_t,
Cov(v_t)=V_t>0.
```

The independence and Gaussian assumptions remain the same. Define the
time-dependent coordinates

```text
X'_t=V_t^(-1/2)X_t,
F'_t=V_t^(-1/2)F_t,
T_t=V_t^(-1/2)A_t V_(t-1)^(1/2).
```

Assume `||T_t||_2<=rho<1` and `Cov(X'_t)<=Pbar I`. In these coordinates each
measurement noise has covariance `I`. Thus every local Kalman gain is
`K=P^-(P^-+I)^(-1)`, symmetric, with `0<=K<=kappa I`, where
`kappa=Pbar/(Pbar+1)`, and `0<=I-K<=I`.

Apply the definitions above using block matrices and replace the scalar
increment in (1) by `G_(t,H)^T d_(t,H)^(-1)G_(t,H)`. Each block coefficient
is a product of transitions, gains, and later update factors. Submultiplicativity
gives `||b_tj||_2<=kappa rho^(t-j)` despite noncommuting factors. Propagating
the covariance with an excluded old observation similarly gives
`||Cov(Z_t,Y'_j-m'_j)||_2<=Pbar rho^(t-j)`. Regression orthogonality still
annuls every included-history block. In the residual-pair expansion use the
oriented term `Cov(Z_t,Y'_j-m'_j) b_sj^T`. The proof of (6a)–(6b) now bounds block
operator norms, with the same scalar majorants and gain refinement.

Each local conditional covariance satisfies `d_t>=I`. Hence block-normalizing
does not enlarge these norms. The symmetric matrix `C_L-I` has zero diagonal
blocks. For a block vector `u`, apply the scalar matrix of block operator norms
to the vector with entries `||u_t||_2`. Its maximum row sum bounds
`||C_L-I||_2`. This proves (3) with (2) or (2g), `rmin=1`, and no multiplier
depending on `d`. The `B B^T` versus `B^T B` argument is unchanged. Invertible
noise whitening preserves true and surrogate mean information when `F` is
whitened too. Therefore the optimization conclusions and calendar-mask graph
extend to complete block selection.

The innovation-variance refinement also extends: compute
`d_star=min_t lambda_min(Cov(Y'_t | Y'_1,...,Y'_(t-1)))` and replace the
leading denominator `1` by `d_star>=1`, keeping the same gain bound.

This includes coupled latent dynamics and within-block correlated measurement
noise. Merely assuming `||A_t||_2<1` before whitening does not establish the
required metric contraction. Arbitrary partial observation `H_t X_t` is not
covered, and the selected block must be observed in full.

## 3. Certified design optimization

Assume `J0>0` and `delta_L<1`. Congruence of (3) by any `F_S`, followed by
addition of the fixed prior, gives

```text
(1-delta_L) J(S) <= J_L(S) <= (1+delta_L) J(S).
```

It follows that

```text
p log(1-delta_L)
 <= logdet J_L(S)-logdet J(S)
 <= p log(1+delta_L).                               (7)
```

Let `U_L` be a mathematically valid upper bound for the maximum surrogate
logdet over the permitted design family. Then

```text
max_S logdet J(S) <= U_L-p log(1-delta_L).           (8)
```

An exactly evaluated feasible incumbent supplies the lower bound. If the
surrogate incumbent has logdet optimality gap at most `tau`, its true logdet
suboptimality is at most

```text
tau+p log[(1+delta_L)/(1-delta_L)].                  (9)
```

The empty schedule has `J=J_L=J0` and satisfies these conclusions. Independent
scalar chains add their matrices; using the maximum chain `delta_L` gives
the same global sandwich. The design family can contain arbitrary linear
budgets, installation costs, counts, minimum gaps, and mandatory decisions,
because the approximation bound holds before imposing those constraints.
Actual floating-point certificates require the normal solver/numerical
qualifications; (8) does not certify an unvalidated solver bound.

A useful prior-aware bound is sharper than the blanket shift in (8). Write
`A_L(S)=J_L(S)-J0`. The data-information sandwich gives

```text
J(S) <= J0+A_L(S)/(1-delta_L).                      (10)
```

Therefore maximizing the logdet of the affine corrected information in (10)
over the same graph relaxation supplies a true-design upper bound. Its optimum
is no larger than `U_L-p log(1-delta_L)` when `U_L` is the optimal value of
the same uncorrected relaxation, because
`J0+A/(1-delta_L) <= (J0+A)/(1-delta_L)`. Any valid upper bound for this
corrected optimization is also usable.

For example, at an SPD surrogate mixture `M`, put
`N=J0+(M-J0)/(1-delta_L)`. A single logdet tangent gives

```text
logdet N-p+tr(N^(-1)J0)
  + max_allowed_path sum_arc tr(N^(-1)W_arc)/(1-delta_L).  (11)
```

This is a valid true-design upper bound if the path maximum is exact or has a
certified upper bound. The same count-aware dynamic program prices the rescaled
arc matrices. Equations (10)–(11) are elementary order and concavity
consequences, included for practical use rather than as separate novelty claims.

## 4. Finite-state formulation and calendar versus selected memory

At stage `t`, the state records the preceding `L` selection bits. A skip arc
shifts in zero and contributes no information. A choose arc shifts in one
and contributes the PSD term in (1), precomputed from that bitmask's history.
The source state is the all-zero history; all final masks connect to the sink.
There are `O(n 2^L)` states and arcs, including source and terminal layers.
There are at most `2 n 2^L` decision arcs, plus the terminal connections.
Unit flow gives
the exact graph hull of the *surrogate* information without extra linking
constraints. Binary calendar-visit marginals force a unique selection
sequence and therefore a unique path. General linking constraints preserve
integer exactness; they need not preserve the continuous hull.

The objective is logdet of affine PSD information, so this gives a convex
MINLP with ordinary selection/installation binaries. A fixed count can be
handled by a further count layer. Forbidden/mandatory decisions and minimum
gaps can remove arcs or states. Linear surrogate pricing is a longest-path
dynamic program, including count states when needed.

Conditioning on the last `m` *selected* observations instead gives a valid
analog of the theorem after reindexing that subset, since a selected gap has
transition modulus at most `rho`. But its straightforward state contains an
ordered tuple of up to `m` selected calendar times, requiring
`O(n^(m+1))` states/arcs in the crude enumeration. Calendar memory instead
has a fixed binary window and `O(n2^L)` size. These should not be confused.

For physical-time sampling, a uniform candidate spacing lower bound is one
way to obtain `rho<1` per calendar index. Refining a continuous-time grid
makes `rho` closer to one and can make this result computationally weak.
Multiple scalar observations at one time cannot simply be treated as
successive indices satisfying the same strict contraction bound.

A simple boundary counterexample shows why strict decay matters. Let a single
latent random intercept persist forever: `X_t=X`, with `Var(X)=1`, independent
measurement variances one, and constant mean sensitivity `F_t=1`. For all `n`
observations, `R=I+11^T`, so true added information is `n/(n+1)`. For fixed
window `L` and `n>=L`, the local-history surrogate instead has added information

```text
L/(L+1)+(n-L)/[(L+1)(L+2)].
```

The first `L` increments telescope; each later local conditional has the same
positive increment `1/[(L+1)(L+2)]`. Thus the surrogate information grows
linearly with `n` while true information stays below one. No fixed-window
horizon-uniform relative Fisher bound is possible in this class with `rho=1`.
Adding a fixed SPD prior does not prevent its unbounded logdet error. This is
a limitation of the model class without strict decay, not a counterexample
to the theorem.

## 5. Prior work and limitations of the current claim

The working model is Vecchia's established conditional-density truncation.
[Schäfer, Katzfuss, and Owhadi, 2021](https://arxiv.org/abs/2004.14455), DOI
10.1137/20M1336254, gives KL-optimal sparse inverse Cholesky factors and
rigorous approximation results for a broad kernel class. Its §4.1 discusses
added measurement noise and a different latent-factor strategy. Primary
Theorem 3.4 and §4.1 were inspected. Sparse inverse approximation, conditional
factorization, and exponential decay are not claimed as new here.

[Kozdoba, Marecek, Tchrakian, and Mannor, 2019](https://arxiv.org/abs/1809.05870)
proves finite-history prediction approximation through Kalman exponential
forgetting. Its primary Theorems 1–2 were inspected. The scalar proof above
instead uses the stronger assumption of strict stable transitions to get an
explicit covariance bound for all selection patterns, including empty windows
and degenerate process innovations. This distinction alone does not establish
a substantial theoretical advance.

[Katzfuss and Guinness, general Vecchia framework](https://arxiv.org/abs/1708.06302),
primary §2, explicitly includes noisy observations, subsets, and local
conditional factorizations. Therefore handling a subset in the definition of
the working model is also established. [Demko, Moss, and Smith, 1984](https://www.ams.org/mcom/1984-43-168/S0025-5718-1984-0758197-9/S0025-5718-1984-0758197-9.pdf)
is foundational prior for exponential inverse decay.
[Huan et al., 2025](https://arxiv.org/abs/2307.11648), DOI
10.1137/23M1606253, connects conditional neighborhood selection with experimental
design. Primary §§1–3 and 7.1 were inspected: it chooses sparse-factor
conditioning neighborhoods through greedy conditional mutual information,
including multiple target points. It does not present the subset-uniform
calendar-mask design certificate above in these sections. Its introduction
also identifies Vecchia's factors with factorized sparse approximate inverse
(FSAI) preconditioners, crediting Kaporin (1990) and Yeremin, Kolotilina, and
Nikishin (2000), DOI 10.1007/BF02672769. Those original sources remain unread
and are a priority branch for further audit of relative spectral bounds.

[Szabo and Zhu](https://arxiv.org/abs/2410.10649) develops Vecchia-process
probabilistic theory and regression contraction rates; its primary abstract
was read. [Zhang, Tang, and Banerjee, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11444644/)
studies covariance-parameter inference under fixed-domain asymptotics; primary
§3/Theorem 2 was inspected. These provide relevant approximation theory in
different asymptotic settings. [Block Vecchia, 2025](https://marcgenton.github.io/2025.PAGS.Technometrics.pdf)
also makes clear that using vector local conditional factors is established.
This original source audit did not complete that paper's theorem comparison;
the [literature report index](research-20260912-literature-report-index.md)
records the later acquisition status. This source-reading qualification is
separate from the accepted review of the repository's full-block theorem.
No novelty is claimed for block conditional factorization itself.

[Shi and Chen, 2013](https://doi.org/10.1016/j.sysconle.2013.04.012),
*Optimal periodic scheduling of sensor networks: A branch and bound approach*,
is direct conceptual prior for certifying optimization with an approximation
error bound. Its primary abstract and introduction describe a moving cost
approximation with an exponential uniform error bound, used to prune a search
for optimal periodic Kalman schedules. The objective is average prediction
variance in periodic steady state. Full text was not retrieved in this audit,
so its exact hypotheses and construction remain unread. Consequently,
combining forgetting, approximation, and certified sensor optimization must
not be described as a new general strategy.

[Vitus et al., 2012](https://www.michaelvitus.net/pubs/VZAHT_Automatica_2012.pdf),
DOI 10.1016/j.automatica.2012.06.092, gives exact and approximate tree pruning
for finite-horizon Kalman sensor scheduling, with an analytical suboptimality
bound. The primary conference predecessor's formulation and pruning theorems,
and the journal paper's abstract, were read. These are established competitors
for weighted-trace state-estimation objectives.

[Dutta, Wilde, and Smith, 2023](https://arxiv.org/abs/2304.02692), version 2,
uses linear estimator coefficients to formulate selection under polyhedral
constraints as an indicator MIQP. Primary §IV-A, Lemma 2 and Theorem 1 were
read. Its objective is weighted trace of Kalman state covariance. It is a
relevant exact-method baseline, but its convex quadratic objective is not
the D-optimal logdet objective considered here.

The currently interesting claim to audit is the combination of subset-uniform
relative Fisher control, the calendar-mask convex MINLP, and a computable
true-design bound. A broad citation search has not yet established priority.
Scalar proof review has passed. A deeper priority search and small-window
computational viability are required before treating it as a selected research
contribution.

The unrestricted vector/partial-observation case is not proved here. A block
update `I-KH` need not have Euclidean operator norm at most one. The full-block
extension in §2 imposes contraction after noise whitening, which makes its
gain argument valid. Replacing scalar absolute values by matrix norms without
these additional assumptions is invalid. Covariance-parameter Fisher
derivatives are outside this theorem.

All newly identified literature was routed to the sole maintenance agent
`/root/literature`, using absolute project, skill, and KB paths. This
investigation does not edit the literature knowledge base.

## 6. Verification and practical thresholds

The standalone check
[noisy_markov_memory_check.py](../code/research_20260912/noisy_markov_memory_check.py)
imports no production Markov solver. It checks every one of the 511 nonempty
subsets of five nine-candidate models at windows `L=0,...,6`: stationary
correlations 0.4, 0.6, and 0.9; a signed nonstationary chain with a zero
transition; and stable signed deterministic latent evolution with zero process
noise. All 17,885 subset/window checks passed. The checks include individual
regression, old-observation covariance, overlapping-residual covariance, and
spectral inequalities. This supplies numerical evidence, not a proof.

Reproduce in the existing isolated environment:

```bash
cd code/research_20260912
uv run --frozen noisy_markov_memory_check.py
```

The [JSON report](../code/research_20260912/results/noisy-markov-memory-check.json)
records the seed, Python/NumPy versions, measured errors, bounds, and
thresholds. No dependencies or production solver files changed.

For `Pbar/rmin=1`, the following use the revised finite-series bound (2).
`2^L` is the maximum state multiplier per calendar
stage, before counts or multiple chains.

| Correlation bound | Target `delta` | First `L` | Actual bound | `2^L` |
| --- | ---: | ---: | ---: | ---: |
| 0.4 | 0.10 | 4 | 0.05631 | 16 |
| 0.4 | 0.05 | 5 | 0.02266 | 32 |
| 0.4 | 0.01 | 6 | 0.00909 | 64 |
| 0.6 | 0.10 | 9 | 0.07513 | 512 |
| 0.6 | 0.05 | 10 | 0.04519 | 1,024 |
| 0.6 | 0.01 | 13 | 0.00979 | 8,192 |
| 0.9 | 0.10 | 72 | 0.09131 | about `4.72e21` |

At `rho=0.4,L=6`, the worst measured spectral error among the stationary
nine-point subsets was 0.000836, compared with bound 0.00909. The finite sample
is not a uniform certificate for larger `n`. Strong correlation is a decisive
practical limitation of this conservative bound, rather than a regime in
which scalability has been shown. Scalar independent proof review has passed.
The subsequent [scalar implementation and bounded comparison](research-20260912-noisy-markov-design-implementation.md),
[exact certificates](research-20260912-noisy-markov-certificates.md), and
[fixed physical grid test](research-20260912-fixed-physical-grid-benchmark.md)
are complete and separately reviewed. They establish the stated case-specific
results and scaling limits, with no general runtime-superiority or publication
priority claim.

## 7. Bounded literature search record

Queries on 2026-09-12 included `Vecchia approximation experimental design`,
`Vecchia approximation operator norm error exponential convergence covariance
inverse Cholesky`, `"finite memory" "experimental design" "correlated"`,
`"sensor selection" "Vecchia"`, `"finite memory" "sensor" "logdet"`,
`"sensor scheduling" "finite memory" "approximation"`, and
`"Optimal periodic scheduling of sensor networks"`. Further queries were
`"Vecchia" "spectral" "error" Markov`, `"Vecchia" "uniform" "operator norm"`,
and `"finite memory" "Fisher information" "Kalman"`.
The FSAI branch also used `"Factorized sparse approximate inverse"
"exponential" decay`. [Chow and Saad, 2013 author manuscript](https://www-users.cse.umn.edu/~saad/PDF/ys-2013-3.pdf)
applies FSAI to Gaussian covariance matrices; its abstract and §§2.2–3 were
inspected. [Localized inverse factorization](https://academic.oup.com/imajna/article/41/1/729/5824482)
has a primary search-rendered theorem on dimension-uniform sparsity under
entry decay and bounded neighborhood growth. Its full text remains unread.
Both were routed for ingestion and future priority audit.
Primary source checks focused on the sections identified above. The search
found strong established approximation machinery and the neighborhood-selection
work, but no matching uniform-calendar-window MINLP certificate in the
material inspected. This is a bounded negative search, not a priority claim.
