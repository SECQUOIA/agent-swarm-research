# Sharp extinction bounds with unobserved daughter dependence

Date: 2026-09-06. Status: independently verified known-method corollary. The [proof review](../reviews/extinction-proof.md) verifies the statements; the [literature review](../reviews/extinction-literature.md) identifies direct overlap with branching decision-process theory and classical rearrangement. This note is retained as groundwork, not a new standalone theorem.

## Problem and relevance

A population balance specifies expected offspring in each phenotype, but usually not the joint phenotypes of two sisters. Can we bound eventual extinction sharply without choosing that unmeasured joint law? This is relevant to establishment of small microbial populations and to structured birth–death models. It concerns the stochastic mechanism behind a population balance, not clinical guidance.

The statement that sibling dependence can change extinction while leaving mean growth unchanged is already established; see Peter Olofsson, *Branching Processes with Local Dependencies*, Annals of Applied Probability 6 (1996), 238–268, [open author copy](https://www.stat.rice.edu/~olofsson/local.pdf). The candidate contribution under investigation is the exact optimization over all couplings consistent with specified marginals.

## Model

There are m types. At its reproduction event, an individual of type i dies without offspring with probability d_i, or produces exactly two daughters with probability b_i=1-d_i. Conditional on division the ordered daughter types have a symmetric law C_i on {1,…,m}². Its two marginals equal a specified probability vector p_i. Events and subsequent descendant families are independent conditional on their starting types. Thus inherited daughter types may be dependent, but no unrecorded shared environmental noise acts after division.

The admissible set U_i is the compact transport polytope of symmetric nonnegative matrices with row sums p_i. The family C=(C_i) is fixed across generations. The same genealogy can be embedded in continuous time using positive finite exponential event rates a_i. Extinction is unchanged by those clocks. The finite type, finite rate process is nonexplosive.

Write F_C:[0,1]^m→[0,1]^m as

\[
 F_{C,i}(z)=d_i+b_i\sum_{j,k}C_{i,jk}z_jz_k.
\]

The extinction vector q_C is the least fixed point, obtained by iterating F_C from zero. This is standard multitype branching theory.

## Theorem 1: attainable lower and upper envelopes

Define

\[
 T_i(z)=d_i+b_i\min_{C_i\in U_i}\sum_{j,k}C_{i,jk}z_jz_k,
 \qquad
 S_i(z)=d_i+b_i\sum_j p_{ij}z_j^2.
\]

Let q^- and q^+ be the limits of iterating T and S from zero. These limits exist. Then every admissible C satisfies

\[
 q^-\le q_C\le q^+ \quad\text{componentwise}.
\]

Both bounds are attained by single stationary families of couplings, simultaneously for every initial type. The upper family is C_i^+=diag(p_i). For the lower family choose C_i^- to minimize the expression in T_i(q^-).

### Proof

All maps are monotone on the unit cube; minima preserve monotonicity because each quadratic has nonnegative coefficients. Their values lie in the cube. Iteration from zero therefore increases to a limit. The minimum map is continuous: the feasible set is compact, and each objective is uniformly Lipschitz on the cube. Hence each limit is a fixed point and is the least one, by induction against any fixed point.

For every equal-marginal coupling,

\[
 \sum_jp_{ij}z_j^2-\sum_{j,k}C_{i,jk}z_jz_k
 =\tfrac12\sum_{j,k}C_{i,jk}(z_j-z_k)^2\ge0.
\]

Consequently T≤F_C≤S, which gives the claimed bounds by monotone iteration. The diagonal family has F_{C^+}=S and therefore attains q^+.

Select minimizers at q^-, which exist by compactness. Then F_{C^-}(q^-)=T(q^-)=q^-. The least-fixed-point property gives q_{C^-}≤q^-. The universal lower bound gives the reverse inequality. Thus q_{C^-}=q^-.

### Evaluating the minimum

Let Q_{i,z}(u), 0<u<1, be the quantile function of the scalar random variable z_J for J distributed as p_i. The rearrangement inequality gives

\[
 \min_{C_i\in U_i}\sum C_{i,jk}z_jz_k
 =\int_0^1Q_{i,z}(u)Q_{i,z}(1-u)\,du.
\]

One may implement this by sorting types by z_j and matching mass from opposite ends. Ties can be split arbitrarily. A symmetric minimizing type coupling exists by reflecting u↔1-u; no independence assumption is needed. The [independent proof review](../reviews/extinction-proof.md) supplies a self-contained layer-cake proof of the transport identity.

## Identical mean and lineage observations

The offspring mean matrix is M_ij=2b_i p_ij, independent of C. In continuous time, expected type counts with column convention satisfy

\[
 \dot n_j=\sum_i a_i(2b_ip_{ij}-\delta_{ij})n_i.
\]

A chronological lineage that selects one daughter uniformly at each division also sees the same event rates, death probabilities, and transition probabilities p_ij for every coupling. Thus even exact knowledge of all such first-moment trajectories and all single-lineage trajectory laws cannot determine the coupling. Joint sister observations, correlations across descendant families, or extinction observations contain information absent from those data.

These indistinguishability statements assume observation of one randomly chosen daughter, not a selected surviving or fastest-growing daughter, and exclude full-tree or pair-lineage measurements.

## Important boundaries

- If types include exact additive quantities and daughters must satisfy an eventwise conservation law, U_i must be restricted accordingly. The diagonal coupling may be physically inadmissible. The general minimum proof still works for any nonempty compact independently specified U_i; the diagonal maximum formula need not.
- The upper-envelope proof uses one coupling that maximizes the generating function for every z. Merely maximizing at a candidate fixed point is insufficient to prove attainment of a general upper Bellman envelope.
- No claim of fast numerical convergence follows from monotone iteration. Near criticality convergence may be arbitrarily slow.
- This result does not infer the true coupling, and the interval need not be narrow.

## Next checks

Proof and literature checks are complete for the basic statements. The active extensions are [uniform near-critical bounds](extinction-near-critical.md) and [an explicit rule for tied reproductive values](extinction-perron-ties.md). Certified computation and broader novelty assessment remain open.
