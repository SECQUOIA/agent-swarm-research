# D-optimal design on a finite information graph at fixed parameter dimension

Date: 2026-09-12. Status: theorem and corollary passed a
[fresh independent review](research-20260912-doptimal-fptas-independent-review.md).
The explicit-DAG theorem is now also derived from the executable Lean
spectral-cover construction in [topic 21](../formal/topics/21-dag-spectral/README.md),
with proved correctness and bit-work bounds. The bounded literature audit has
not established priority. Normalization and dynamic programming are
established ideas; the precise proposed combination needs review.

The proposed result is a deterministic FPTAS for maximizing the determinant
of a sum of rational positive semidefinite matrices along a path in an
explicit directed acyclic graph, with fixed matrix dimension. It permits a
singular prior and arbitrarily poor numerical conditioning. Applied to the
finite-history information graph, it would extend the weighted-trace scheme
to D-optimality at fixed parameter dimension. Its large polynomial exponent
makes this a complexity result, not a practical solver claim.

## 1. Explicit graph problem

Fix a positive integer `p`. The input is a finite directed acyclic graph
`G=(V,E)` with source `s`, sink `t`, rational symmetric matrices `Q_e>=0`
of order `p` on its edges, and a rational symmetric prior `Q0>=0`. Set

```text
J(P)=Q0+sum_(e in P) Q_e
```

for every `s-t` path `P`. First find any feasible path or report that none
exists. Let `N=max(1,|V|-1)` bound path length. If `s=t`, the empty path is
handled immediately. Matrices and the graph are explicitly encoded.

**Theorem.** Given rational `0<eta<1`, the algorithm below returns
a feasible path satisfying

```text
det J(P_hat) >= (1-eta) max_P det J(P).                 (1)
```

Its bit complexity is polynomial in input length and `1/eta` for fixed
`p`. Its polynomial exponent depends on `p`; this is not fixed-parameter
tractability with an exponent independent of dimension.

The graph may encode cardinality, mandatory decisions, spacing, or other
finite-state restrictions. Complexity is measured in its explicit size.
The theorem does not promise a polynomial graph construction for arbitrary
side constraints or binary-encoded resource budgets.

## 2. All-rational algorithm

Exact rational pivoted LDL factorization writes each edge matrix and prior
as a sum of at most `p` nonzero rank-one terms:

```text
Q_e=sum_(j owned by e) w_j v_j v_j^T,
Q0 =sum_(j owned by prior) w_j v_j v_j^T,
w_j>0 rational, v_j rational.                         (2)
```

Zero terms are discarded. A positive diagonal pivot yields a rational PSD
Schur complement, and a PSD residual with all diagonal entries zero is
zero. Thus such a decomposition exists even for singular matrices. There
are at most `M=p(|E|+1)` factor labels. Each retains its edge or prior owner.

Enumerate all sets of `p` factor labels with nonsingular rational matrix
`V_b=[v_b1,...,v_bp]`, ordering columns by a fixed label order. For each:

1. Choose powers of two `tau_i=2^r_i` satisfying
   `1<=tau_i^2 w_bi<4`, using exact rational comparisons. Define rational
   `T=diag(tau_i) V_b^(-1)`, `A_e=T Q_e T^T`, and `A0=T Q0 T^T`.
2. Discard this basis if any diagonal entry of `A0` exceeds `4p`.
   Remove each edge with any diagonal entry of `A_e` exceeding `4p`.
   PSD then implies that every entry of each retained matrix has absolute
   value at most `4p`.
3. Require the path to traverse all distinct edge owners among the selected
   basis factors. There are at most `p`; track their presence with a bitmask
   of at most `2^p` values. Prior factors require no bit.
4. Set `h=eta/(p^2 N)`. Give every retained edge the integer vector of
   upper-triangular labels `Z_e,ij=floor(A_e,ij/h)`, `1<=i<=j<=p`.
   Floor applies to negative entries too. Do not round the prior.
5. In topological order run an exact dynamic program whose states are
   `(vertex,owner-mask,sum of integer edge labels)`. Retain one actual path
   realizing each state. Extend labels by exact addition. At `t`, accept
   only complete owner masks.
6. Evaluate each terminal representative's original rational determinant
   and keep a largest value across all bases.

