# Constructive direction: fixed core with many polyhedral output blocks

Date: 2026-09-05. Status: detailed proof developed and two independent
reviews passed; novelty/source audit remains open.

The supplied final Haugland (2016) article has now been read. Its §6,
printed p. 214, poses precisely the fixed-pool plus fixed-input/output/quality
question. Its actual hardness results allow an unbounded pool count. Thus the
new fixed-input and fixed-quality corollaries answer published questions;
the fixed-output case remains unsettled here. A contrary statement in a 2014
abstract is absent from the final article, and no formal retraction is claimed.
Later-literature novelty remains provisional.

The detailed theorem is in
[the result draft](../results/fixed-core-block-polyhedral-optimization.md).
The draft also proves a stronger complementary application: fixed numbers
of pools and qualities, arbitrary input/output counts, with no bypass arcs
(or only a bounded number of bypass arcs).

## Proposed application

**Candidate.** Standard pooling is polynomial-time solvable when the number
of inputs and the number of pools are fixed, with arbitrarily many outputs
and qualities. Shared input capacities, output blending from several pools,
direct input-to-output bypasses, arc capacities, lower and upper output
throughputs, and linear costs are retained. This is a polynomial bit-complexity
claim with potentially large parameter-dependent exponent, not a practical
strongly polynomial algorithm or an FPT claim.

