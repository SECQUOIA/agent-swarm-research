# Full-block noisy Markov design with input dimension: approximation scheme

Date: 2026-09-12. Status: proposed algorithmic corollary of the separately
reviewed [dimension-free block precision bound](research-20260912-noisy-markov-memory.md).
The proof below uses that bound and passed a
[fresh independent review](research-20260912-full-block-fptas-independent-review.md).
The bounded literature audit below has not located an older result covering
both input dimensions under these promises. This is not a complete priority
proof, and no first-FPTAS claim is made.

The useful distinction from the earlier
[scalar approximation scheme](research-20260912-scalar-noisy-design-fptas.md)
is that the number of jointly acquired channels is part of the input. The
schedule records one decision per time, and its combinatorial state count does
not grow exponentially with the channel count. The generic Gaussian graphical
model algorithm discussed in the [2012 prior-work reduction](research-20260912-scalar-gmrf-prior-reduction.md)
has a treewidth-dependent exponent and does not directly establish this scope.

## 1. Rational input and explicit promises

Fix rational constants `0<rho0<1` and `B0>0`. There are `n` candidate times and
a common block dimension `d`, both part of the input. The zero-mean error model
is

```text
Y_t = m_t(theta)+X_t+v_t,
X_t = A_t X_(t-1)+w_t,                 t=2,...,n.
```

The initial state, process errors, and observation errors are mutually
independent Gaussian vectors. Their covariances are rational matrices
`P_1>=0`, `Q_t>=0`, and `V_t>0`. Transitions `A_t` are rational. Singular
initial and process covariance matrices are allowed. Recursively define

```text
P_t = A_t P_(t-1) A_t^T+Q_t.
```

The input is promised to satisfy the rational Loewner inequalities

```text
A_t V_(t-1) A_t^T <= rho0^2 V_t,        t=2,...,n,
P_t <= B0 V_t,                         t=1,...,n.       (1)
```

Positive semidefiniteness and these promises can be checked by exact rational
linear algebra in polynomial time. They impose contraction in the
observation-noise metric; Euclidean stability of `A_t` alone is insufficient.
They do not require bounded Euclidean condition numbers for `V_t`.

Selecting time `t` acquires all `d` coordinates of `Y_t`. The only selection
constraint is `|S|=k`, with input integer `0<=k<=n`. Fixed mandatory and
forbidden times are also allowed if the resulting family is nonempty. General
side constraints and selection of individual coordinates within a block are
outside this statement.

The mean sensitivities `F_t` are rational `d`-by-`p` matrices at the specified
nominal parameter. The parameter dimension `p` may also be part of the input.
Providing these sensitivities is part of the input specification; the result
does not assert polynomial-time evaluation of arbitrary nonlinear process
models or ODE sensitivities. Error covariances are known and independent of
the mean parameter. Let `R_SS` be the covariance of the selected observation
errors. The objective is

```text
I(S) = tr[W (J0+F_S^T R_SS^(-1) F_S)],
W>=0, J0>=0,                            W,J0 rational p-by-p.     (2)
```

Both `W` and `J0` are fixed across schedules. The data term is zero for an
empty schedule. For one parameter take `p=1,W=1`; then (2) is scalar Fisher
information plus a fixed nonnegative prior. In general it is a weighted trace
of information, not a trace of inverse information. Multi-parameter
D-optimality, A-optimality, and a parameter-dependent covariance contribution
are not covered by the approximation-scheme statement.

## 2. Algorithm and guarantee

**Corollary.** For the fixed constants in (1) and rational `0<epsilon<1`,
there is an algorithm polynomial in the rational input encoding length and
`1/epsilon` that returns a feasible schedule `S_hat` satisfying

```text
I(S_hat) >= (1-epsilon) max_(|S|=k) I(S).                (3)
```

The polynomial includes `n,d,p` as input dimensions. Its exponent in
`1/epsilon` depends on `rho0`; it is independent of `d` and `p`.

