# Independent source inventory: DAG spectral approximation sets

Date: 2026-09-20. This review fixes the mathematical obligations and source
boundaries before implementation. It does not claim that the topic is
already formally verified. Only topic 21 is authorized by this inventory.

## Sources and scope

The primary source is
[A polynomial-size spectral approximation set of feasible DAG paths](../../../notes/research-20260912-dag-psd-approximation-set.md),
Sections 1–7. Its predecessor is
[D-optimal design on a finite information graph at fixed parameter dimension](../../../notes/research-20260912-fixed-parameter-doptimal-fptas.md),
Sections 1–4. The current manuscript statements are
`thm:dag-spectral-set`, `lem:spectral-normalization`, and
`subsec:spectral-consequences` in
[03-approximation.tex](../../../paper-correlated-measurements/sections/03-approximation.tex).
The [historical independent review](../../../notes/research-20260912-psd-approximation-set-independent-review.md)
supports the source proof but is not a review of the new Lean statements.

Topic 21 covers the complete explicit-DAG algorithm: input normalization,
all-rank trial generation, actual path production, the all-target relative
PSD sandwich, exact singular ranges, output size, termination and Turing
bit complexity, and the stated criterion consequences. It also covers
the algebraic finite-memory transfer in Section 7 of the primary note,
conditional on a separately supplied uniform matrix sandwich.

The source paper's broader original-design corollary
`cor:true-spectral-cover` additionally invokes stochastic locality bounds
and polynomial finite-history graph construction under all four promise
classes of `thm:trace-fptas`. Those producers and stochastic theorems are
outside the explicit-DAG input scope of topic 21. Proving the conditional
sandwich composition must not be described as formal verification of
that entire original-design corollary. The predecessor's noisy Markov
design corollary has the same dependency boundary.

The normalization lemma is shared with topic 22, but topic 21 applies it
to paths only. The represented-matroid theorem, contraction, determinant
profile interpolation, and base recovery in the later manuscript section
and [approximation appendix](../../../paper-correlated-measurements/appendices/approximation.tex)
remain topic 22. The appendix's scalar Gaussian-message predecessor,
its separate normalization/regularization argument, and numerical-model
qualifications do not provide the rational DAG normalization used here.
They are not additional topic-21 obligations. Likewise, the earlier
individual-channel hardness claim, practical solver certificates,
literature priority, and numerical runtime comparisons are outside this
package.

## Input and output contracts

The input is an explicitly encoded finite directed acyclic graph with
specified vertices `s,t`, real-symmetric PSD matrices whose entries are
rational, a rational symmetric PSD prior, fixed matrix dimension `p>=1`,
and rational accuracy `0<eta<1`. Every edge has its own identity and
owner label, including when several edges have identical matrices.
Parallel edges may be represented distinctly. A supplied topological
ordering must be verified or constructed; an arbitrary input graph must
not silently acquire one as an unverified certificate.

For an actual source-to-sink path `P`, the information is
`J(P)=Q0+sum_(e in P) Q_e`. Each edge is selected at most once because
the graph is acyclic. Side constraints are supported only through the
explicit graph representation. The theorem does not promise a small
graph for arbitrary binary resource budgets or unencoded constraints.

The result is a finite set of actual feasible paths, with the quantifiers

```text
for every feasible P, there exists one P_hat in C such that
(1-eta) J(P) <=PSD J(P_hat) <=PSD (1+eta) J(P).
```

The same representative satisfies both inequalities in every direction.
It is not a direction-dependent lower envelope, a convex combination of
paths, or an approximately feasible object. The set is constructed before
choosing a scalar criterion. Its paths need not be Pareto optimal.

If no source-to-sink path exists, return the empty set and detect
infeasibility. If `s=t`, acyclicity permits only the empty path, whose
information is the prior; return its exact singleton, including zero or
singular priors. For the remaining cases set `N=max(1,|V|-1)`, a valid
bound for every path and prefix length.

## Complete obligation inventory

The identifiers below label source obligations. Final claims may regroup
them, but every substantive conclusion remains required.