If no basis produces a terminal representative, return the feasible path
found initially. Section 3 proves that its optimal determinant is then zero.
This covers an empty factor list. A DAG path cannot reuse an edge. Because
future extensions depend only on the vertex and recorded state, merging
paths with identical integer labels and owner masks preserves every
reachable state.

## 3. Guarantee

Suppose an optimal path `P_star` has positive determinant. The factors in
its edge matrices and its prior span `R^p`. Introduce real vectors
`u_j=sqrt(w_j) v_j` only in the proof. Choose a maximum-absolute-determinant
basis from that factor collection:

```text
B=[u_b1,...,u_bp]=V_b diag(sqrt(w_bi)).
```

Every factor `u` in this collection has coordinates `x=B^(-1)u` with
`|x_i|<=1`. Replacing column `i` by `u` changes the determinant to
`x_i det B`, so maximality proves the bound. This elementary maximum-volume
basis argument is established linear algebra, not a claimed new lemma.

The algorithm enumerates these labels. Its transformation gives

```text
T B=diag(tau_i sqrt(w_bi)),
I <= T B B^T T^T < 4 I.                               (3)
```

Thus every transformed factor `T u=(T B)x` has coordinates of absolute
value less than `2`. Each edge matrix and the prior has at most `p` factors,
so all their transformed diagonal entries are at most `4p`. The optimum
survives this basis's filter and meets its owner requirements. Moreover,

```text
A_star=T J(P_star) T^T >= T B B^T T^T >= I.            (4)
```

This also holds if several basis factors share an owner: that owner's
matrix contains their sum. Every accepted terminal representative for this
basis contains the basis factors as well.

Let `P_hat` be the representative at the optimum's terminal integer-label
state. For every path of at most `N` edges and every entry, floor gives

```text
0 <= sum_(e in P) A_e,ij-h sum_(e in P) Z_e,ij < N h.  (5)
```

The empty path has residual zero. Negative entries satisfy the same bound.
The two paths have identical label sums and identical unrounded prior.
Their residuals both lie in `[0,Nh)`, even if their lengths differ. Hence,
with `A_hat=T J(P_hat) T^T`,

```text
max_(i,j)|A_hat,ij-A_star,ij| < N h,
||A_hat-A_star||_2 <= p N h=eta/p,
A_hat >= A_star-(eta/p)I >= (1-eta/p)A_star.           (6)
```

The last step uses (4). Undoing the congruence and using monotonicity of
determinant on positive definite matrices gives

```text
det J(P_hat) >= (1-eta/p)^p det J(P_star)
             >= (1-eta) det J(P_star).                (7)
```

The final step is Bernoulli's inequality. Choosing the largest determinant
across all representatives preserves this guarantee.

If every feasible information matrix is singular, all determinants are zero
and any path satisfies (1). Conversely, any path with positive determinant
supplies a basis and a terminal representative by the same argument. This
proves the fallback rule without any eigenvalue lower bound on the prior
or any positive lower bound on the optimum.

## 4. State count and exact arithmetic

Put `d_p=p(p+1)/2`. Each integer edge-label entry lies between
`-4p/h-1` and `4p/h`. Across paths of length at most `N`, there are at most

```text
C=ceil(8p N/h+N)+2=ceil(8p^3 N^2/eta+N)+2              (8)
```

possible values per coordinate. This loose bound covers signed entries
and differing lengths. Per basis there are at most `|V| 2^p C^d_p` states
and `|E| 2^p C^d_p` transitions. There are at most `M^p` bases. Thus the
number of operations is polynomial in graph size and `1/eta` for fixed
`p`. One predecessor and one exact matrix sum per state suffice.

Rational LDL, inversion, congruence, and determinant computations have
polynomial bit complexity, with polynomial-size outputs by determinant
bounds. The dyadic exponents are bounded by a polynomial in the encoding
length of `w_bi`. Path sums contain at most `N` rational matrices; summing
their denominator bit lengths gives a polynomial bound. Floors use exact
integer division. Integer labels have polynomial encoding length in the
input length and `log(1/eta)`. No square-root, spectral, floating-point,
or algebraic-number oracle is required by the algorithm.

The crude state bound contains `(N^2/eta)^(p(p+1)/2)` before basis
enumeration. It does not suggest competitive runtimes on the repository's
`p=3,n=96` numerical benchmarks.