Return immediately for `k=0`. Put `eta=epsilon/2` and
`C0=2 B0/(1-rho0)^2`. Choose the smallest integer `L>=0` with
`C0 rho0^(L+1)<=eta`, unless `L=n-1` is reached first. Use rational powers
and comparisons; computing logarithms is unnecessary. For `n=1`, take
`L=0`. If `n=0`, return the empty schedule. At the cap `L=n-1`, local
conditioning is exact for every schedule.

For each time `t` and every subset `H` of its preceding `L` calendar times,
compute the following matrices directly in the original coordinates:

```text
B_(t,H) = R_(t,H) R_HH^(-1),
D_(t,H) = R_tt-R_(t,H) R_HH^(-1) R_(H,t),
G_(t,H) = F_t-B_(t,H) F_H,
w_(t,H) = tr[W G_(t,H)^T D_(t,H)^(-1) G_(t,H)].       (4)
```

For empty `H`, use `D=R_tt` and `G=F_t`. Observation noise is positive
definite, so every inverse in (4) exists. The weights are nonnegative
rationals.

Use an exact dynamic program on states consisting of calendar time, the
selection bitmask of the preceding `L` times, and the count of selections.
Skipping contributes zero; selecting contributes (4) for the history encoded
by the mask. Count and mandatory/forbidden restrictions remove inadmissible
arcs. Add the constant `tr(W J0)` once. This maximizes the additive surrogate
over the original discrete feasible family; there is no fractional hull gap.

For the proof, introduce whitening only as a mathematical change of
coordinates:

```text
X'_t=V_t^(-1/2) X_t,
T_t=V_t^(-1/2) A_t V_(t-1)^(1/2).
```

Inequalities (1) imply `||T_t||_2<=rho0` and
`Cov(X'_t)<=B0 I`. The reviewed block theorem therefore bounds the relative
precision error, simultaneously for every subset, by

```text
delta_L <= 2 B0 rho0^(L+1) (1-rho0^(L+1))/(1-rho0)^2
        <= C0 rho0^(L+1).                              (5)
```

The theorem uses block operator norms, so (5) has no factor `d`. True and
surrogate information are invariant under this invertible change of
coordinates when the sensitivities are transformed with the observations.
Thus the rational calculation (4) produces the same surrogate information.
Congruence, the positive semidefinite trace weight, and the nonnegative fixed
prior give

```text
(1-delta_L) I(S) <= I_L(S) <= (1+delta_L) I(S).          (6)
```

If `S_star` optimizes (2) and `S_hat` optimizes the surrogate, then

```text
I(S_hat) >= I_L(S_hat)/(1+delta_L)
         >= I_L(S_star)/(1+delta_L)
         >= [(1-delta_L)/(1+delta_L)] I(S_star)
         >= (1-epsilon) I(S_star).                     (7)
```

At the full-history cap take `delta_L=0` instead of (5). The inequality holds
even when the optimum is zero. If the optimum is positive, it also gives
`log I(S_star)-log I(S_hat)<=log((1+delta_L)/(1-delta_L))`.

## 3. Arithmetic and bit complexity

Let `a0=log(2)/log(1/rho0)`. Minimality of the accuracy-based history length
gives

```text
2^L <= max{1,(C0/eta)^a0}.                              (8)
```

Capping `L` cannot increase this bound. The graph has
`O(n(k+1)2^L)` states and arcs, and longest-path optimization requires that
many rational additions and comparisons. Its state count depends on elapsed
calendar time, not the number of scalar coordinates in the observation.

Every matrix inverted locally has at most `d(L+1)` rows. Computing (4)
therefore costs a polynomial in `d(L+1)` and `p` for each of `O(n2^L)`
histories. One deliberately simple implementation first forms the complete
`nd`-by-`nd` observation covariance by state covariance recursions. This also
has polynomial arithmetic and storage cost. Exploiting structure can reduce
that cost but is unnecessary to prove the result.

For bit complexity, the input is an explicitly encoded rational matrix
instance, with binary numerators and denominators. State covariance entries
are sums of products involving at most a polynomial number of input factors
along a time path. A common denominator obtained from the product of input
denominators to polynomial powers has polynomial encoding length. Products
of bounded-length rational entries and sums over state-coordinate paths have
polynomial-size numerators: the number of monomials may be large, but its
logarithm is polynomial in `n,d`. Consequently, the covariance matrices have
polynomial encoding length. Exact linear solves on their principal matrices
have polynomial bit complexity and polynomial-size results by determinant
bounds or fraction-free elimination. This applies even when ordinary
floating-point conditioning is poor.