This would extend the one-pool fixed-input case and address a bounded-input
case of the two-pool question in
[Boland, Kalinowski, Rigterink (2017), §4, question 4](https://optimization-online.org/wp-content/uploads/2015/08/5059.pdf).
That source does not establish the multiple-pool theorem proposed here.

## General structural theorem behind the candidate

Fix integers \(r,d,k,D\). A compact semialgebraic core
\(x\in C\subset\mathbb R^r\) is described by polynomial inequalities
of degree at most \(D\), with rational coefficients. There are \(N\)
continuous blocks \(z_j\in\mathbb R^{d_j}\), \(d_j\le d\), with

\[
P_j(x)=\{z_j:B_j(x)z_j\le b_j(x)\}.
\]

All coefficient functions are rational polynomials of degree at most \(D\).
Every block has explicit finite rational box bounds. The only coupling is

\[
\sum_j A_j(x)z_j=b(x)\in\mathbb R^k,
\]

and the objective is \(c_0(x)+\sum_j c_j(x)^\top z_j\). The proposed
result is exact polynomial-time global optimization for fixed \(r,d,k,D\),
with time polynomial in the total coefficient bit length and number of
constraints and blocks.

The key issue is avoiding an exponential choice of one local basis per
block. Merely observing that fixing the core gives an LP does not suffice.

### Proof plan using support functions

For fixed core \(x\), include objective value as one more aggregate coordinate:

\[
T_j(x)=\{(A_j(x)z_j,c_j(x)^\top z_j):z_j\in P_j(x)\},
\qquad T(x)=\sum_j T_j(x).
\]

If all blocks are nonempty, \(T(x)\) is compact convex. An aggregate point
\((b(x),v-c_0(x))\) belongs to \(T(x)\) exactly when

\[
\lambda^\top(b(x),v-c_0(x))
\le\sum_j\max_{z_j\in P_j(x)}
\lambda^\top(A_j(x)z_j,c_j(x)^\top z_j)
\quad\forall\lambda\in\mathbb R^{k+1}.
\]

Each block has at most \(\binom{M_j}{d_j}\) candidate vertex bases.
For a nonsingular basis the vertex coordinates are rational functions of
\(x\), of degree bounded in terms of \(d,D\). Determinants, vertex
feasibility tests, and pairwise comparisons of support scores are all
polynomials in \((x,\lambda)\) after recording determinant signs. Their
number and coefficient sizes are polynomial; their degrees are bounded.

A sign-invariant semialgebraic decomposition in the fixed-dimensional
\((x,\lambda)\)-space has polynomial complexity. On every realizable sign
condition it records whether each block is nonempty and chooses a support
maximizing candidate vertex for every block. It simultaneously selects all
\(N\) bases without enumerating their Cartesian product. Degenerate and
lower-dimensional cells, including determinant-zero loci, must be retained.
Every nonempty bounded polytope has a vertex with \(d_j\) independent
active rows, including when the polytope is lower dimensional.

On one such cell the sum of selected support scores is rational. Multiplying
their nonzero denominators clears the sum. Its degree may grow linearly in
\(N\); its coefficient size remains polynomial because the number of core
variables is fixed. This degree growth is harmless for polynomial bit
complexity in a fixed-dimensional real-algebraic algorithm. It does prevent
a casual claim of algebraic degree bounded only by the fixed parameters.

Combine the polynomially many sign conditions into a polynomial-size formula
\(\Phi(x,v,\lambda)\) expressing the support inequality and block
nonemptiness. Then

\[
\exists x\in C\ \forall\lambda\in\mathbb R^{k+1}\ 
\Phi(x,v,\lambda)
\]

defines the attainable objective values. The number of quantified and free
variables is fixed. Standard exact quantifier elimination therefore yields
the attainable subset of the real line in polynomial time. Compactness
ensures that its minimum is attained when nonempty. Recovery of all leaf
variables is provided by the algebraic-coefficient LP algorithm of
[Adler–Beling (1994)](https://adler.ieor.berkeley.edu/ilans_pubs/lp_algebraic_1994.pdf):
the fixed-dimensional optimal core and optimum value lie in a common
polynomial-degree field, satisfying that algorithm's field-degree bound.
This proof obligation has been independently checked.

## Pooling encoding

Let the input count be \(m\) and pool count \(p\), both fixed. Use source
fractions \(q_{i\ell}\ge0\), \(\sum_iq_{i\ell}=1\), as the core
(dimension \(mp\)). Fractions on missing input-to-pool arcs are zero.
For every output \(j\), use a block of \(p\) pool-to-output flows
\(v_{\ell j}\) and \(m\) direct flows \(z_{ij}\), setting missing arcs
to zero. Each block has dimension \(p+m\), independently of the quality
count.

With input qualities \(C_{ia}\), the output upper-quality inequality is

\[
\sum_\ell\bigl(\sum_iC_{ia}q_{i\ell}-U_{ja}\bigr)v_{\ell j}
+\sum_i(C_{ia}-U_{ja})z_{ij}\le0.
\]

Lower qualities give the reversed inequality. Output-throughput and arc
bounds are local. Pool capacities, input-to-pool arc capacities, and shared
input capacities give at most \(p+mp+m\) aggregate inequalities:

\[
\sum_jv_{\ell j}\le S_\ell,\quad
q_{i\ell}\sum_jv_{\ell j}\le U_{i\ell},\quad
\sum_j\bigl(\sum_\ell q_{i\ell}v_{\ell j}+z_{ij}\bigr)\le S_i.
\]

Their lower-bound versions can also be included. A fixed number of bounded
slack variables converts them to the general theorem's aggregate equations.
The pool-input flow is recovered as \(q_{i\ell}\sum_jv_{\ell j}\).
Its linear cost contributes coefficient
\(\sum_i c_{i\ell}q_{i\ell}\) to each \(v_{\ell j}\); remaining
arc costs are already local linear costs. Zero-throughput pools cause no
division or representation problem.

## Preliminary literature audit

Searches on 2026-09-05 for fixed inputs and pools, two pools with bounded
inputs, and fixed-dimensional parametric block LPs did not locate this exact
theorem. This is not proof of novelty.

- [Boland et al. (2017)](https://optimization-online.org/wp-content/uploads/2015/08/5059.pdf)
  gives the one-pool fixed-input result and poses the multiple-pool question.
- [Piecewise parametric structure in the pooling problem (2017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6417401/)
  gives constructive multiple-pool subclasses under one quality and flow
  relaxations. Its assumptions need detailed comparison before a novelty claim.
- [Block-Structured Integer and Linear Programming in Strongly Polynomial and Near Linear Time (2020)](https://arxiv.org/abs/2002.07745)
  is a nearby algorithmic reference for few aggregate rows, but its LP data are
  fixed. It does not immediately settle the variable-core global problem.
- The repository's
  [common-factor fixed-linking theorem](../results/common-factor-fixed-linking-optimization.md)
  treats a scalar core and interval leaves by basis enumeration. Its classical
  bounded-LP basis precedent must be acknowledged. The proposed support
  formulation handles higher-dimensional blocks and multiple moving core
  variables.

## Rejected or deferred directions

- Pure treewidth or bounded-degree pooling tractability is not promising:
  the repository has just proved hardness even with all degrees at most two;
  that does not itself settle treewidth, but invalidates a degree-only route.
- Robust Newton/Miranda feasibility certification looks close to standard
  interval and Kantorovich theory unless a stronger structural or complexity
  result is found. Deferred in favor of the concrete pooling question.
- A generic bounded number of integer variables in a nonlinear core is not
  automatically safe: fixed-dimensional nonconvex integer polynomial
  optimization has arithmetic hardness. Restricting a fixed number of binary
  design variables is safe by finite enumeration, but arbitrary integer core
  domains are not claimed here.
