# A polynomial-size spectral approximation set of feasible DAG paths

Date: 2026-09-12. Status: theorem and corollaries passed a
[fresh independent review](research-20260912-psd-approximation-set-independent-review.md).
Priority is unresolved. This is a complexity result, with a large polynomial
exponent. Topic 21 contains an executable Lean reference construction with
proved correctness and bit-work bounds, independently reviewed. It is not a
practical solver.

The proposed extension of the
[reviewed determinant scheme](research-20260912-fixed-parameter-doptimal-fptas.md)
retains paths from every normalization trial. The resulting set approximates
every feasible information matrix in both directions under the positive
semidefinite order. Enumerating the exact range of singular matrices avoids
a lower eigenvalue assumption. The set can then serve several design
criteria without rerunning the graph dynamic program.

## 1. Statement and scope

Fix the matrix dimension `p>=1`. The input is an explicitly encoded finite
DAG `G=(V,E)`, source `s`, sink `t`, rational symmetric PSD edge matrices
`Q_e`, and a rational symmetric PSD prior `Q0`, all of order `p`. Write

```text
J(P) = Q0 + sum_(e in P) Q_e
```

for an `s-t` path `P`. Given rational `0<eta<1`, the proposed algorithm
constructs a set `C` of actual feasible paths such that, for every feasible
path `P`, some `P_hat in C` satisfies

```text
(1-eta) J(P) <=_PSD J(P_hat) <=_PSD (1+eta) J(P).       (1)
```

In particular, the two matrices have the same kernel. The cardinality of
`C` and the algorithm's Turing bit complexity are polynomial in input
length and `1/eta` for fixed `p`. No positive definite prior, positive
eigenvalue lower bound, or Euclidean condition-number bound is assumed.

If no feasible path exists, report that fact and return the empty set.
If `s=t`, the empty path is the only path and gives an exact singleton set.
Otherwise put `N=max(1,|V|-1)`. A path has at most `N` edges.

The claim concerns explicit DAGs. Cardinality, spacing, and other finite
restrictions may be encoded in vertices, but arbitrary side constraints
or binary-encoded resource budgets need not have a polynomial-size graph.
The exponent depends on `p`; this is not a dimension-independent
fixed-parameter running-time bound.

The term **approximation set** is deliberate. Its paths need not be
Pareto optimal. Removing PSD-dominated paths would preserve a one-sided
maximization guarantee, but could destroy the upper half of (1).

## 2. Exact normalization on an enumerated range

Use rational LDL factorization once to write each input matrix as
a sum of at most `p` nonzero factors:

```text
Q_e = sum_(j owned by e) w_j v_j v_j^T,
Q0  = sum_(j owned by prior) w_j v_j v_j^T,
w_j > 0 rational; v_j rational.                      (2)
```

Zero matrices have no factors. The decomposition is valid for singular
PSD matrices. The implemented recursion inspects the leading diagonal.
A zero leading entry forces its entire row and column to zero, so that
coordinate is skipped. A nonzero leading entry is positive and leaves a
rational PSD Schur complement. Each recursive call removes one coordinate.
No square roots or pivot-search oracle are needed. Retain factor
labels and their owners. Let `M<=p(|E|+1)` be the number of labels.

For each rank `r=1,...,p`, enumerate all sets of `r` labels whose rational
columns form a full-column-rank matrix `V_b` of size `p` by `r`. Fix the
column order by label order. This is a trial, not a claim that the labels
belong to any feasible common path.

Define

```text
S = range(V_b),
L = (V_b^T V_b)^(-1) V_b^T,
Pi = V_b L.                                         (3)
```

All three matrix expressions are rational; `Pi` is the orthogonal
projector onto `S`. Reject the trial if `Pi Q0 != Q0`. Delete any edge
with `Pi Q_e != Q_e`. These are exact rational tests. They restrict every
retained matrix's range to `S`.

Choose powers of two `tau_i` such that `1<=tau_i^2 w_bi<4`, using exact
rational comparisons. Set