Each dynamic-programming value sums at most `n` such rational arc weights
and one rational prior. Adding their denominator bit lengths gives a
polynomial bound. Comparing exact rational path values is therefore
polynomial, irrespective of how many paths share a state. Equations (8) and
`L=O(1+log(1/epsilon))` complete the bit-complexity argument. There is no
spectral decomposition, approximate eigenvalue primitive, or irrational
whitening operation in the algorithm.

The constants must remain fixed as the input grows. This is not a uniform
FPTAS if `rho0` can approach one or `B0` can grow without bound as part of the
input. For example, `a0` is about `0.756,1.357,3.106,6.579` at correlations
`0.4,0.6,0.8,0.9`, respectively, before matrix-calculation costs. Fine
physical-time grids often make the per-step correlation approach one.
Polynomial dependence on dimension also does not make dense matrix inversion
cheap for thousands of spectral channels or image pixels.

## 4. Prior-work audit and application assessment

Primary sources were checked on 2026-09-12. The existing scalar prior audit
is inherited only where its assumptions apply.

The 2012 Mahalanabis–Stefankovic Gaussian message algorithm has runtime
depending exponentially on a squared graph-treewidth parameter. The scalar
augmentation used in the linked prior reduction has width at most three.
With dense `d`-dimensional latent states and dense within-time matrices, the
natural Gaussian bags contain whole state blocks, so that argument has width
growing with `d`. Replacing scalar graph vertices by vector-valued vertices
does not remove the dimension of the separator precision messages or their
rounding nets. This explains why that specific prior reduction does not prove
the full-block result; it is not a lower bound on all older algorithms.

The same distinction matters even for `d=1` when the rank of
`F W F^T` is input-sized. Augmenting a Gaussian model by a `p`-dimensional
target generally enlarges separator messages. Making independent scalar
copies instead produces selection decisions that must be tied across copies;
the reviewed scalar-target reduction does not remove that coupling. The
weighted-trace objective is also the total explained squared norm in a
multiresponse regression problem with shared selected predictor groups.
Optimizing each response separately and summing its optimum does not solve
the common-subset problem.

The [March 2026 Vecchia and growing-rank follow-up audit](research-20260912-kaminetz-webber2026-priority-audit.md)
checks the distinct Kaminetz–Webber paper and additional multiresponse
comparators. It recommends the scalar-observation, input-sized-rank case as
the simplest statement, with full blocks as an extension. Priority remains
qualified.