## 5. Noisy Markov design corollary

Use the rational block model and fixed contraction and signal-to-noise
promises of the [full-block weighted-trace scheme](research-20260912-full-block-design-fptas.md).
Here `p` is fixed, while candidate times `n` and jointly acquired observation
coordinates `d` are input dimensions. The prior `J0>=0` may be singular.
Sensitivities are rational input; evaluating arbitrary process or ODE
sensitivities is outside the complexity claim. Acquire complete observation
blocks, with cardinality `k` and mandatory or forbidden times represented
in the graph.

Selecting time `t` with retained history `H` contributes rational PSD

```text
Q_(t,H)=G_(t,H)^T D_(t,H)^(-1) G_(t,H),
G_(t,H)=F_t-R_(t,H) R_HH^(-1) F_H,
D_(t,H)=R_tt-R_(t,H) R_HH^(-1) R_(H,t).                (9)
```

Skipping contributes zero. Positive definite observation noise makes all
local conditional covariances invertible. The [reviewed memory bound](research-20260912-noisy-markov-memory.md)
implies, simultaneously for every schedule,

```text
(1-delta_L) J(S) <= J_L(S) <= (1+delta_L) J(S),
delta_L <= C0 rho0^(L+1), C0=2 B0/(1-rho0)^2.         (10)
```

Adding a fixed PSD prior preserves these inequalities. At full history
`L=n-1`, use `delta_L=0` because the local information is exact.

Given rational `0<epsilon<1`, put `eta=epsilon/2`. Choose the smallest `L`
with `C0 rho0^(L+1)<=epsilon/(4p)` by rational comparisons, unless full
history is reached first. Handle `n=0` or `k=0` directly. Apply the graph
algorithm to `J_L`. For an exact optimum `S_star`,

```text
det J(S_hat)
 >= (1-eta) [(1-delta_L)/(1+delta_L)]^p det J(S_star)
 >= (1-epsilon) det J(S_star).                        (11)
```

Since `(1-delta)/(1+delta)>=1-2delta`, Bernoulli's inequality bounds this factor's
power below by `1-2p delta>=1-epsilon/2`. The product of the two losses is
at least `1-epsilon`. Zero optimal determinant causes no problem. For a
positive optimum, D-efficiency is at least `(1-epsilon)^(1/p)`. This is not
a multiplicative approximation to the logarithm of the determinant.

The graph has `O(n(k+1)2^L)` states and edges. For fixed `rho0<1,B0,p`,
`2^L` is polynomial in `1/epsilon`. The local matrix calculations have
polynomial bit complexity in `d,p,n,L` as established in the weighted-trace
note. Their composition with Sections 2–4 therefore gives an FPTAS.

This is not a uniform FPTAS if `rho0` approaches one, `B0` grows, or `p`
is part of the input. Physical-time grid refinement can destroy a fixed
per-step contraction promise. Arbitrary individual-coordinate selection
inside a block is outside this corollary.

## 6. Prior-work audit

**An elementary exact-hardness check.** The graph problem already embeds
PARTITION at `p=2` with zero prior and diagonal matrices. For positive
integer inputs `a_1,...,a_m`, build `m` two-choice stages, assigning either
`diag(a_i,0)` or `diag(0,a_i)` at stage `i`. If parallel edges are unwanted,
replace each choice by a two-edge diamond with one zero edge. Every path
has information `diag(s,A-s)`, where `A=sum_i a_i` and `s` is a subset sum.
Its determinant is `s(A-s)=A^2/4-(s-A/2)^2`. The optimum equals `A^2/4`
exactly when a partition exists. Thus even this fixed-dimensional case is
weakly NP-hard. This standard reduction illustrates why an approximation
scheme is nontrivial; no new hardness result is claimed.