```text
T = diag(tau_i) L,          K = V_b diag(1/tau_i),
A_e = T Q_e T^T,           A0 = T Q0 T^T.             (4)
```

Then `T K=I_r`, `K T=Pi`, and for every retained matrix `Q`,

```text
Q = K (T Q T^T) K^T.                                (5)
```

Equation (5) uses both symmetry and the exact range restriction.
Congruence alone would not permit reconstruction outside `S`.

Reject the trial if a diagonal entry of `A0` exceeds `4p`. Delete any
retained edge whose transformed matrix has a diagonal entry above `4p`.
All remaining matrices are PSD, so every entry has absolute value at most
`4p`. Require all distinct edge owners of the selected basis factors to
appear in the output path. Track at most `r` such owners with a bitmask;
selected prior factors need no bit. Every accepted path then satisfies

```text
A(P) = A0 + sum_(e in P) A_e
     >=_PSD diag(tau_i^2 w_bi) >=_PSD I_r.             (6)
```

An edge is traversed at most once in a DAG, so factors sharing an owner
are present with their correct multiplicities. Together with the range
restriction, (6) says the original matrix has range exactly `S`.

## 3. Signed integer labels and output set

For the rank-`r` trial set

```text
h = eta/(r N),
Z_e,ij = floor(A_e,ij/h),       1<=i<=j<=r.            (7)
```

Floor includes negative entries. Do not round the common prior `A0`.
In topological order, run a dynamic program with states

```text
(vertex, owner-mask, sum of upper-triangular integer labels).
```

Keep one actual path per reachable state. Transitions add edge labels
and update owner masks. This computes all reachable states exactly:
every future extension depends only on the current vertex and recorded
state. Strict increase in the verified topological order prevents a suffix
from revisiting a vertex or edge in either prefix. Thus replacing a prefix
by its representative preserves feasible continuations as well as the
recorded state.
At `t`, retain every representative with a complete owner mask. Add these
paths to `C` for every basis trial and every rank. Duplicates may be
removed by path identity; no scalar objective is evaluated.

Handle `r=0` separately. A zero information matrix is possible only when
`Q0=0` and every edge on the path has `Q_e=0`. If `Q0=0`, search the
subgraph containing exactly these zero-matrix edges and add one path if
it exists. This covers all rank-zero paths exactly.

## 4. Proof of the spectral guarantee

Fix any feasible path `P` of rank `r>0`, not necessarily optimal for any
criterion. Its factors from (2) span `S_P=range J(P)`. To see this, a
vector is in the kernel of a sum of PSD matrices if and only if it is in
the kernel of every summand. Thus no factor on `P` leaves `S_P`.

Introduce `u_j=sqrt(w_j) v_j` only for the proof. Choose `r` such vectors
from the prior and `P` that maximize their `r`-dimensional volume. For
their matrix `B`, this volume squared is `det(B^T B)>0`. Every other
factor vector in the path has coordinates `u=B x` satisfying

```text
|x_i| <= 1 for each i.                               (8)
```

Indeed, replacing column `i` by `u` multiplies the volume by `|x_i|`;
a larger coordinate would contradict maximality. The algorithm need not
find this maximum-volume basis: it enumerates its label set among its
trials. The Lean proof performs determinant replacement in coordinates of
the factor span, so the argument also applies to a proper subspace of the
ambient space. It then reorders the selected labels into the trial
producer's deterministic increasing order. In that trial, `S=S_P`, so the prior and all edges of `P` survive
the exact range tests.

For this trial, `T B=diag(tau_i sqrt(w_bi))`. Equations (8) and
`tau_i sqrt(w_bi)<2` imply that every coordinate of each transformed
factor vector in `P` has absolute value below `2`. Each individual
matrix has at most `p` factors, so its transformed diagonal is at most
`4p`. The prior and every edge of `P` survive the magnitude filters.
The path also contains the selected owners, and (6) holds for it.