| Primary source inspected | Result and closest scope | What the inspection establishes here |
|---|---|---|
| [Mahalanabis–Stefankovic2012, Theorem43](https://arxiv.org/abs/1209.5991) and its thesis counterpart | Gaussian posterior-variance approximation using precision messages and treewidth-dependent rounding nets. | The separately reviewed scalar-target reduction is strong prior. It does not give a dimension-independent exponent for general dense blocks or a growing-rank target. |
| [Craparo et al.2007, §IV.A, pp5–6](https://faculty.nps.edu/emcrapar/GNC2007.pdf) | Independent `2`-by-`2` information blocks give an additive communication objective and a multiple-choice knapsack FPTAS. §IV.B treats the dense case heuristically. | This is an earlier information-block FPTAS, but its independence assumption removes the temporal subset-dependent inverse. Do not claim that approximation schemes for block information selection are new. |
| [Vitus et al.2010, Definition4 and Theorem3](https://engineering.purdue.edu/~jianghai/Publication/ACC2010_SensorSchedule.pdf), expanded in [Automatica2012](https://doi.org/10.1016/j.automatica.2012.06.092) | Covariance-matrix dominance and epsilon pruning give an average-cost error bound for vector state scheduling. | The primary conference theorem permits arbitrary accuracy but does not supply the polynomial-in-accuracy and dimension state-count guarantee proved above. The 2012 publisher abstract was also checked; its PDF was indexed but a local retrieval failed. |
| [Maity–Hartman–Baras2022, Lemma5, Eq12, p5](https://johnbaras.com/wp-content/uploads/2022/02/20-13-Pub-Version_1-s2.0-S0005109821006075-main.pdf) | Convex covariance design followed by covariance tracking; an additive bound depends on the covariance mismatch with optimal and relaxed trajectories. | Its epsilon is an instance-dependent mismatch bound, not an input accuracy parameter with an FPTAS runtime. The expression includes a state-dimension factor. |
| [Tropp–Gilbert–Strauss2006, PartI, Theorems5.1–5.2](https://tropp.caltech.edu/papers/TGS05-Algorithms-Simultaneous-I-preprint.pdf) | Simultaneous orthogonal matching pursuit for common-support multiple signals, with coherence-dependent error/support guarantees. | Multiple responses and polynomial algorithms are established. The inspected guarantees are not arbitrary `1-epsilon` optimal explained-information guarantees over the promised covariance class. |
| [Tropp2006, PartII, Theorems5.1 and6.1](https://tropp.caltech.edu/papers/Tro05-Algorithms-Simultaneous-II-preprint.pdf) | Convex row-sparsity relaxations with exact-recovery-coefficient and residual-correlation assumptions. | These theorems require conditions on the chosen support and approximation residual. They do not directly imply the current scheme for unrestricted rational sensitivities and cardinality. |
| [Liberty–Sviridenko2017, §5, Lemmas14–15](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2017.19) | Sparse multiple linear regression and its weak-supermodularity parameter give arbitrary-error greedy guarantees with more selected variables. | The guarantee enlarges the cardinality by a factor involving conditioning and logarithmic accuracy. It is a useful multiresponse competitor, but does not preserve the exact `k` budget required in (3). |
| [Liu et al.2016, §IV.C](https://arxiv.org/abs/1508.03690) | Correlated sensor selection explicitly includes the trace of Fisher information, with weak-correlation quadratic approximations and local/semidefinite methods. | The scalarized criterion is established and should be credited. The paper does not give the finite-history relative guarantee or this approximation scheme. Its reported variance comparisons also caution against treating a trace-of-information result as a guarantee for parameter covariance. |

Other identified sources were routed to the sole literature agent. The
primary abstract of Simila–Tikka2006 describes a common-input multiresponse
forward-selection algorithm. Tzoumas–Jadbabaie–Pappas2016 gives a scalable
constant-factor batch-state result; Vafaee–Siami2022 approximates a fully
sensed reference through randomized scheduling. Neither inspected abstract
claims the current fixed-cardinality FPTAS. These are leads, not full-text
exclusions. The earlier audit also left Radovilsky–Shattah–Shimony2006 noisy
emission selection unread because no full text was retrieved; its scope
remains an unresolved prior-work question.

Representative query record: `sensor scheduling fully polynomial Gaussian`;
`sensor selection FPTAS vector Gaussian`; `sensor scheduling polynomial time
epsilon Kalman`; `Gaussian measurement scheduling approximation finite memory
algorithm exponential stability`; `multiresponse subset selection
approximation`; `multivariate regression subset selection FPTAS`;
`simultaneous sparse approximation approximation polynomial`; and
`multiresponse subset selection exponential covariance approximation scheme`.
Searches also followed references and primary author pages rather than relying
on the absence of exact terminology. This bounded search has not established
an exhaustive negative literature claim.

## 5. Process relevance and practical limits

There is also direct relevance without large observation blocks.
[Wang et al., Measure This, Not That](https://arxiv.org/abs/2406.09557),
which includes Bernal Neira, explicitly optimizes the trace of the Fisher
information matrix in its reaction-kinetics and carbon-capture studies. The
input-sized parameter dimension in (2) therefore supports an established
process-design criterion. This does not cover that paper's entire feasible
family of installation and measurement budgets. Its comparisons also show
that a large trace need not resolve practical nonidentifiability, which is
why the present trace guarantee must not be reported as a D-optimality or
parameter-covariance guarantee.

One promising process use is selecting acquisition times for a shared
FT-NIR analyzer during a kinetic run, where each acquisition produces a full
spectrum and one important rate constant is the inferential target.
The 2003 paper
[Optimal on-line sampling of parallel reactions: general concept and a specific spectroscopic example](https://doi.org/10.1016/S0920-5861(03)00134-2)
directly studies sampling times, counts, and windows for a pseudo-first-order
rate estimated using online FT-NIR. Its publisher abstract and introduction
support the application motivation; full text has not yet been read. They do
not establish the vector autoregressive noise model or promises (1).

The open 2026 study
[Raman-guided sample subset selection for cost-efficient offline calibration in bioprocesses](https://doi.org/10.1007/s00449-026-03402-x)
provides an adjacent practical example and spectral subset-selection
comparators. Its selected expense is offline reference assays; inline spectra
are already available. It therefore does not validate selecting whether to
acquire complete spectra under (2). It also identifies drift and process
effects that would require residual-model validation. We must not assume
these effects follow a stable Gaussian vector recursion.

No process validation or implementation advantage has yet been demonstrated
for the full-block approximation scheme. An important empirical question is
whether calibrated residual models meet (1) with correlations small enough
that (5) gives practical history lengths. The theoretical statement could be
useful despite an input-dependent Gaussian treewidth, but that fact alone is
not evidence of a substantial applied advance.

## 6. Why selecting complete blocks is essential

The following elementary reduction was proposed by the root researcher and
independently checked. It is a scope boundary, not a claimed new hardness
result. If the decision may instead select individual coordinates within a
block, there is no deterministic FPTAS for scalar information unless `P=NP`, even when the
observation covariance has condition number at most `5/3`.

Take a simple cubic graph on `m` vertices with adjacency matrix `A`, and an
Independent Set target `k`. This problem is NP-hard even on 2-connected
cubic planar graphs; see
[Mohar2001, Theorem4.1(a), pp10–11 of the author manuscript](https://www.sfu.ca/~mohar/Reprints/2001/BM01_JCT82_Mohar_ApexGraphs.pdf).
Use one calendar time, block dimension `d=m`, and one-parameter sensitivity
vector equal to all ones. Choose independent isotropic observation noise
`V=(2/3)I` and latent covariance `P=(1/3)I+A/12`. The latent spectrum lies
in `[1/12,7/12]`, so `P` is positive definite and `P<=(7/8)V`. Thus the
promises (1) hold with the fixed constant `B0=1`; the transition promise is
vacuous. The total observation covariance is still `R=P+V=I+A/12`. Now
count individual coordinates in the cardinality budget, so a feasible choice
is any `k`-subset of vertices. This strengthening was independently reviewed;
hardness does not require correlated observation noise or a singular latent
covariance.

The spectrum of `A` is contained in `[-3,3]`, hence
`(3/4)I<=R<=(5/4)I`. For any selected subset, put
`x=(I+A_SS/12)^(-1)1`. Since `||A_SS/12||_infinity<=1/4`, the Neumann bound
gives `||x||_infinity<=4/3`. The equation for each coordinate then implies
`x_i>=1-(3/12)(4/3)=2/3`. Summing those equations gives

```text
I(S) = 1^T R_SS^(-1)1
     = k-(1/12) sum_(i in S) degree_S(i) x_i.
```

If `S` is independent, `I(S)=k`. If it contains an edge, its degree sum is
at least two, so `I(S)<=k-1/9`. An FPTAS run at the rational accuracy
`epsilon=1/[18(m+1)]` must return an independent `k`-set whenever one
exists: even with the prior `I0=1`, its allowed loss from the yes-instance
optimum is at most `epsilon(k+1)<=1/18`, smaller than `1/9`. Checking the
returned set for edges would decide Independent Set in polynomial time.

This result does not contradict the full-block scheme: that scheme assigns
one binary decision to the entire vector, whereas this reduction requires
`m` independent binary decisions inside its only block. It also does not
rule out constant-factor approximations or a PTAS on this restricted
partial-coordinate class. General correlated-regression hardness is old;
the explicit conditioning and gap calculation here serve to explain the
theorem's selection restriction.