| ID | Required mathematical or algorithmic conclusion |
|---|---|
| G01 | Construct or verify a topological order for the explicit DAG, prove every accepted edge advances it, establish the `N` path-length bound, and provide exact reachability with an actual path or infeasibility result. Handle `s=t` and empty feasible families. |
| N01 | An actual rational pivoted PSD elimination produces at most `p` nonzero factors `w_j v_j v_j^T` per edge/prior, with rational `w_j>0`, nonzero rational `v_j`, exact reconstruction, and retained owner labels. Prove termination, including singular and zero matrices, and the label bound `M<=p(|E|+1)`. |
| N02 | Prove the required PSD foundations: sums have kernel equal to the intersection of summand kernels, rank-one factors span the information range, zero PSD sums have only zero summands, and `abs(A_ij)^2<=A_ii A_jj`. These must refer to actual matrices, kernels, ranges, and PSD order. |
| N03 | For every `1<=r<=p`, enumerate all `r`-element label subsets and test full column rank exactly over the rationals. Fix a deterministic order of their columns. There are at most `binom(M,r)` trials. A basis with incompatible owners is allowed as a trial, not presumed feasible. |
| N04 | For full-column-rank `V`, construct rational `L=(V^T V)^(-1)V^T` and `Pi=V L`; prove `LV=I`, projector symmetry/idempotence and exact range. Implement the exact prior test `Pi Q0=Q0` and edge tests `Pi Q_e=Q_e`. |
| N05 | Produce rational dyadic scales `tau_i=2^k_i>0` by terminating exact comparisons, with `1<=tau_i^2 w_i<4`. Prove exponent and encoding-length bounds from the original rational weights. No square-root computation or maximum-volume oracle is part of the algorithm. |
| N06 | Construct `T=diag(tau)L`, `K=V diag(tau^-1)`, prove `TK=I`, `KT=Pi`, and exact reconstruction `Q=K(TQT^T)K^T` for every retained symmetric atom/prior. Establish PSD preservation under these rectangular congruences. |
| N07 | Apply the diagonal magnitude filter `A_ii<=4p` to `A=TQT^T`, rejecting a prior or deleting an edge otherwise. Prove every retained entry has absolute value at most `4p`. These are exact rational tests. |
| N08 | Track the distinct nonprior owners among the selected basis labels, at most `r` in number. Every accepted path containing them has normalized information at least `diag(tau_i^2 w_i)>=I_r`. Prior factors, repeated owners, incompatible owners, and deleted owners are handled correctly. |
| N09 | For every target path of positive information rank `r`, construct a maximum-volume basis among its actual weighted factors. Prove all target factors have basis coordinates of absolute value at most one, including factors in a proper rank-`r` subspace. Connect this proof-only real basis to an enumerated rational label trial. |
| N10 | Prove the trial from N09 preserves the target's prior and every edge under both exact-range and magnitude filters, and that the target satisfies its forced-owner condition. For every accepted path, prove its original information range is exactly the trial range, rather than merely contained in it. |
| P01 | With `h=eta/(rN)>0`, compute all upper-triangular labels `floor(A_e,ij/h)` as exact signed integers. Keep the common prior unrounded. For every path/prefix of at most `N` edges, prove each rounding residual lies in `[0,Nh)`, including negative entries and the empty path. |
| P02 | Define and execute the topological dynamic program on states `(vertex,owner mask,summed signed label vector)`, retaining one actual representative per reachable state. Prove initialization, every transition, termination, witness feasibility, and completeness of all reachable states. |
| P03 | Prove that replacing a prefix by its representative preserves every feasible suffix and final state. The proof must use acyclicity to exclude a repeated-vertex or repeated-edge conflict; it cannot assume that arbitrary path concatenation is feasible. No path-length label is required, but this must follow from the residual and continuation arguments. |
| P04 | Return every complete-owner terminal representative across all ranks/trials. Removing duplicates by actual path identity is allowed. Every returned object is an actual source-to-sink path. Every positive-rank target has a terminal representative in its surviving trial. |
| P05 | Handle rank zero by checking `Q0=0` and finding one path using only zero-matrix edges. Prove this covers exactly every possible zero-information target, even if positive-rank paths coexist. A nonzero prior excludes rank-zero information. |
| S01 | Equal signed summed labels imply every entry of the symmetric normalized difference has absolute value below `Nh`, even for paths of different lengths. Derive the spectral/quadratic-form bound `-eta I<=Delta<=eta I` from `rNh=eta`, with the exact factor `r`, not an unproved norm-equivalence constant. |
| S02 | Use the actual target floor `A(P)>=I_r` to prove both normalized relative inequalities. Undo the rectangular congruence using exact reconstruction to establish the all-target original-space PSD sandwich for the actual producer. |
| S03 | Prove equal kernels and ranges, including singular matrices, both from the sandwich with `eta<1` and/or the exact trial range. No positive-definite prior, positive eigenvalue lower bound, or condition-number premise is permitted. |
| C01 | Establish the signed-label count with `d_r=r(r+1)/2` and `C_r=ceil(8prN^2/eta+N)+2`. Every accumulated coordinate has at most `C_r` possible integer values; differing path lengths and negative floors must be included. |
| C02 | Bound each trial by `|V| 2^r C_r^d_r` states and `|E| 2^r C_r^d_r` edge extensions, subject to explicitly accounted storage/dictionary costs. Tie the counts to the implemented state-merging algorithm rather than exhaustive path enumeration. |
| C03 | Prove the actual output-cardinality bound `1+sum_(r=1..p) binom(M,r) 2^r C_r^d_r`, including exceptional and rank-zero outputs, and bound witness reconstruction/output length by at most `N` edges per path. |
| C04 | Prove polynomial bit lengths for every rational factor, pivot, Gram inverse, projector, scale, transformed entry, comparison, floor, and path sum from the raw encoded input. Small positive pivots and almost dependent bases must be included; a unit-cost arithmetic count does not prove this claim. |
| C05 | Give a deterministic finite implementation/algorithmic realization with polynomial Turing bit work in the entire explicit input length and `1/eta` for fixed `p`, accounting for primitive arithmetic, dictionary operations, all trials, and path recovery. The polynomial exponent may depend on `p`; no dimension-independent FPT claim is made. |
| O01 | For any nonnegative PSD-order-monotone function homogeneous of positive degree `q`, a best representative has value at least `(1-eta)^q` times the feasible optimum, whenever the feasible family is nonempty. Concavity is unnecessary. An arbitrary function still needs a specified evaluation/comparison procedure. |
| O02 | Derive determinant factor `(1-eta)^p`, determinant-root factor `1-eta`, and the `(1-epsilon)` D-optimality scheme using `eta=epsilon/p` and Bernoulli's inequality. Give exact rational determinant comparison and preserve the zero-optimum/all-singular cases. This also supplies the explicit-DAG predecessor theorem. |
| O03 | Derive the E-optimality factor `1-eta` for the actual minimum eigenvalue. Verify a fixed-degree exact algebraic comparison realization with polynomial bit work for rational fixed-size matrices, including repeated/equal eigenvalues; do not silently assume a real-number oracle. If all feasible matrices are singular, the optimum is zero. |
| O04 | Prove inverse order and trace bounds on positive definite matrices, yielding conventional A-cost ratio `1/(1-eta)` and `1+epsilon` at `eta=epsilon/(1+epsilon)`. Prove the set detects whether any positive-definite feasible information exists; singular matrices have infinite cost, not an ordinary finite approximation ratio. Inverses/traces are rational and exactly comparable. |
| O05 | On the proved common range, establish the two-sided Moore–Penrose inverse sandwich with factors `1/(1+eta)` and `1/(1-eta)`. Preserve estimability of a specified contrast and derive its A-type minimum-cost bound, plus sums for finitely many estimable contrasts with nonnegative weights. Handle the zero contrast and zero variance without division by the optimum. No different-kernel inverse-order rule may be assumed. |
| O06 | Prove reuse of the same path set after adding any common PSD prior or applying any common, possibly rectangular, congruence. State the evaluation assumptions for the resulting selected criterion. |
| T01 | Given an explicit PSD-edge graph and a separately supplied uniform finite-memory sandwich `(1-delta)J<=J_L<=(1+delta)J`, prove the true-matrix factors `(1-eta)(1-delta)/(1+delta)` and `(1+eta)(1+delta)/(1-delta)` for every target and its returned representative. Require `0<=delta<1`; include singular information. |
| T02 | For rational `0<epsilon<1`, `eta=epsilon/4`, and `delta<=epsilon/8`, prove both true-matrix factors lie within `1±epsilon`, including the source's lower-deficit bound `epsilon/2` and upper-excess bound `17epsilon/28`. This is algebraic transfer, not verification of an upstream stochastic graph producer. |
| B01 | Verify the stated singular-range obstruction: `a=(1,0)`, `b=(1,t)` with nonzero rational `t` give different rank-one kernels, with neither matrix dominating a positive multiple of the other despite arbitrarily small entrywise difference. Explain why deleting a PSD-dominated representative can lose the upper half of the cover. These delimit the actual guarantee. |