The exact DP therefore reaches `P`'s terminal integer-label state with a
complete owner mask. Let `P_hat` be the representative stored there.
For any path of at most `N` edges and each upper-triangular coordinate,

```text
0 <= sum_e A_e,ij - h sum_e floor(A_e,ij/h) < N h.     (9)
```

Both paths have the same integer sums and common prior. Consequently
every entry of `Delta=A(P_hat)-A(P)` has absolute value below `N h`.
Symmetry and the row-sum bound give

```text
||Delta||_2 <= r N h = eta.
```

Since `A(P)>=_PSD I_r`,

```text
(1-eta) A(P) <=_PSD A(P_hat) <=_PSD (1+eta) A(P).     (10)
```

Congruence by the rectangular matrix `K` and (5) yield (1). Both paths
have range exactly `S_P` by the range tests and owner requirement. The
rank-zero case was handled separately. This proves the assertion for
every path, with a representative that may depend on that path.

### Why exact ranges matter

For `a=(1,0)^T` and `b=(1,t)^T`, with any nonzero rational `t`, the PSD
rank-one matrices `aa^T` and `bb^T` are arbitrarily close entrywise as
`t` tends to zero. Neither can dominate a positive multiple of the other:
their kernels differ. Thus entrywise rounding in the ambient space cannot
by itself prove a relative guarantee for singular matrices. The range
enumeration preserves the relevant face of the PSD cone exactly.

## 5. Bit complexity and cardinality

There are at most `binom(M,r)` rank-`r` trials. Let

```text
d_r = r(r+1)/2,
C_r = ceil(8 p r N^2/eta + N) + 2.                   (11)
```

Each retained arc entry has magnitude at most `4p`. Over at most `N`
edges, one signed integer sum has at most `C_r` possible values. Thus
there are at most `|V| 2^r C_r^(d_r)` states and
`|E| 2^r C_r^(d_r)` edge extensions per trial, up to fixed-dimensional
arithmetic and dictionary factors. A conservative bound on terminal
representatives is

```text
|C| <= 1 + sum_(r=1)^p binom(M,r) 2^r C_r^(d_r).      (12)
```

In fixed dimension, LDL factors, `(V_b^T V_b)^(-1)`, dyadic scales,
range tests, transformed matrices, and integer floors have polynomial
bit length and can be computed in polynomial bit complexity. Very small
nonzero pivots or very large dyadic exponents increase bit length, not
the numerical range of the DP labels. The reference DP uses lists, rather than an optimized dictionary. If
`B_r=2^r C_r^(d_r)`, its retained table has at most `|V| B_r` entries,
but a vertex may temporarily hold `1+|E| B_r` candidate paths before
merging. A conservative full-scan comparison count is
`|V| (1+|E| B_r)^2`; key evaluation, edge scans, and arithmetic are
additional charges. Stored whole paths add a factor of at most `N` to
copying and storage. Path reconstruction has at most
`N` edges per representative. The maximum-volume proof uses square roots
but the algorithm does not; all implemented comparisons can be rational.

This is a polynomial bound for fixed `p`, not an attractive running-time
prediction at moderate dimension. An independent exact checker exercises
all basis trials on small instances, using exhaustive path enumeration for
verification. The executable Lean reference producer is separate from that checker.
No practical solver benchmark is asserted.

## 6. Consequences for design criteria

The same computed set works for an objective chosen afterwards. A
separate objective evaluation/comparison procedure is still needed; the
matrix theorem alone does not supply an oracle for an arbitrary function.

For a nonnegative Loewner-nondecreasing function `Phi` homogeneous of
degree `q>0`, the best representative has value at least
`(1-eta)^q max_P Phi(J(P))`. No concavity is required for this deduction.
Loewner monotonicity without a scaling or continuity condition does not
imply a multiplicative scalar guarantee.

Concrete consequences include:

- **D-optimality:** taking `eta=epsilon/p` gives a `(1-epsilon)`
  determinant approximation by Bernoulli's inequality. Rational
  determinants can be compared exactly. Determinant roots have factor
  `1-eta`; this is not a multiplicative log-determinant statement.
- **E-optimality:** the largest `lambda_min(J)` in the set has factor
  `1-eta`. The reference comparator uses rational characteristic coefficients of
  the Kronecker difference `A tensor I - I tensor B` to bound every
  nonzero eigenvalue difference away from zero. Rational PSD threshold
  tests and a finite dyadic bisection then distinguish less, equal, and
  greater, including repeated eigenvalues. Its complete rational arithmetic
  trace has a verified bound `C(p)(B+1)^5` for input entry bit bound `B`.
  If all paths are
  singular, the optimum is zero.
- **A-optimality:** among positive definite matrices, the least
  `tr(J^(-1))` in the set has cost at most `1/(1-eta)` times optimum.
  Set `eta=epsilon/(1+epsilon)` for a `(1+epsilon)` minimization ratio.
  Inverses and traces are rational. Assign infinite cost to singular
  matrices; if no positive definite path exists, the set detects this.

The common-kernel guarantee also preserves estimability of a specified
contrast `c`. On that common range, inversion gives the corresponding
two-sided bounds for Moore-Penrose inverses. Hence `c^T J^dagger c`, with
infinite cost when `c` is not estimable, inherits the A-type minimization
bound. This is a same-range argument; the pseudoinverse is not claimed
to be order reversing across arbitrary different kernels.

Two useful algebraic properties require no new algorithm. For any
additional common prior `H>=0`, (1) remains true after adding `H` to both
matrices. It also remains true after any common congruence `J -> R J R^T`.
Thus the set can be reused after these operations, with ordinary
qualifications about evaluating the chosen criterion.

## 7. Transfer from a finite-memory information graph

Suppose a separately established finite-memory construction provides,
uniformly for every feasible design path,

```text
(1-delta) J(P) <=_PSD J_L(P) <=_PSD (1+delta) J(P),
0 <= delta < 1.                                      (13)
```

Apply the present scheme to its explicit additive PSD graph. For every
true matrix `J(P)`, its representative satisfies

```text
[(1-eta)(1-delta)/(1+delta)] J(P)
  <=_PSD J(P_hat)
  <=_PSD [(1+eta)(1+delta)/(1-delta)] J(P).             (14)
```

The result includes singular matrices because (13) preserves kernels.
For rational `0<epsilon<1`, choose `eta=epsilon/4` and require
`delta<=epsilon/8`; both factors in (14) then lie within
`[1-epsilon,1+epsilon]`. For the upper factor its excess over one is
`(eta+2delta+eta delta)/(1-delta)`, bounded by
`(epsilon/2+epsilon^2/32)/(1-epsilon/8) <= 17 epsilon/28`.
The lower factor's deficit is at most `eta+2delta<=epsilon/2`.

Whether this yields an FPTAS for the original design input depends on
the graph construction. The fixed-correlation, bounded-noise-ratio,
fixed-parameter-dimension full-block model and its explicit restrictions
are those in the reviewed determinant note. This extension does not
remove those restrictions or cover arbitrary dense measurement errors.

## 8. Prior audit and proposed contribution boundary

The following are comparisons of the source statements read, not a
claim that the absence of a matching search result establishes novelty.

**Approximate Pareto sets and profile dynamic programming are established.**
Papadimitriou and Yannakakis (2000), Tsaggouris and Zaroliagis (2009), and
Mittal and Schulz (2013, Operations Research) give foundational schemes
for finitely many nonnegative additive objectives. Their read hypotheses
do not directly provide relative PSD approximation from signed matrix
entries: entrywise relative accuracy can destroy a small eigenvalue.
The precise source audit and cancellation example are in the
[determinant note, Section 6](research-20260912-fixed-parameter-doptimal-fptas.md).
These results are direct antecedents of the integer-label DP, not ideas
to claim as new.