**Fixed-dimensional design.** Brown, Laddha, and Singh's Theorem 2 gives a
randomized PTAS for fixed-dimensional monotone concave homogeneous matrix
objectives under partition constraints, with extension to matroids. Taking
the determinant root covers D-efficiency. Their runtime exponent depends
on `1/epsilon^2`, so it is not an FPTAS. Section 3 already guesses a
normalization, filters large vectors, and forces a guessed subset into the
solution. These strategies must not be claimed as new. The proposed
comparison point is a basis of only `p` factors combined with signed
matrix-label dynamic programming on a DAG. [Brown et al. 2024, DOI
10.1016/j.orl.2024.107186](https://par.nsf.gov/servlets/purl/10548928).

**Local search.** Madan, Singh, Tantipongpipat, and Xie analyze D-optimal
local search with a determinant-root approximation scale `(k-p+1)/k`,
subject to their algorithmic qualifications. This is near optimal when
`k` is large relative to dimension and accuracy. Combining it with small-
cardinality enumeration gives a PTAS whose exponent can depend on accuracy;
it does not directly give an FPTAS or the history-dependent path result.
[Madan et al. 2019](https://proceedings.mlr.press/v99/madan19a.html).

**Information along paths.** Ott, Kochenderfer, and Boyd formulate a
mixed-integer convex problem for independent-measurement A/D-information
along constrained paths. Their sequential dynamic program uses surrogate
node rewards. Section 4.1 measures an a posteriori gap to a convex
relaxation; it does not establish an arbitrary-accuracy polynomial scheme.
The model permits general graphs and limits repeated visits, so a time
expansion alone would not give the explicit DAG required here without
handling those additional feasibility restrictions. [Ott et al. 2024](https://arxiv.org/html/2402.08841v2).

**Recent cardinality approximation.** Lau, Wang, and Zhou's Theorem 1.2
gives a deterministic with-replacement D-design algorithm with
determinant-root guarantee `[k!/((k-p)! k^p)]^(1/p)` for `k>=p`. It recovers
near-optimality for large `k` relative to `p/epsilon`; the theorem is not an
arbitrary-accuracy FPTAS for every budget. Their method uses interlacing
polynomials and returns an actual multiset. It is a strong independent-design
competitor, but does not model history-dependent information along a path.
[Lau et al. 2025, DOI
10.1137/1.9781611978315.33](https://cs.uwaterloo.ca/~lapchi/papers/interlacing-design.pdf).

**Multiobjective paths.** Rounded labels and approximate Pareto sets are
established techniques. Tsaggouris and Zaroliagis treat nonlinear path
utilities under nonnegative additive costs, coordinatewise monotonicity,
and growth conditions. Determinant is not coordinatewise monotone in
arbitrary signed matrix entries. The basis step above supplies bounded
signed coordinates and a relative Loewner perturbation bound. This is the
extra argument needed for the reduction, not a new general dynamic
programming method. [Tsaggouris and Zaroliagis 2009, DOI
10.1007/s00224-007-9096-4](https://www.ceid.upatras.gr/webpages/faculty/zaro/pub/jou/J28-TOCS-mosp.pdf);
[Papadimitriou and Yannakakis 2000, DOI
10.1109/SFCS.2000.892068](https://www.cs.purdue.edu/homes/yexiang/courses/18fall-cs590/papers/papadimitriou2000.pdf).

**Low-rank optimization.** Mittal and Schulz use positive linear
coordinates, a monotone outer function, and a growth bound. Their
extreme-point guarantee applies to quasi-concave minimization or
quasi-convex maximization. Continuous-polytope approximation of concave
determinant-root maximization permits a fractional path mixture, so it does
not alone justify a discrete path approximation. Another specialized
reduction may still exist. [Mittal and Schulz 2013, DOI
10.1007/s10107-011-0511-x](https://doi.org/10.1007/s10107-011-0511-x).

The separate Operations Research paper by the same authors, Theorem 3.3,
uses a pseudopolynomial exact linear-objective oracle and fixed many
nonnegative profile coordinates. Its outer function is coordinatewise
nondecreasing with a fixed polynomial scaling bound. Section 7 treats a
positive ratio with mixed minimization/maximization directions. These
conditions do not directly cover determinant cancellation. For example,
`A_t=[[1,1-t],[1-t,1]]` and `B=[[1,1],[1,1]]`, `0<t<1`, are PSD with all
positive entries. Their entries differ by multiplicative factors at most
`1/(1-t)`, tending to one, but `det A_t=2t-t^2` and `det B=0`. Thus a
relative coordinate approximation alone does not give a relative determinant
approximation. The normalization and spectral argument in Section 3 supply
that missing control. [Mittal and Schulz 2013, DOI
10.1287/opre.1120.1093](https://web.mit.edu/schulz/www/epapers/ms-or-2013.pdf).

**Pseudopolynomial nonlinear discrete optimization.** Berstein and
coauthors' Theorem 1.3 optimizes an arbitrary nonlinear function of a fixed
number of integer weight sums over a represented matroid, in time polynomial
in the representation size and the largest absolute weight. This is close
prior for the bounded-profile optimization step, although a DAG path family
is not generally a matroid basis family. Their motivating experimental-design
application is minimum-aberration model fitting. A combination of existing
profile algorithms and normalization may imply wider design approximation
results; that issue remains open in this audit. [Berstein et al. 2008, DOI
10.1137/070696465](https://optimization-online.org/wp-content/uploads/2007/07/1725.pdf).

**Hardness distinctions.** Ohsaka studies maximum principal
subdeterminants, including rank-parameterized hardness. That criterion
differs from a fixed-order determinant of a sum when selection cardinality
exceeds feature dimension. The parameterized lower bounds also target an
exponent independent of rank, whereas the proposed algorithm's exponent
depends on `p`. This is neither a contradiction nor a hardness proof for
our precise graph problem. [Ohsaka 2024, DOI
10.1007/s00453-023-01205-0](https://link.springer.com/article/10.1007/s00453-023-01205-0).

Ohsaka's Section 5.3, Observation 5.11, rounds individually bounded rational
vectors in dimension `d`, enumerates `k<=d` distinct rounded vectors, and
controls the additive error in a principal Gram determinant. This is
relevant determinant-rounding prior. It does not directly optimize sums of
an input number of factors along paths, or provide a relative determinant
guarantee without additional normalization. Its concluding question about
a relative rank-parameterized approximation asks for an exponent independent
of rank and is not settled by this note.

Bansal and Xu's August 2026 A/E-design hardness construction uses dimension
`d=m+n+1` growing with its three-dimensional-matching input. Their discussion
explicitly distinguishes the known fixed-dimensional design results. Thus
their Theorem 1.1 does not contradict a fixed-`p` scheme, and it concerns
A/E objectives rather than the determinant guarantee stated here.
[Bansal and Xu 2026](https://arxiv.org/html/2608.05468v1).

The previous [scalar GMRF reduction](research-20260912-scalar-gmrf-prior-reduction.md)
already narrowed the scalar trace scheme's novelty. Whether an older
matrix-design or discrete nonlinear optimization theorem implies the graph
result is unresolved. Fresh proof review has passed, but a stronger priority
audit is needed before any first-FPTAS claim. The candidate contribution is
an explicit fixed-parameter D-optimal approximation guarantee for the
finite-history model, including exact rational arithmetic and singular
priors.


## 7. Lean verification and the spectral-cover implementation

[Topic 21](../formal/topics/21-dag-spectral/README.md) verifies the stronger
explicit-DAG spectral-cover construction in the
[spectral-set note](research-20260912-dag-psd-approximation-set.md).
Its determinant consequence gives the explicit-graph theorem here by
choosing the matrix tolerance `epsilon/p` and applying Bernoulli's inequality.
It preserves singular priors, zero determinant optima, empty feasible sets,
and the source-equals-sink case. Exact rational determinant comparison
selects a representative. This route does not require a separate
implementation of the predecessor's full-rank-only normalization argument.

The reference implementation uses leading-coordinate rational LDL with
zero-row skipping, enumerated rational range bases, exact dyadic scales,
and a list-based profile DP. The common-range spectral guarantee also
covers rank-deficient information. The complete costed realization takes a
graph with verified topological vertex indices and starts from the original
rational matrix encodings. Its bounds account for factor initialization,
all trials, exact arithmetic, dictionary scans, storage and path recovery.
These are schoolbook bit-work bounds, not practical timing predictions; consult the
[coverage map](../formal/topics/21-dag-spectral/COVERAGE.md) and
[verification record](../formal/topics/21-dag-spectral/VERIFICATION.md).

The original noisy-Markov-design corollary also depends on stochastic
locality and a finite-history graph producer. Those dependencies are
outside topic 21. Only the algebraic transfer conditional on their uniform
PSD sandwich is included. The represented-matroid extension is topic 22,
and no practical solver timing or priority claim follows from this work.