## Source audit and difficult proof steps

No substantive defect in the explicit-DAG theorem or its algebraic
corollaries was found during this inventory. The historical independent
review reaches the same conclusion. The principal implementation risks
are omitted producers or strengthened premises, not an identified false
inequality.

The maximum-volume choice is made separately for every target path,
not just for an optimizer of one criterion. Its weighted vectors can
involve square roots only in the proof. Because weights are positive,
independence of their weighted columns is equivalent to independence of
their rational label columns. The algorithm enumerates all label trials;
it need not compute that target-dependent maximizing basis.

Rectangular reconstruction needs the exact range test and symmetry.
For a retained matrix, `Pi Q=Q` and symmetry give `Q Pi=Q`. Without
these facts, closeness of `TQT^T` says nothing about components outside
the guessed range. A statement about arbitrary normalized matrices
with assumed reconstruction would leave the central producer obligation
unfinished.

Repeated basis owners must be deduplicated only in the mask, not in
the factor sum. A single selected edge contains all its distinct basis
factors. Conversely, a trial whose required owner was removed by a
filter must simply have no accepted path. It is not valid to remove that
owner from the requirement and retain the `A>=I` conclusion.

For signed floors, both residuals lie in the same half-open interval
`[0,Nh)`. Their difference is bounded by `Nh`, not `2Nh`. This remains
true when lengths differ. The prior cancels exactly because it is never
rounded. Empty paths satisfy the strict upper bound because `N>=1`
and `h>0`. The bound is on a single common representative matrix in all
directions, not a different representative for each quadratic form.