**Design normalization and several criteria are already combined.**
Brown, Laddha, and Singh (2024),
[Fast algorithms for maximizing the minimum eigenvalue in fixed dimension](https://par.nsf.gov/servlets/purl/10548928),
give a randomized fixed-dimensional PTAS for partition and matroid
constraints and discuss a broad class of concave monotone homogeneous
criteria. Their proof guesses a subset, normalizes, filters large
vectors, and forces the guessed subset. Thus normalization, filtering,
owner forcing, and transfer to several criteria are not new individually.
The proposed distinction is deterministic polynomial dependence on
`1/eta` for an explicit DAG, with one objective-independent set and exact
handling of all singular ranges. A PTAS with an accuracy-dependent
exponent does not by itself establish that statement.

**PSD pruning in covariance dynamic programs is old and directly relevant.**
Atanasov, Le Ny, Daniilidis, and Pappas (2014),
[Information Acquisition with Sensing Robots: Algorithms and Error Bounds](https://www.georgejpappas.org/wp-content/uploads/2024/04/0528.pdf),
ICRA, DOI `10.1109/ICRA.2014.6907811`, define algebraic redundancy by PSD
domination of a convex combination of covariance states, and relaxed
redundancy after an additive `epsilon I` shift. Their Section IV uses it
to prune a forward Riccati DP. Theorem 3 bounds additive terminal
log-determinant loss through a positive process-noise eigenvalue and an
optimal-trajectory covariance bound. It does not state the relative
all-information-matrix cardinality and bit-complexity guarantee (1).
Its gas-concentration application makes this particularly relevant prior.
Convex-combination dominance can retain a different path for each scalar
criterion; it does not immediately give the single feasible
representative in the two-sided matrix sandwich.

Vitus, Zhang, Abate, Hu, and Tomlin (2012),
[On efficient sensor scheduling for linear dynamical systems](https://engineering.purdue.edu/~jianghai/Publication/Automatica2012_sensor.pdf),
Automatica 48(10):2482–2493, DOI `10.1016/j.automatica.2012.06.092`,
is the earlier source for that redundancy machinery. The author-posted
preprint's Section 2 assumes positive definite process noise. Section 5
develops additive covariance/cost pruning; Theorem 6 gives an additive
average accumulated-trace error bound involving peak covariance and the
process-noise eigenvalue. The read result is not a conditioning-free
relative spectral cover of all feasible additive information sums.

**Multiplicative relaxed covariance DP is also earlier work.**
Alriksson and Rantzer (2005),
[Sub-Optimal Sensor Scheduling with Error Bounds](https://portal.research.lu.se/en/publications/sub-optimal-sensor-scheduling-with-error-bounds/),
DOI `10.3182/20050703-6-CZ-1902.01192`, is an earlier relaxed-DP source
cited by Vitus et al. Its model and Section 3 were read in the authorized
reprint, Paper V of Alriksson's 2008 thesis, printed pages 137–148
([institutional thesis record](https://www.lunduniversity.lu.se/lup/publication/55817061-3253-44fd-a6cf-9c568df96185)).
The method uses multiplicative upper/lower slack parameters in covariance
recursions. Procedure 2 compares pointwise lower envelopes of quadratic
forms: it tests whether some vector `x` makes one quadratic form smaller
than every retained form. The minimizing retained matrix may depend on
`x`; this is not a single feasible matrix that sandwiches a given target
matrix in every direction. The read sections do not establish a
polynomial Turing/cardinality bound. Thus a claim to introduce
multiplicative covariance pruning would be incorrect; the proposed
all-target matrix sandwich is a more specific distinction.

For example, `min{x^T diag(0,2)x, x^T diag(2,0)x} <= x^T I x` for
every `x`. A lower-envelope representation may therefore discard `I`,
although neither retained singular matrix approximates `I` relatively in
PSD order. This quantifier difference persists even with exact envelopes.

Lincoln and Rantzer (2006),
[Relaxing Dynamic Programming](http://www.derongliu.org/adp/adp-cdrom/refs/lincoln20061249.pdf),
DOI `10.1109/TAC.2006.878720`, develop the underlying multiplicative
Bellman inequalities and minimum-of-quadratics representation in Sections
II–III. Rantzer (2006),
[Relaxed dynamic programming in switching systems](http://www.derongliu.org/adp/adp-cdrom/rantzer-IETCTA-2006.pdf),
IEE Proceedings 153(5):567–574, Theorems 1–3, relates feasibility of
finite-dimensional value iteration to approximation of the scalar
optimal value function and a uniform cost-to-go/stage-cost bound. These
read statements do not imply (1) for all feasible matrices. Their
switched-system graph model also permits changing the continuous state
along edges; the present additive-matrix theorem does not cover that
greater dynamical generality.

**Recent generic approximation-set frameworks still require a reduction.**
Bökler, Chimani, and Jasper (2026),
[One-Exact Approximate Pareto Sets for APX-Hard Multiobjective Problems](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2026.112),
DOI `10.4230/LIPIcs.ESA.2026.112`, was published on 2026-08-25. Its
introduction and formal setup concern fixed finitely many positive
rational objective functions and a relaxed-dual-restriction oracle.
The framework does not directly turn finitely many signed matrix entries
into relative PSD order. A suitable reduction or oracle could still
subsume parts of this construction; the present audit has not proved
that no such reduction exists.

All newly identified sources and available full text were routed to the
shared literature agent. Broader cone-order approximation and relaxed
switched-system DP literature remain priority checks. The bounded search
does not establish originality.

The strongest candidate statement to investigate is the full feasible
spectral approximation set (1), including rank-deficient faces, rational
bit complexity, and objective-independent reuse. The D-, A-, and
E-optimality ratios are consequences, not separate algorithmic inventions.
The large worst-case exponent remains a material limit on practical
significance. Section 9's executable Lean reference producer has proved
schoolbook bit-work bounds, but it is not an optimized solver and supplies
no practical performance or wall-clock evidence.


## 9. Lean verification scope

[Topic 21](../formal/topics/21-dag-spectral/README.md) records the frozen
claims, declaration map, independent reviews, and targeted checks. The
construction starts from the original rational PSD prior and edge matrices
and an explicit graph with a checked topological ordering. It produces the
factor labels, rational normalization trials, filtered owner-aware path DP,
and returned paths; a successful trial or relative-cover certificate is
not supplied as an additional hypothesis. The proved matrix results include
all-target two-sided approximation and exact singular ranges. Criterion
results cover D-, E-, A-, and estimable-contrast guarantees and reuse after a
common PSD prior or congruence.

The whole-producer cost theorem starts from the original matrix and accuracy
encodings. It includes factor initialization, all trials and rejected gates,
cached normalization and labels, dictionary scans, stored-data access, and
path copying and deduplication. The costed core takes verified topological
vertex indices. A separate front end computes an order for arbitrary vertex
numbering; its ordering and endpoint-scan counts are distinct from the core's
bit-work theorem. The exact E comparator and rational D/A/contrast selectors
also have verified execution bounds, including path-matrix construction.
These are schoolbook arithmetic and explicit storage/scan charges, not a
wall-clock guarantee for Lean's runtime. The
[coverage map](../formal/topics/21-dag-spectral/COVERAGE.md) and
[verification record](../formal/topics/21-dag-spectral/VERIFICATION.md) are
the authoritative completion records.

The finite-memory result verified in this package is the conditional
sandwich composition (13)–(14), including the stated epsilon constants.
It assumes the explicit PSD-edge graph and the uniform upstream sandwich.
It does not verify the stochastic locality estimates or construction of a
polynomial finite-history graph for the original measurement-design input.
The represented-matroid extension belongs to topic 22 and is excluded.
The package makes no literature-priority or practical-runtime claim.