The count `C_r` follows from edge labels in
`[-4p/h-1,4p/h]` and at most `N` additions. The displayed extra two
integer values safely cover endpoints. The terminal mask factor `2^r`
is conservative because only a complete mask is actually returned.
Any simpler polynomial implementation of dictionary lookup must still
account for its extra work; the source's edge-extension count does not
make dictionary access unit-cost automatically.

For E-optimality, saying that the eigenvalue is algebraic is not alone
a polynomial-time comparison proof. Fixed degree, coefficient-height
bounds, root isolation/separation, and exact equality handling are all
relevant. For contrast costs, the matrix inequalities apply to arbitrary
real contrasts; rational bit-complexity evaluation requires encoded
rational contrasts/weights or an explicitly supplied comparison method.
The generic criterion caveat in the source should remain visible in the
final documentation. An absent feasible path is distinct from a
nonempty family having zero maximum information or infinite minimum
A-cost.

The predecessor determinant construction can be recovered by running
the spectral-cover producer with accuracy `epsilon/p` and comparing
determinants. Its full-rank signed-label spacing is then precisely
`epsilon/(p^2 N)`, matching the predecessor. No second independent
producer is needed merely to reproduce this already implied theorem.
No multiplicative guarantee for log-determinants follows from these
determinant ratios.

## Existing foundations and proof decomposition

The repository has no previously verified all-rank spectral DAG producer
identified by this inventory. `Formal/QuadraticPrecision/Spectral.lean`
and Mathlib's `Analysis/Matrix/Spectrum` provide actual real Hermitian
spectral/rank facts. Mathlib also has matrix rank, inverses, Schur
complement identities, and PSD order facts. The reciprocal-anchor PSD
file is specialized to a three-by-three arrow matrix and does not
already discharge the general normalization theorem.

Mathlib's `Analysis/Matrix/LDL.lean` proves a noncomputable
positive-definite decomposition through Gram–Schmidt over `RCLike`.
It is not the singular-PSD rational pivoting producer required by N01.
The latter needs explicit rational elimination and a link to the real
PSD semantics. Similarly, a real spectral theorem is useful to prove
criterion inequalities but is not an exact rational eigenvalue-comparison
algorithm.

`Formal/ReciprocalAnchor/ManyBitCost.lean` provides explicit schoolbook
addition, multiplication, division, gcd normalization, and rational-step
cost bounds. `ManyEvaluatorBitCost.lean` illustrates tying those primitive
costs to an actual producer's arithmetic charge and operand families.
These are possible reusable foundations for C04–C05; they do not give
topic-21 operand bounds without a new proof.

Independent implementation blocks are: rational PSD factorization;
rectangular normalization and all-target maximum-volume coverage;
actual graph/path and profile-state DP; signed-label spectral estimates;
producer size/bit complexity; and criterion/conditional-transfer
consequences. Final assembly must compose these into one actual
deterministic producer. Conditional statements that assume its correct
trials, bounded state set, or feasible representatives do not complete
the headline theorem.

## Verification evidence and documentation boundary

This inventory read the source notes, manuscript sections, relevant
appendix boundaries, historical review, existing Lean foundations, and
the beginning and interfaces of
[review_psd_approximation_set.py](../../../code/research_20260912/review_psd_approximation_set.py).
That checker contains a small exact label-DP implementation and uses
exhaustive path enumeration as an independent reference. Its saved
fixture results are useful corroboration, not a proof of the universal
algorithm, complexity, or Lean/software correspondence. No checker,
Lean build, project-wide verification, or CI inspection was run for
this source inventory.

Final note and paper updates should identify exactly which producer,
arithmetic model, and mathematical consequences have been checked.
They should preserve the large fixed-dimension exponent, unresolved
priority, absence of demonstrated practical performance, and the
conditional status of transfer from an externally supplied finite-memory
graph. They must not mark the full stochastic original-design corollary,
represented-matroid extension, or the complete correlated-measurements
manuscript verified by this explicit-DAG package.
